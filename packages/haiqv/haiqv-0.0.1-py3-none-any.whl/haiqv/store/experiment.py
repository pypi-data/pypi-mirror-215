from ..entities.experiment import Experiment
from ..error.value_error import HaiqvValueError

class ExpStore():
    @classmethod
    def __init__(cls, exp) -> Experiment:
        if isinstance(exp, Experiment):
            cls.experiment = exp
        else:
            raise HaiqvValueError('not matched variable Type: Experiment')