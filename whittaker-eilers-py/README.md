# Whittaker-Eilers Smoothing and Interpolation
**The Whittaker-Eilers smoother is the perfect smoother.** It offers extremely quick, efficient smoothing with built-in interpolation via weights on each measurement. This package provides a sparse-matrix implementation for additional speed and memory efficiency and can handle both equally and unequally spaced measurements. This package was originally written in Rust so additional examples, tests, and benchmarks are also available in addition to it being super speedy. The API is almost identical.

---

```bash
pip install whittaker-eilers
```

## Usage
To start smoothing and interpolating data, create a reusable WhittakerSmoother class. You'll only need to recreate this class if the length or sampling rate of your data changes.

### Equally spaced data
This is the fastest smoothing option. It smooths equally spaced y measurements using two tunable parameters, `lambda` (2e4) and the smoother `order` (2). The larger the lambda, the smoother the data.
```python
from whittaker_eilers import WhittakerSmoother

data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]

whittaker_smoother = WhittakerSmoother(lmbda=2e4, order=2, data_length = len(data_to_smooth))

smoothed_data = whittaker_smoother.smooth(data_to_smooth)

print("Smoothed data: {}".format(smoothed_data))
```



### Non-equally spaced data
If you wish to smooth unequally spaced data, you need to provide an `x_input` with the sample times/positions. 
```python
from whittaker_eilers import WhittakerSmoother

x_input = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]

whittaker_smoother = WhittakerSmoother(
    lmbda=2e4, order=2, data_length=len(data_to_smooth), x_input=x_input
)

smoothed_data = whittaker_smoother.smooth(data_to_smooth)

print("Smoothed non-equally spaced data: {}".format(smoothed_data))


```

### Weighted data & Interpolation
Each measurement can then be weighted to trust some measurements more than others. Setting `weights` to 0 for measurements will lead to interpolation. 
```python
from whittaker_eilers import WhittakerSmoother

x_input = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
weights = [1.0] * len(x_input)
weights[5] = 0.0

whittaker_smoother = WhittakerSmoother(
    lmbda=2e4,
    order=2,
    data_length=len(data_to_smooth),
    x_input=x_input,
    weights=weights,
)

smoothed_data = whittaker_smoother.smooth(data_to_smooth)

print("Smoothed and interpolated weighted data: {}".format(smoothed_data))

```
You can use these methods in combination with each other for instance, interpolating measurements without providing an x input. For more advanced examples of usage take a look at the examples, tests, and benches in the [Github](https://github.com/AnBowell/whittaker-eilers) repository. Here's an image of some smoothed data from an example:

<img src="/examples/images/smoothed_data.png" alt="Time-series smoothed by Whittaker-Eilers method" width="800" />

### Other methods
```python
from whittaker_eilers import WhittakerSmoother
x_input = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
weights = [1.0] * len(x_input)
weights[5] = 0.0

whittaker_smoother = WhittakerSmoother(
    lmbda=2e4,
    order=2,
    data_length=len(data_to_smooth),
    x_input=x_input,
    weights=weights,
)

whittaker_smoother.get_order()
whittaker_smoother.get_lambda()
whittaker_smoother.get_data_length()
whittaker_smoother.update_weights([0.5] * len(x_input))
whittaker_smoother.update_order(3)
whittaker_smoother.update_lambda(4321.0)
```

## Future Features
- Cross validation options to find optimal lambda.
- Scatter plot smoothing
- Generic typing

## References
The algorithm implemented here mirrors a 2003 implementation by Paul H. C. Eilers in Matlab. I've included scripts and data from the original paper in the tests for this package. The original paper and code can be found here:

[A Perfect Smoother](https://pubs.acs.org/doi/10.1021/ac034173t)
Paul H. C. Eilers
Analytical Chemistry 2003 75 (14), 3631-3636
DOI: 10.1021/ac034173t
