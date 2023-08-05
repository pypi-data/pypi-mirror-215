from ..entities.model import Model

class ModelStore:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls)            
            cls.__instance.models = dict()
            
        return cls.__instance    
    
    def add_version(self, model:Model):        
        if model.model_nm not in self.models.keys():
            self.models[model.model_nm] = {
                'latest_version': 1
            }
            self.models[model.model_nm]['metadata'] = {
                1: {
                    'model_path': model.model_path,
                    'step': model.step,
                    'metric': model.metric,
                    'tags': model.tags                
                }
            }
        else:
            self.models[model.model_nm]['latest_version'] += 1

            self.models[model.model_nm]['metadata'].update({
                self.models[model.model_nm]['latest_version']: {
                    'model_path': model.model_path,
                    'step': model.step,
                    'metric': model.metric,
                    'tags': model.tags
                    }
                }
            )

        return self.models[model.model_nm]
        
    def get_model_name(self) -> list:
        return list(self.models.keys())

    def get_model_by_name(self, model_nm:str):        
        return self.models[model_nm]
    
    def get_model_version_by_name(self, model_nm:str, version:int):
        return self.models[model_nm]['metadata'][version]