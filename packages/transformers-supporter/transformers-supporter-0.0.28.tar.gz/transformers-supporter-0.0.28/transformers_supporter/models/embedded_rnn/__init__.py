from . import configuration_embedded_rnn
from . import modeling_embedded_rnn
from . import feature_extraction_embedded_rnn

def register_auto():
    configuration_embedded_rnn.register_auto()
    modeling_embedded_rnn.register_auto()
    feature_extraction_embedded_rnn.register_auto()
