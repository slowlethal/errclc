
import numpy as np
import pytest
from fehlerrechnung_funktionen import roundwitherror, list_error_calc


examples = [((1.05, 0.19343), (1.05, 0.2)),
            ((123456, 100), (123460, 100)),
            ((0.002342342, 0.000054343), (0.00234, 0.00006)),
            ((2.3, 1), (2.3, 1)),
            ((13.7, 5.6), (14, 6))]

@pytest.mark.parametrize("example", examples)
def test_pre(example):
    x, err = example[0]
    x_err_calc = roundwitherror(x, err)
    x_err_read = (example[1])
    assert x_err_read == x_err_calc

values = (({"a":(4, 0.1), "b":(5, 1)}, "a/b", (0.8, 0.18)),
          ({"a":(4, 0.1), "b":(5, 1)}, "a+b", (9, 1.1)),
          ({"a":(4, 0.1), "b":(5, 1)}, "a**b", (1024, 1547.565426)),
          ({"a":(4, 0.1), "b":(5, 1)}, "a*b", (20, 4.5)))


@pytest.mark.parametrize("value", values)
def test_list_error_calc(value):
    assert np.all((np.array(list_error_calc(*value[:-1])) -
                   np.array(value[2]))/np.array(value[2])) < 1e-4
