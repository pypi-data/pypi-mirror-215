from typing import Optional, Union, Dict

class Model:
    def __init__(
            self, 
            model_nm: Optional[str], 
            model_path: str, 
            step: int, 
            metric: Optional[Dict],             
            tags: Optional[Dict]
        ):
        self.model_nm = model_nm
        self.model_path = model_path
        self.step = step
        self.metric = metric
        self.tags = tags
    
    @property
    def model_nm(self):
        return self._model_nm
    
    @model_nm.setter
    def model_nm(self, new_nm):
        self._model_nm = new_nm
    
    @property
    def model_path(self):
        return self._model_path
    
    @model_path.setter
    def model_path(self, new_path):
        self._model_path = new_path
    
    @property
    def step(self):
        return self._step
    
    @step.setter
    def step(self, new_step):
        self._step = new_step
    
    @property
    def metric(self):
        return self._metric
    
    @metric.setter
    def metric(self, new_metric):
        self._metric = new_metric

    @property
    def tags(self):
        return self._tags
    
    @tags.setter
    def tags(self, new_tags):
        self._tags = new_tags