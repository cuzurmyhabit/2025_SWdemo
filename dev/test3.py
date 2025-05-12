import os

if True:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras

mobilenet_model = keras.applications.mobilenet.MobileNet(weights='imagenet')
conv_preds_layer_output = mobilenet_model.get_layer(name='conv_preds').output
rerouted_model = keras.Model(inputs=mobilenet_model.inputs, outputs=conv_preds_layer_output, name='')

