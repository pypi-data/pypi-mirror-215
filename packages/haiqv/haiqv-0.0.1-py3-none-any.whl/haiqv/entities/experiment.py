from typing import Optional, Dict, List

class Experiment:
    def __init__(
            self,
            experiment_id: str,
            name: str,
            artifact_location: str,
            lifecycle_stage: str,
            last_update_time: int,
            creation_time: int,
            tags: Optional[List[Dict[str,str]]] = None
        ):
        self._experiment_id = experiment_id
        self._name = name
        self._artifact_location = artifact_location
        self._lifecycle_stage = lifecycle_stage
        self._last_update_time = last_update_time
        self._creation_time = creation_time
        self._tags = tags
    
    @property
    def experiment_id(self):
        return self._experiment_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def artifact_location(self):
        return self._artifact_location
    
    @property
    def lifecycle_stage(self):
        return self._lifecycle_stage
    
    @property
    def last_update_time(self):
        return self._last_update_time
        
    @property
    def creation_time(self):
        return self._creation_time
    
    @property
    def tags(self):
        return self._tags