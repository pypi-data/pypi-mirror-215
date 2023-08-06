from NeuroGraph import utils
import numpy as np

fc = np.load("NeuroGraph/data/fc.npy")
print(fc.shape) 
data = utils.construct_data(fc, 1)
print(data)