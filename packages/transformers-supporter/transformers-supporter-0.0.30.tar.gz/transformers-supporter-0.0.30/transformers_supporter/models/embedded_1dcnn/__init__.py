from . import configuration_embedded_1dcnn
from . import modeling_embedded_1dcnn

def register_auto():
    configuration_embedded_1dcnn.register_auto()
    modeling_embedded_1dcnn.register_auto()
