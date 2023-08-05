__version__ = '0.0.1'

import os
import pathlib
from dotenv import load_dotenv

stage = os.environ.get('STAGE', None)
if not stage or stage == 'dev':
    load_dotenv(f'{pathlib.Path(__file__).parent.resolve()}/.env.develop')
else:    
    load_dotenv(f'{pathlib.Path(__file__).parent.resolve()}/.env')
    

# pylint: disable=wrong-import-position
__version__ = '0.0.1'

from . import client

from .track import (    
    init,
    get_current_active_run,
    close,
    log_param,
    log_params,
    log_metric,
    log_metrics,
    # log_model_metadata1,
    # log_model_metadata2,
    log_model_metadata,
    log_model_metadata_versioning,    
    log_datasets,
    log_dict,    
    log_figure,
    log_image,
    log_text,
    log_artifact,
    log_artifacts,
    get_metric_history
)

__all__ = [
    "init",
    "get_current_active_run",
    "close",
    "log_param",
    "log_params",
    "log_metric",
    "log_metrics",
    # "log_model_metadata1",
    # "log_model_metadata2",
    "log_model_metadata",
    "log_model_metadata_versioning",
    "log_datasets",
    "log_dict",
    "log_figure",
    "log_image",
    "log_text",
    "log_artifact",
    "log_artifacts",
    "get_metric_history"
]
