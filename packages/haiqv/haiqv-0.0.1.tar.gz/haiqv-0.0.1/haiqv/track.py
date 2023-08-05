import os
import json
import requests
import pkg_resources
import __main__

from typing import Any, Dict, Optional, Union
from datetime import datetime

from .binding.args_bind import ArgBind
from .binding.yaml_bind import YamlBind
from .entities.run import Run
from .store import ExpStore, RunStore
from .job.background_task import BackGroundTask
from . import client

from .error.value_error import HaiqvValueError
from .utils.common import get_milis, key_subset_split
from .utils.files import _guess_mime_type, path_not_unique, relative_path_to_artifact_path

__HAIQV_UPLOAD_INTERVAL = 2
__HAIQV_STD_LOG_FILE = 'output.log'

class ActiveRun(Run):  # pylint: disable=W0223
    """Wrapper around :py:class:`mlflow.entities.Run` to enable using Python ``with`` syntax."""

    def __init__(self, run):
        Run.__init__(self, run.info, run.data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):        
        status = 'FINISHED' if exc_type is None else 'FAILED'
        close(status)
        return exc_type is None

def init(
        experiment_name: str = None, 
        experiment_id: str = None,
        experiment_tags: Optional[Dict[str, Any]] = None,
        experiment_description: Optional[str] = None,
        run_id: str = None,        
        run_name: Optional[str] = None,
        run_tags: Optional[Dict[str, Any]] = None,
        run_description: Optional[str] = None,
        auto_track_args: bool = False
    ) -> ActiveRun:    
    # client = MlflowClient()
    
    # if experiment_id:
    #     if fluent.get_experiment(experiment_id = experiment_id):
    #         print(f'connect exist experiments id: {experiment_id}')
    #     else:
    #         print(f'create new experiments id: {experiment_id}')
    # else:
    #     if experiment_name:
    #         if fluent.get_experiment_by_name(name = experiment_name):
    #             print(f'connect exist experiments name: {experiment_name}')
    #         else:
    #             print(f'create new experiments name: {experiment_name}')

    # exp = fluent.set_experiment(experiment_name, experiment_id)
    assert experiment_id or experiment_name, 'init need experiment id or experiment name'    
    
    if experiment_id:
        exps = client.get_experiment(exp_id=experiment_id)
        print(f'connect exist experiments id: {experiment_id}')
    elif experiment_name:
        try:
            exps = client.get_experiment(exp_name=experiment_name)
            print(f'connect exist experiments name: {experiment_name}')
        except HaiqvValueError as e:
            exps = client.create_experiment(exp_name=experiment_name, desc= experiment_description, tags= experiment_tags)
            print(f'create new experiments name: {experiment_name}')        
    
    ExpStore(exps)

    if run_name:
        # assert client.search_runs(exp._experiment_id, filter_string=f"run_name='{run_name}'") == None, 'duplicated run name in same experiments'
        run_name = f"{run_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    else:
        run_name = f"run-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    if RunStore.status():
        HaiqvValueError({
            'error_code': 'CLOSE ACTIVE RUN FIRST',
            'message':'already has active runs, please run close() command first.'
        })

    if run_id:
        runs = client.get_run(run_id = run_id)
        print(f'connect exist run id: {run_id}')
    elif run_name:        
        runs = client.create_run(
            exp_id = ExpStore.experiment.experiment_id,
            run_name = run_name,
            start_time = get_milis(),
            desc = run_description,
            tags = run_tags
        )
        print(f'start run name: {run_name}')

    if not RunStore.status():
        RunStore(runs)

    running_file = __main__.__file__
    

    dists = [str(d).replace(" ","==") for d in pkg_resources.working_set]

    if os.path.getsize(running_file) > 0:
        log_artifact(running_file, "code")
    log_text('\n'.join(dists), "requirements.txt")

    if auto_track_args:
        ArgBind.patch_argparse(log_params)
        YamlBind.patch_load(log_params)
    
    bg = BackGroundTask() 
    bg.set_std_log_config(__HAIQV_STD_LOG_FILE, __HAIQV_UPLOAD_INTERVAL, log_artifact)
    bg.start_std_log()

    return ActiveRun(runs)

def get_current_active_run() -> Run:
    assert RunStore.status(), 'has not active runs, please run init() command first'

    return RunStore()

def close(status: str = "FINISHED") -> None:
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
    bg = BackGroundTask()    
    bg.end_std_log()
    client.update_run(
        run_id=get_current_active_run().info['run_id'],
        status=status,
        end_time=get_milis()
    )
    RunStore.flush()

def log_param(key: str, value: Any) -> None:
    """
    Log a parameter (e.g. model hyperparameter) under the current run.

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
    run_id = get_current_active_run().info['run_id']
    client.log_param(run_id=run_id, key=key, value=value)

def log_params(params: Dict[str, Any]) -> None:
    """
    Log a batch of params for the current run.

    :param params: Dictionary of param_name: String -> value: (String, but will be string-ified if
                   not)
    :returns: None

    .. test-code-block:: python
        :caption: Example

        import mlflow

        params = {"learning_rate": 0.01, "n_estimators": 10}

        # Log a batch of parameters
        with mlflow.start_run():
            mlflow.log_params(params)
    """
    run_id = get_current_active_run().info['run_id']

    data = {        
        'metrics': [],
        'params': [{'key': key, 'value': str(value)} for key, value in params.items()],
        'tags': []
    }

    client.log_batch(run_id, data)

    # requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/batches', data = json.dumps(data))

# Metrics 기록
def log_metric(key: str, value: float, step: Optional[int] = None, subset: Optional[str] = None) -> None:
    '''
    mlflow: Names may only contain alphanumerics, underscores (_), dashes (-), periods (.), spaces ( ), and slashes (/)
    '''
    run_id = get_current_active_run().info['run_id']
    client.log_metric(run_id=run_id, key=key, value=value, step=step, subset=subset)

def log_metrics(metrics: Dict[str, float], step: Optional[int] = None, subset: Optional[str] = None) -> None:
    '''
    mlflow: Names may only contain alphanumerics, underscores (_), dashes (-), periods (.), spaces ( ), and slashes (/)
    '''
    assert sum(['/' in k for k in metrics.keys()]) == 0, 'not allow (/) in metric_key'

    run_id = get_current_active_run().info['run_id']

    if subset is None:
        subset_metrics = metrics
    else:
        subset_metrics = {f'{k}/{subset}':v for k,v in metrics.items()}
    
    data = {
        'metrics': [{'key': key, 'value': str(value), 'step': step or 0, 'timestamp': get_milis()} for key, value in subset_metrics.items()],
        'params': [],
        'tags': []
    }

    client.log_batch(run_id, data)

    # requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/api/run/batches', data = json.dumps(data))

def log_batch(run_id: str, data: dict) -> None:
    '''
    :param data: Dict[str, List[Dict[str, Any]] contains Metric, Params, Tags    
    '''
    run_id = get_current_active_run().info['run_id']

    client.log_batch(run_id=run_id, data=data)

def log_artifact(local_file: str, artifact_path: Optional[str] = None) -> None:    
    run_id = get_current_active_run().info['run_id']
    client.log_artifact(run_id=run_id, local_file=local_file, artifact_path=artifact_path)

def log_artifacts(local_dir: str, artifact_path: Optional[str] = None) -> None:        
    run_id = get_current_active_run().info['run_id']
    client.log_artifacts(run_id=run_id, local_dir=local_dir, artifact_path=artifact_path)

# 이 아래로 쭉 베낀거

def log_text(text: str, artifact_file: str) -> None:
    """    
    Log text as an artifact for the current run.

    :param text: String containing text to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the text is saved (e.g. "dir/file.txt").    
    """
    run_id = get_current_active_run().info['run_id']
    client.log_text(run_id=run_id, text=text, artifact_file=artifact_file)    

def log_dict(dictionary: Any, artifact_file: str) -> None:
    """
    Log a JSON/YAML-serializable object (e.g. `dict`) as an artifact. The serialization
    format (JSON or YAML) is automatically inferred from the extension of `artifact_file`.
    If the file extension doesn't exist or match any of [".json", ".yml", ".yaml"],
    JSON format is used.
    
    :param dictionary: Dictionary to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the dictionary is saved (e.g. "dir/data.json").    
    """
    run_id = get_current_active_run().info['run_id']
    client.log_dict(run_id=run_id, dictionary=dictionary, artifact_file=artifact_file)

def log_figure(
    figure: Union["matplotlib.figure.Figure", "plotly.graph_objects.Figure"],
    artifact_file: str,
    run_id: Optional[str] = None
) -> None:
    """
    Log a figure as an artifact. The following figure objects are supported:

    - `matplotlib.figure.Figure`_
    - `plotly.graph_objects.Figure`_

    .. _matplotlib.figure.Figure:
        https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html

    .. _plotly.graph_objects.Figure:
        https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    
    :param figure: Figure to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the figure is saved (e.g. "dir/file.png").
    """
    run_id = get_current_active_run().info['run_id']
    client.log_figure(run_id=run_id, figure=figure, artifact_file=artifact_file)

def log_image(
    image: Union["numpy.ndarray", "PIL.Image.Image"], artifact_file: str
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
    
    :param image: Image to log.
    :param artifact_file: The run-relative artifact file path in posixpath format to which
                            the image is saved (e.g. "dir/image.png").    
    """
    run_id = get_current_active_run().info['run_id']
    client.log_image(run_id=run_id, image=image, artifact_file=artifact_file)

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
def log_model_metadata(model_nm:str, model_path: str, step: int, metric: Optional[dict] = None, tags: Optional[dict] = None) -> None:
    '''
    train step이랑 valid step이랑 차이가 있을 수 밖에 없음
    그냥 step에 따른 값을 가져오는게 아니라
    latest metric을 추가하는게 어떨까 생각해봐야 함
    '''
    run_id = get_current_active_run().info['run_id']

    client.log_model_metadata(
        run_id=run_id,
        model_nm=model_nm,
        model_path=model_path,
        step=step,
        metric=metric,
        tags=tags
    )

def log_model_metadata_versioning(model_nm:str, model_path: str, step: int, metric: Optional[dict] = None, tags: Optional[dict] = None) -> None:    
    '''
    train step이랑 valid step이랑 차이가 있을 수 밖에 없음
    그냥 step에 따른 값을 가져오는게 아니라
    latest metric을 추가하는게 어떨까 생각해봐야 함
    '''
    run_id = get_current_active_run().info['run_id']
    client.log_model_metadata_versioning(
        run_id=run_id,
        model_nm=model_nm,
        model_path=model_path,
        step=step,
        metric=metric,
        tags=tags
    )

def log_datasets(data_nm: str, path: str, desc: str = None, tags: dict = None):
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
    run_id = get_current_active_run().info['run_id']
    client.log_datasets(
        run_id=run_id,
        data_nm=data_nm,
        path=path,
        desc=desc,
        tags=tags
    )

def get_metric_history(metric_key: str, subset: Optional[str] = None) -> dict:
    run_id = get_current_active_run().info['run_id']
    
    return client.get_metric_history(run_id=run_id, metric_key=metric_key, subset=subset)