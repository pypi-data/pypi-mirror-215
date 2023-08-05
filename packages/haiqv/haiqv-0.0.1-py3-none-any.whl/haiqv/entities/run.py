from typing import Optional

# class RunInfo:
#     def __init__(
#             self,
#             run_uuid: str,
#             experiment_id: str,
#             run_name: str,
#             user_id: str,
#             status: str,
#             start_time: int,            
#             artifact_uri: str,
#             lifecycle_stage: str,
#             run_id: str,
#             end_time: Optional[int] = None
#     ):
#         self._experiment_id = experiment_id
#         self._run_id = run_id
#         self._run_uuid = run_uuid        
#         self._run_name = run_name
#         self._user_id = user_id
#         self._status = status                    # RUNNING, SCHEDULED, FINISHED, FAILED, KILLED
#         self._start_time = start_time
#         self._end_time = end_time
#         self._artifact_uri = artifact_uri
#         self._lifecycle_stage = lifecycle_stage  # active, delete
    
#     @property
#     def run_uuid(self):
#         return self._run_uuid
    
#     @property
#     def experiment_id(self):
#         return self._experiment_id
    
#     @property
#     def run_name(self):
#         return self._run_name
    
#     @property
#     def user_id(self):
#         return self._user_id
    
#     @property
#     def status(self):
#         return self._status
    
#     @property
#     def start_time(self):
#         return self._start_time
    
#     @property
#     def end_time(self):
#         return self._end_time
    
#     @property
#     def artifact_uri(self):
#         return self._artifact_uri
    
#     @property
#     def lifecycle_stage(self):
#         return self._lifecycle_stage
    
#     @property
#     def run_id(self):
#         return self._run_id
    
# class RunData:
#     def __init__(
#             self,
#             metrics = None,
#             params = None,
#             tags = None
#         ):
#         self._metrics = metrics
#         self._params = params
#         self._tags = tags

#     @property
#     def metrics(self):
#         return self._metrics
        
#     @property
#     def params(self):
#         return self._params
    
#     @property
#     def tags(self):
#         return self._tags
    
class Run:
    def __init__(
            self,
            info,
            data
            # info: RunInfo,
            # data: RunData            
        ):
        self._info = info
        self._data = data
    
    @property
    def info(self):
        return self._info
    
    @property
    def data(self):
        return self._data
    
    def __repr__(self) -> str:
        return str({k.replace('_',''): v for k,v in self.__dict__.items()})