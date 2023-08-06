from . import configuration_rnn
from . import modeling_rnn
from . import feature_extraction_rnn

def register_auto():
    configuration_rnn.register_auto()
    modeling_rnn.register_auto()
    feature_extraction_rnn.register_auto()
