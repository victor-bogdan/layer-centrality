from uunet.multinet import data
from utils.data_helper import draw_layers

DATASET_NAME = "aucs"

multilayered_network = data(DATASET_NAME)

draw_layers("aucs", multilayered_network, True)
