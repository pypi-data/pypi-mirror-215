import os 
import sys
import json
import yaml
import tempfile
import requests
import posixpath
import contextlib

from typing import Dict, Optional, List, Any, Union

from .entities import experiment, run
from .store.model import ModelStore
from .entities.model import Model
from .error.value_error import HaiqvValueError
from .utils.common import get_milis, key_subset_split
from .utils.files import _guess_mime_type, path_not_unique, relative_path_to_artifact_path

#### EXP

def get_experiments_list(filter_str:Optional[str] = None, view_type:int = 1) -> List[experiment.Experiment]:
    params = {
        'view_type': view_type
    }
    if filter_str:
        params['filter'] = filter_str

    exps = requests.post(
        f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiments',
        params=json.dumps(params)
    )

    if exps.status_code == 200:
        return [experiment.Experiment(**exp.json()) for exp in exps]
    else:
        raise HaiqvValueError(exps.json())


def get_experiment(exp_id=None, exp_name=None) -> experiment.Experiment:
    assert exp_id or exp_name, 'init need experiment id or experiment name'
    
    if exp_id:        
        exp = requests.get(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
            params={'experiment_id': exp_id}
        )
        if exp.status_code == 200:            
            return experiment.Experiment(**exp.json())
        else:
            raise HaiqvValueError(exp.json())
    else:
        exp = requests.get(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
            params = {'experiment_name': exp_name}
        )
        
        if exp.status_code == 200:            
            return experiment.Experiment(**exp.json())
        else:
            raise HaiqvValueError(exp.json())
        
def create_experiment(exp_name, desc:str = None, tags:Optional[Dict[str, Any]] = None) -> experiment.Experiment:
    if desc:
        if tags:
            tags['mlflow.note.content'] = desc
        else:
            tags = {'mlflow.note.content': desc}

    if tags:
        exp_tags = [{'key': k, 'value': str(v) } for k, v in tags.items()]
    
    exp_data = {
        'name': exp_name,
        'tags': exp_tags if tags else tags
    }

    exp = requests.post(
        f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
        data = json.dumps(exp_data)
    )

    return experiment.Experiment(**exp.json())

def update_experiment(exp_id:str, new_name:Optional[str] = None, tags:Optional[Dict]=None) -> None:
    if tags:
        exp_tags = [{'key': k, 'value': str(v)} for k, v in tags.items()]
        for exp_tag in exp_tags:
            tag = requests.patch(
                f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment/tags',
                params=json.dumps({'experiment_id': exp_id, 'key': exp_tag['key'], 'value': exp_tag['value']})
            )
            if tag.status_code == 200:
                print(f"Set Tag Complete:\nkey={exp_tag['key']}, value={exp_tag['value']}")
            else:
                raise HaiqvValueError(tag.json())
                
    if new_name:
        exp = requests.patch(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
            params=json.dumps({'experiment_id': exp_id, 'new_name': new_name})
        )
        if exp.status_code == 200:
            print(f'name change complete:\nexperiment id = {exp_id}, new_name={new_name}')
        else:
            raise HaiqvValueError(exp.json())
    

def delete_experiment(exp_id=None, exp_name=None) -> None:
    assert exp_id or exp_name, 'init need experiment id or experiment name'
    
    if exp_id:        
        exp = requests.delete(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
            data=json.dumps({'experiment_id': exp_id})
        )        
        if exp.status_code == 204:
            print(f'delete complete: experiment id = {exp_id}')
        else:
            raise HaiqvValueError(exp.json())
    else:        
        exp = requests.delete(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/experiment',
            data = json.dumps({'experiment_name': exp_name})
        )
        if exp.status_code == 204:
            print(f'delete complete: experiment name = {exp_name}')
        else:
            raise HaiqvValueError(exp.json())

##### RUNS

def get_run_lists(exp_ids:str, filter_str:Optional[str] = None, run_view_type:int = 1):
    params = {
        'experiment_ids': exp_ids,
        'view_type': run_view_type
    }

    if filter_str:
        params['filter'] = filter_str

    runs = requests.post(
        f'{os.environ.get("_HAIQV_BASE_URL")}/api/runs',
        params=json.dumps(params)
    )

    if runs.status_code == 200:
        return [run.Run(**item.json()) for item in runs]
    else:
        raise HaiqvValueError(runs.json())

def get_run(run_id:str) -> run.Run:
    run_item = requests.get(
        f'{os.environ.get("_HAIQV_BASE_URL")}/api/run',
        params={'run_id': run_id}
    )
    if run_item.status_code == 200:
        return run.Run(**run_item.json())
    else:
        raise HaiqvValueError(run_item.json())

def create_run(exp_id: str, run_name: str, start_time: int, desc: str = None, tags: Optional[Dict[str, Any]] = None) -> run.Run:
    if desc:
        if tags:
            tags['mlflow.note.content'] = desc
        else:
            tags = {'mlflow.note.content': desc}
        
    if tags:
        run_tags = [{'key': k, 'value': str(v) } for k, v in tags.items()]

    data = {
        'experiment_id': exp_id,
        'run_name': run_name,
        'start_time': start_time if start_time else get_milis(),
        'tags': run_tags if tags else tags
    }

    runs = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run', data = json.dumps(data))

    if runs.status_code == 200:
        return run.Run(info=runs.json()['info'], data=runs.json()['data'])
    else:
        raise HaiqvValueError(runs.json())

def update_run(
        run_id: str,
        status: Optional[str] = None,
        end_time: Optional[int] = None,
        run_name: Optional[str] = None,
    ) -> None:

    data = {
        'run_id': run_id
    }

    if status:
        data['status'] = status
    
    if end_time:
        data['end_time'] = end_time
    else:
        data['end_time'] = get_milis()

    if run_name:
        data['run_name'] = run_name

    res = requests.patch(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run', data = json.dumps(data))

    if res.status_code != 200:        
        raise HaiqvValueError(res.json())

def delete_run(run_id:str) -> None:
    run_item = requests.delete(
        f'{os.environ.get("_HAIQV_BASE_URL")}/api/run',
        data=json.dumps({'run_id': run_id})
    )

    if run_item.status_code == 204:
        print(f'delete complete: run id = {run_id}')
    else:
        raise HaiqvValueError(run_item.json())
    
#### LOGS

def log_param(run_id: str, key: str, value: Any) -> None:
    """
    Log a parameter (e.g. model hyperparameter) under the current run. If no run is active,
    this method will create a new active run.

    :param key: Parameter name (string). This string may only contain alphanumerics,
                underscores (_), dashes (-), periods (.), spaces ( ), and slashes (/).
                All backend stores support keys up to length 250, but some may
                support larger keys.
    :param value: Parameter value (string, but will be string-ified if not).
                  All backend stores support values up to length 500, but some
                  may support larger values.

    :return: the parameter value that is logged.

    .. test-code-block:: python
        :caption: Example

        import mlflow

        with mlflow.start_run():
            value = mlflow.log_param("learning_rate", 0.01)
            assert value == 0.01
    """    
    data = {
        'run_id': run_id,
        'key': key,
        'value': value
    }

    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/param', data = json.dumps(data))
    if res.status_code != 200:
        raise HaiqvValueError(res.json())

# Metrics 기록
def log_metric(run_id: str, key: str, value: float, step: Optional[int] = None, subset: Optional[str] = None) -> None:
    '''
    mlflow: Names may only contain alphanumerics, underscores (_), dashes (-), periods (.), spaces ( ), and slashes (/)
    '''
    assert '/' not in key, 'not allow (/) in metric_key'

    if subset is None:
        metric_key = key
    else:
        metric_key = f'{key}/{subset}'
    
    data = {
        'run_id': run_id,
        'key': metric_key,
        'value': value,
        'step': step,
        'timestamp': get_milis()
    }

    requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/metric', data = json.dumps(data))

def log_batch(run_id: str, data: dict) -> None:
    '''
    :param data: Dict[str, List[Dict[str, Any]] contains Metric, Params, Tags    
    '''
    data['run_id'] = run_id
    requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/batches', data = json.dumps(data))

def log_artifact(run_id: str, local_file: str, artifact_path: Optional[str] = None) -> None:
    '''
    artifact path 관련된건 그대로 베낀거라 추후 라이센스 문제가 생길수도 있지 않을까?
    나중에 다르게 고쳐보자
    '''
    assert not (artifact_path and path_not_unique(artifact_path)), f'Invalide artifact Path: {artifact_path}'
        
    filename = os.path.basename(local_file)
    mime = _guess_mime_type(filename)
    paths = (artifact_path, filename) if artifact_path else (filename,)
    endpoint = posixpath.join("/", *paths)
    headers = {'Content-type': mime}
    
    with open(local_file, 'rb') as f:
        requests.put(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/artifact?run_id={run_id}&artifact_path={endpoint}',
            files={'local_file':(filename, f, headers)}
        )

def log_artifacts(run_id: str, local_dir: str, artifact_path: Optional[str] = None) -> None:
    '''
    요것도 그대로 베낀거라 나중에 찬찬히 고쳐보자
    '''    
    
    local_dir = os.path.abspath(local_dir)
    for root, _, files in os.walk(local_dir):
        if root == local_dir:
            artifact_dir = artifact_path
        else:
            rel_path = os.path.relpath(root, local_dir)
            rel_path = relative_path_to_artifact_path(rel_path)
            artifact_dir = (
                posixpath.join(artifact_path, rel_path) if artifact_path else rel_path
            )

        for f in files:
            log_artifact(run_id= run_id, local_file=os.path.join(root, f), artifact_path=artifact_dir)

@contextlib.contextmanager
def _log_artifact_helper(run_id, artifact_file):
    """
    Yields a temporary path to store a file, and then calls `log_artifact` against that path.

    :param run_id: String ID of the run.
    :param artifact_file: The run-relative artifact file path in posixpath format.
    :return: Temporary path to store a file.
    """
    norm_path = posixpath.normpath(artifact_file)
    filename = posixpath.basename(norm_path)
    artifact_dir = posixpath.dirname(norm_path)
    artifact_dir = None if artifact_dir == "" else artifact_dir

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, filename)
        yield tmp_path
        log_artifact(run_id, tmp_path, artifact_dir)

# 이 아래로 쭉 베낀거

def log_text(run_id: str, text: str, artifact_file: str) -> None:
    """    
    Log text as an artifact.

    :param run_id: String ID of the run.
    :param text: String containing text to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the text is saved (e.g. "dir/file.txt").

    .. code-block:: python
        :caption: Example

        from mlflow import MlflowClient

        client = MlflowClient()
        run = client.create_run(experiment_id="0")

        # Log text to a file under the run's root artifact directory
        client.log_text(run.info.run_id, "text1", "file1.txt")

        # Log text in a subdirectory of the run's root artifact directory
        client.log_text(run.info.run_id, "text2", "dir/file2.txt")

        # Log HTML text
        client.log_text(run.info.run_id, "<h1>header</h1>", "index.html")
    """
    
    with _log_artifact_helper(run_id, artifact_file) as tmp_path:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(text)

def log_dict(run_id: str, dictionary: Any, artifact_file: str) -> None:
    """
    Log a JSON/YAML-serializable object (e.g. `dict`) as an artifact. The serialization
    format (JSON or YAML) is automatically inferred from the extension of `artifact_file`.
    If the file extension doesn't exist or match any of [".json", ".yml", ".yaml"],
    JSON format is used.

    :param run_id: String ID of the run.
    :param dictionary: Dictionary to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the dictionary is saved (e.g. "dir/data.json").

    .. code-block:: python
        :caption: Example

        from mlflow import MlflowClient

        client = MlflowClient()
        run = client.create_run(experiment_id="0")
        run_id = run.info.run_id

        dictionary = {"k": "v"}

        # Log a dictionary as a JSON file under the run's root artifact directory
        client.log_dict(run_id, dictionary, "data.json")

        # Log a dictionary as a YAML file in a subdirectory of the run's root artifact directory
        client.log_dict(run_id, dictionary, "dir/data.yml")

        # If the file extension doesn't exist or match any of [".json", ".yaml", ".yml"],
        # JSON format is used.
        mlflow.log_dict(run_id, dictionary, "data")
        mlflow.log_dict(run_id, dictionary, "data.txt")
    """
    
    extension = os.path.splitext(artifact_file)[1]

    with _log_artifact_helper(run_id, artifact_file) as tmp_path:
        with open(tmp_path, "w") as f:
            # Specify `indent` to prettify the output
            if extension in [".yml", ".yaml"]:
                yaml.dump(dictionary, f, indent=2, default_flow_style=False)
            else:
                json.dump(dictionary, f, indent=2)

def log_figure(
    run_id: str, 
    figure: Union["matplotlib.figure.Figure", "plotly.graph_objects.Figure"],
    artifact_file: str
) -> None:
    """
    Log a figure as an artifact. The following figure objects are supported:

    - `matplotlib.figure.Figure`_
    - `plotly.graph_objects.Figure`_

    .. _matplotlib.figure.Figure:
        https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html

    .. _plotly.graph_objects.Figure:
        https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html

    :param run_id: String ID of the run.
    :param figure: Figure to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the figure is saved (e.g. "dir/file.png").

    .. code-block:: python
        :caption: Matplotlib Example

        import mlflow
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([0, 1], [2, 3])

        run = client.create_run(experiment_id="0")
        client.log_figure(run.info.run_id, fig, "figure.png")

    .. code-block:: python
        :caption: Plotly Example

        import mlflow
        from plotly import graph_objects as go

        fig = go.Figure(go.Scatter(x=[0, 1], y=[2, 3]))

        run = client.create_run(experiment_id="0")
        client.log_figure(run.info.run_id, fig, "figure.html")
    """

    def _is_matplotlib_figure(fig):
        import matplotlib.figure

        return isinstance(fig, matplotlib.figure.Figure)

    def _is_plotly_figure(fig):
        import plotly

        return isinstance(fig, plotly.graph_objects.Figure)
    
    

    with _log_artifact_helper(run_id, artifact_file) as tmp_path:
        # `is_matplotlib_figure` is executed only when `matplotlib` is found in `sys.modules`.
        # This allows logging a `plotly` figure in an environment where `matplotlib` is not
        # installed.
        if "matplotlib" in sys.modules and _is_matplotlib_figure(figure):
            figure.savefig(tmp_path)
        elif "plotly" in sys.modules and _is_plotly_figure(figure):
            file_extension = os.path.splitext(artifact_file)[1]
            if file_extension == ".html":
                figure.write_html(tmp_path, include_plotlyjs="cdn", auto_open=False)
            elif file_extension in [".png", ".jpeg", ".webp", ".svg", ".pdf"]:
                figure.write_image(tmp_path)
            else:
                raise TypeError(
                    f"Unsupported file extension for plotly figure: '{file_extension}'"
                )
        else:
            raise TypeError("Unsupported figure object type: '{}'".format(type(figure)))

def log_image(
    run_id: str, 
    image: Union["numpy.ndarray", "PIL.Image.Image"], 
    artifact_file: str
) -> None:
    """
    Log an image as an artifact. The following image objects are supported:

    - `numpy.ndarray`_
    - `PIL.Image.Image`_

    .. _numpy.ndarray:
        https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html

    .. _PIL.Image.Image:
        https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image

    Numpy array support
        - data type (( ) represents a valid value range):

            - bool
            - integer (0 ~ 255)
            - unsigned integer (0 ~ 255)
            - float (0.0 ~ 1.0)

            .. warning::

                - Out-of-range integer values will be **clipped** to [0, 255].
                - Out-of-range float values will be **clipped** to [0, 1].

        - shape (H: height, W: width):

            - H x W (Grayscale)
            - H x W x 1 (Grayscale)
            - H x W x 3 (an RGB channel order is assumed)
            - H x W x 4 (an RGBA channel order is assumed)

    :param run_id: String ID of the run.
    :param image: Image to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the image is saved (e.g. "dir/image.png").

    .. code-block:: python
        :caption: Numpy Example

        import mlflow
        import numpy as np

        image = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)

        run = client.create_run(experiment_id="0")
        client.log_image(run.info.run_id, image, "image.png")

    .. code-block:: python
        :caption: Pillow Example

        import mlflow
        from PIL import Image

        image = Image.new("RGB", (100, 100))

        run = client.create_run(experiment_id="0")
        client.log_image(run.info.run_id, image, "image.png")
    """

    def _is_pillow_image(image):
        from PIL.Image import Image

        return isinstance(image, Image)

    def _is_numpy_array(image):
        import numpy as np

        return isinstance(image, np.ndarray)

    def _normalize_to_uint8(x):
        # Based on: https://github.com/matplotlib/matplotlib/blob/06567e021f21be046b6d6dcf00380c1cb9adaf3c/lib/matplotlib/image.py#L684

        is_int = np.issubdtype(x.dtype, np.integer)
        low = 0
        high = 255 if is_int else 1
        if x.min() < low or x.max() > high:
            msg = (
                "Out-of-range values are detected. "
                "Clipping array (dtype: '{}') to [{}, {}]".format(x.dtype, low, high)
            )
            print(msg)
            x = np.clip(x, low, high)

        # float or bool
        if not is_int:
            x = x * 255

        return x.astype(np.uint8)
    
    

    with _log_artifact_helper(run_id, artifact_file) as tmp_path:
        if "PIL" in sys.modules and _is_pillow_image(image):
            image.save(tmp_path)
        elif "numpy" in sys.modules and _is_numpy_array(image):
            import numpy as np

            try:
                from PIL import Image
            except ImportError as exc:
                raise ImportError(
                    "`log_image` requires Pillow to serialize a numpy array as an image. "
                    "Please install it via: pip install Pillow"
                ) from exc

            # Ref.: https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html#numpy-dtype-kind
            valid_data_types = {
                "b": "bool",
                "i": "signed integer",
                "u": "unsigned integer",
                "f": "floating",
            }

            if image.dtype.kind not in valid_data_types:
                raise TypeError(
                    f"Invalid array data type: '{image.dtype}'. "
                    f"Must be one of {list(valid_data_types.values())}"
                )

            if image.ndim not in [2, 3]:
                raise ValueError(
                    "`image` must be a 2D or 3D array but got a {}D array".format(image.ndim)
                )

            if (image.ndim == 3) and (image.shape[2] not in [1, 3, 4]):
                raise ValueError(
                    "Invalid channel length: {}. Must be one of [1, 3, 4]".format(
                        image.shape[2]
                    )
                )

            # squeeze a 3D grayscale image since `Image.fromarray` doesn't accept it.
            if image.ndim == 3 and image.shape[2] == 1:
                image = image[:, :, 0]

            image = _normalize_to_uint8(image)

            Image.fromarray(image).save(tmp_path)

        else:
            raise TypeError("Unsupported image object type: '{}'".format(type(image)))

'''
모델 파일 기록할 때, 그때 당시의 metric이나 step을 같이 가져가야 할 필요성 있음
- 기록 대상:
    - model_path
    - step
    - metric

- log_model_metadata1: run 객체를 전달
- log_model_metadata2: current_active_run으로 자동 추출해서 전달(위험성이 있을 것 같음.. 뭔가가 걸림... 뭔가가...)
- log_model_metadata3: 전부 수동으로 받아서 artifacts로 파일로 기록
'''

# def log_model_metadata1(run: Run, model_nm: str, model_path: str, step:int, metric: Optional[dict] = None, metric_subset: Optional[str] = None, tags: Optional[dict] = None) -> None:
#     model_tags = dict()
#     client = MlflowClient()

#     run_uri = "runs:/{}/{}".format(run.info.run_id, model_nm)
#     model_src = RunsArtifactRepository.get_underlying_uri(run_uri) # 모델 파일이 원래 업로드 되야 하는 path

#     model_tags['path'] = os.path.abspath(model_path)
#     model_tags['step'] = step
    
#     if metric is None:
#         model_tags['metric'] = dict()
#         runs = client.get_run(run.info.run_id)

#         for key in runs.data.metrics.keys():
#             metric = [metric for metric in client.get_metric_history(runs.info.run_id, key) if metric.step == step]            
#             if len(metric) != 0:            
#                 model_tags['metric'].update({
#                     metric[0].key: metric[0].value
#                 })                                        
#     else:        
#         if metric_subset:
#             model_tags['metric'] = {f'{k}/{metric_subset}':v for k,v in metric.items()}                        
#         else:
#             model_tags['metric'] = metric            

#     if tags:
#         model_tags.update(tags)
    
#     try:
#         client.get_registered_model(model_nm)
#     except:
#         client.create_registered_model(model_nm)
    
#     client.create_model_version(model_nm, model_src, run.info.run_id, tags=model_tags, await_creation_for=0)

# def log_model_metadata2(model_nm: str, model_path: str, step:int, metric: Optional[dict] = None, metric_subset:Optional[str] = None, tags: Optional[dict] = None) -> None:
#     model_tags = dict()
#     client = MlflowClient()

#     task = get_current_active_run()
#     runs = client.get_run(task.info.run_id)

#     run_uri = "runs:/{}/{}".format(runs.info.run_id, model_nm)
#     model_src = RunsArtifactRepository.get_underlying_uri(run_uri) # 모델 파일이 원래 업로드 되야 하는 path

#     model_tags['path'] = os.path.abspath(model_path)
#     model_tags['step'] = step

#     if metric is None:
#         model_tags['metric'] = dict()
#         for key in runs.data.metrics.keys():
#             metric = [metric for metric in client.get_metric_history(runs.info.run_id, key) if metric.step == step]
#             if len(metric) != 0:                
#                 model_tags['metric'].update({
#                     metric[0].key: metric[0].value
#                 })                    
#     else:        
#         if metric_subset:
#             model_tags['metric'] = {f'{k}/{metric_subset}':v for k,v in metric.items()}            
#         else:
#             model_tags['metric'] = metric            

#     if tags:
#         model_tags.update(tags)
    
#     try:
#         client.get_registered_model(model_nm)
#     except:
#         client.create_registered_model(model_nm)
    
#     client.create_model_version(model_nm, model_src, runs.info.run_id, tags=model_tags, await_creation_for=0)

# 여기까지
def log_model_metadata(
        run_id: str, 
        model_nm:str, 
        model_path: str, 
        step: int, 
        metric: Optional[dict] = None, 
        tags: Optional[dict] = None) -> None:
    '''
    train step이랑 valid step이랑 차이가 있을 수 밖에 없음
    그냥 step에 따른 값을 가져오는게 아니라
    latest metric을 추가하는게 어떨까 생각해봐야 함
    '''
    
    runs = get_run(run_id)    

    model_tags = dict()
    model_tags['model_path'] = os.path.abspath(model_path)
    model_tags['step'] = step    

    if metric is None:
        # 1. Step에 맞춰 Metric 가져오기
        # model_tags['metric'] = dict()
        # for m in runs.data['metrics']:
        #     key, subset = key_subset_split(m['key'])

        #     metric = [metric for metric in get_metric_history(key, subset=subset, run_id=runs.info['run_id']) if metric['step'] == step]
        #     for item in metric:
        #         k, s = key_subset_split(item['key'])
        #         if k in model_tags['metric'].keys():
        #             model_tags['metric'][k].update({s: item['value']} if s else item['value'])
        #         else:
        #             model_tags['metric'].update({
        #                 k: {s: item['value']} if s else item['value']
        #             })             

        # 2. Latest Metric 가져오기
        model_tags['metric'] = dict()
        for m in runs.data['metrics']:
            (key, subset), value = key_subset_split(m['key']), m['value']
            if key in model_tags['metric'].keys():
                model_tags['metric'][key].append({
                    'subset': subset,
                    'value': value
                })
            else:
                model_tags['metric'][key] = [{
                    'subset': subset,
                    'value': value
                }]
    else:
        model_tags['metric'] = metric

    if tags:
        model_tags.update(tags)

    log_dict(run_id, model_tags, f'models/{model_nm}_step_{step}.txt')

def log_model_metadata_versioning(
        run_id: str, 
        model_nm:str, 
        model_path: str, 
        step: int, 
        metric: Optional[dict] = None, 
        tags: Optional[dict] = None) -> None:    
    '''
    train step이랑 valid step이랑 차이가 있을 수 밖에 없음
    그냥 step에 따른 값을 가져오는게 아니라
    latest metric을 추가하는게 어떨까 생각해봐야 함
    '''
    
    runs = get_run(run_id)

    ms = ModelStore()

    model_tags = dict()
    model_tags['model_path'] = os.path.abspath(model_path)
    model_tags['step'] = step    

    if metric is None:
        # 1. Step에 맞춘 metric 가져오기
        # model_tags['metric'] = dict()
        # for m in runs.data['metrics']:            
        #     key, subset = key_subset_split(m['key'])

        #     metric = [metric for metric in get_metric_history(key, subset=subset, run_id=runs.info['run_id']) if metric['step'] == step]
        #     for item in metric:
        #         k, s = key_subset_split(item['key'])
        #         if k in model_tags['metric'].keys():
        #             model_tags['metric'][k].update({s: item['value']} if s else item['value'])
        #         else:
        #             model_tags['metric'].update({
        #                 k: {s: item['value']} if s else item['value']
        #             })             
        
        # 2. latest Metric 가져오기
        model_tags['metric'] = dict()
        for m in runs.data['metrics']:
            (key, subset), value = key_subset_split(m['key']), m['value']            
            if key in model_tags['metric'].keys():
                model_tags['metric'][key].append({
                    'subset': subset,
                    'value': value
                })
            else:
                model_tags['metric'][key] = [{
                    'subset': subset,
                    'value': value
                }]
    else:
        model_tags['metric'] = metric
    
    if tags:
        model_tags.update(tags)
    else:
        model_tags['tags'] = None
    
    mv = ms.add_version(Model(model_nm=model_nm,**model_tags))

    log_dict(run_id, mv, f'models/model_{model_nm}_info.txt')

# def log_datasets1(data_nm: str, path: str):
#     '''
#     dataset을 log_param으로 path만 담아서 보관
#     나중에 DATASET인것을 확인하기 위해 prefix로 HAIQV_DATASET_을 붙이고 data_nm으로 key값을 생성하기로 함

#     dataset목록은 log_params로 기록된 것에서 startwith HAIQV_DATASET으로 가져오면 됨
#     '''
#     
#     log_param(f'HAIQV_DATASET_{data_nm}', path, run_id = run_id)

def log_datasets(run_id: str, data_nm: str, path: str, desc: str = None, tags: dict = None):
    '''
    log_dataset을 그냥 log_params만 할 경우 datadir만 넣게 될 경우 의미가 없을 것 같음

    ## 기각
    차라리 해당 기능을 넣는다면 glob.glob같은걸 써서 해당 폴더 밑에 
    파일 이름들이나 파일 갯수를 추가 기록해주면 도움이 되지 않을까 싶은데
    사실 파일 이름을 기록한다고 해도 파일 양이 많으면 그걸 누가 보겠냐 하는 생각이 들기는 함
    log_dict를 사용해서 처리 하는 것이 좋아보임

    ## 아이디어
    일단은 log_dict로 artifacts 폴더에 dataset 폴더 밑에 각 데이터 셋의 정보를 기록하여 파일로 떨굼
    이렇게 하면 dataset의 정보만 가져올 수 있음

    - 기록
    path: 파일 패스
    desc: 사용자 정의 파일 설명(default: None)
    tags: 사용자 정의 파일 태그(default: None)
    
    '''    
    
    datasets = dict()
    
    datasets['path'] = os.path.abspath(path)
    
    if desc:
        datasets['desc'] = desc

    if tags:
        datasets.update(tags)

    log_dict(run_id, datasets, f'dataset/{data_nm}_info.txt')

def get_metric_history(run_id: str, metric_key: str, subset: Optional[str] = None) -> dict:
    
    metrics = requests.get(
            f'{os.environ.get("_HAIQV_BASE_URL")}/api/metrics',
            params={
                'run_id': run_id,
                'metric_key': metric_key,
                'subset': subset
            }
        )
    
    return metrics.json()