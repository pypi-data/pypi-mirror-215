from . import configuration_cnn
from . import modeling_cnn
from . import image_processing_cnn

def register_auto():
    configuration_cnn.register_auto()
    modeling_cnn.register_auto()
    image_processing_cnn.register_auto()
