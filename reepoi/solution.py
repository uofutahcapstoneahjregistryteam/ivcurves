import json
import numpy as np


parameters = np.column_stack((np.arange(1, 33), 1 + np.zeros((32, 6))))
header = 'Index,photocurrent,saturation_current,resistance_series,resistance_shunt,n,cells_in_series'

for name in ['case1.csv', 'case2.csv']:
    np.savetxt(name, parameters, delimiter=',', header=header, comments='')

