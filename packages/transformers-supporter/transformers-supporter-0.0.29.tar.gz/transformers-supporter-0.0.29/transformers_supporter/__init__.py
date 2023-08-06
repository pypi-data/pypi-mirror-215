from . import models
from . import pipelines

#

'''
from .models.ann import configuration_ann
from .models.ann import feature_extraction_ann
from .models.ann import modeling_ann

from .models.cnn import configuration_cnn
from .models.cnn import modeling_cnn
from .models.cnn import image_processing_cnn

from .models.custom_bert import configuration_custom_bert
from .models.custom_bert import modeling_custom_bert

from .models.embedded_1dcnn import configuration_embedded_1dcnn
from .models.embedded_1dcnn import modeling_embedded_1dcnn

from .models.embedded_rnn import configuration_embedded_rnn
from .models.embedded_rnn import modeling_embedded_rnn
from .models.embedded_rnn import feature_extraction_embedded_rnn

from .models.pretrained_embedded_rnn import configuration_pretrained_embedded_rnn
from .models.pretrained_embedded_rnn import modeling_pretrained_embedded_rnn

from .models.faster_rcnn import configuration_faster_rcnn
from .models.faster_rcnn import modeling_faster_rcnn
from .models.faster_rcnn import image_processing_faster_rcnn

from .models.rnn import configuration_rnn
from .models.rnn import modeling_rnn
from .models.rnn import feature_extraction_rnn

def register_auto():
    configuration_ann.register_auto()
    modeling_ann.register_auto()
    feature_extraction_ann.register_auto()

    configuration_cnn.register_auto()
    modeling_cnn.register_auto()
    image_processing_cnn.register_auto()

    configuration_custom_bert.register_auto()
    modeling_custom_bert.register_auto()

    configuration_embedded_1dcnn.register_auto()
    modeling_embedded_1dcnn.register_auto()

    configuration_embedded_rnn.register_auto()
    modeling_embedded_rnn.register_auto()
    feature_extraction_embedded_rnn.register_auto()

    configuration_pretrained_embedded_rnn.register_auto()
    modeling_pretrained_embedded_rnn.register_auto()

    configuration_faster_rcnn.register_auto()
    modeling_faster_rcnn.register_auto()
    image_processing_faster_rcnn.register_auto()

    configuration_rnn.register_auto()
    modeling_rnn.register_auto()
    feature_extraction_rnn.register_auto()
    
from .pipelines import tabular_regression
from .pipelines import tabular_classification
from .pipelines import image_classification
from .pipelines import fixed_length_translation

def register_pipeline():
    tabular_regression.register_pipeline()
    tabular_classification.register_pipeline()
    image_classification.register_pipeline()
    fixed_length_translation.register_pipeline()
'''
