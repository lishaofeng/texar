"""
Conv1D discriminator.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from txtgen import HParams
from txtgen.modules.encoders.encoder_base import EncoderBase
from txtgen.core.layers import get_layer


class CNN(ModuleBase):
  """CNN for text."""
  def __init__(self, hparams=None):
    ModuleBase.__init__(self, hparams)

    self._conv_layers = []
    for k in self._hparams.kernel_sizes:
      activation = lambda x : tf.nn.leaky_relu(x, alpha=0.01)
      conv_layer = tf.layers.Conv1D(self._hparams.num_filter, k,
                                    activation=activation)
      self._conv_layers.append(conv_layer)

    self._dropout_layer = tf.layers.Dropout(rate=self._hparams.drop_ratio)
    self._proj_layer = tf.layers.Dense(1)

  @staticmethod
  def default_hparams():
    return {
      "name": "cnn"
      "kernel_sizes": [3, 4, 5],
      "num_filter": 128,
      "drop_ratio": 0.5
    }


  def _build(self, inputs):
    drop_ratio = self._hparams.drop_ratio
    drop_ratio = 1 - utils.switch_dropout(1 - drop_ratio)
    pooled_outputs = []
    for conv_layer in self._conv_layers:
      h = conv_layer(inputs)
      # pooling after conv
      h = tf.reduce_max(h, axis=1)
      h = tf.reshape(h, [-1, h.get_shape().as_list()[-1]])
      pooled_outputs.append(h)

    outputs = tf.concat(pooled_outputs, 1)
    outputs = self._dropout_layer(outputs)

    logits = proj_layer(outputs)

    self._add_internal_trainable_variables()
    self._built = True

    return logits