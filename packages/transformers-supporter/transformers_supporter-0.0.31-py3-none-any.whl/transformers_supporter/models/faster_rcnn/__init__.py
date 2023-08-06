from . import configuration_faster_rcnn
from . import modeling_faster_rcnn
from . import image_processing_faster_rcnn

def register_auto():
    configuration_faster_rcnn.register_auto()
    modeling_faster_rcnn.register_auto()
    image_processing_faster_rcnn.register_auto()
