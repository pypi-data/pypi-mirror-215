from . import configuration_pretrained_embedded_rnn
from . import modeling_pretrained_embedded_rnn

def register_auto():
    configuration_pretrained_embedded_rnn.register_auto()
    modeling_pretrained_embedded_rnn.register_auto()
