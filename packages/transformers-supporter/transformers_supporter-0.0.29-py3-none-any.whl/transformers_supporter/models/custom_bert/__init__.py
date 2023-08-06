from . import configuration_custom_bert
from . import modeling_custom_bert

def register_auto():
    configuration_custom_bert.register_auto()
    modeling_custom_bert.register_auto()
