from . import configuration_ann
from . import modeling_ann
from . import feature_extraction_ann

def register_auto():
    configuration_ann.register_auto()
    modeling_ann.register_auto()
    feature_extraction_ann.register_auto()
  
