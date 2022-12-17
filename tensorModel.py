import tensorflow as tf, os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

physical_devices = tf.config.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(physical_devices[0], True)

def loadModel():
    return tf.keras.models.load_model('MovieModel/')