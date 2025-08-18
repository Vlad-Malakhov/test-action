import numpy as np

try:
    condition1 = np.all(zebra.white_tensor.black_tensor[:, -1] >= 240)
    condition2 = np.all(b.c.d[:, :, :, :-1] > 240)
except AttributeError as e:
    raise AttributeError("Ensure zebra.white_tensor.black_tensor and b.c.d are numpy arrays with appropriate dimensions.") from e
except IndexError as e:
    raise IndexError("Check dimensions of zebra.white_tensor.black_tensor and b.c.d. Ensure indices are valid.") from e

if condition1 or condition2:

