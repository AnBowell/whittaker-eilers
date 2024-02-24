# Whittaker-Eilers Smoothing and Interpolation
**The Whittaker-Eilers smoother is the perfect smoother.** It offers extremely quick, efficient smoothing with built-in interpolation via weights on each measurement. This crate provides a sparse-matrix implementation for additional speed and memory efficiency and can handle both equally and unequally spaced measurements.

---

```toml
[dependencies]
whittaker-eilers = "0.1.3"
```

## Usage
To start smoothing and interpolating data, create a reusable WhittakerSmoother struct via the `new` function. You'll only need to recreate this struct if the length or sampling rate of your data changes.

### Equally spaced data
This is the fastest smoothing option. It smooths equally spaced y measurements using two tunable parameters, `lambda` (2e4) and the smoother `order` (2). The larger the lambda, the smoother the data.
```rust
use whittaker_eilers::WhittakerSmoother;

let data_to_smooth = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0];

let whittaker_smoother = 
            WhittakerSmoother::new(2e4, 2, data_to_smooth.len(), None, None)
            .unwrap();

let smoothed_data = whittaker_smoother.smooth(&data_to_smooth).unwrap();
println!("Smoothed data: {:?}", smoothed_data);
```



### Non-equally spaced data
If you wish to smooth unequally spaced data, you need to provide an `x_input` with the sample times/positions. 
```rust
use whittaker_eilers::WhittakerSmoother;

let x_input = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0];
let data_to_smooth = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0];

let whittaker_smoother = 
            WhittakerSmoother::new(2e4, 2, data_to_smooth.len(), Some(&x_input), None)
            .unwrap();

let smoothed_data = whittaker_smoother.smooth(&data_to_smooth).unwrap();

println!("Smoothed data: {:?}", smoothed_data);

```

### Weighted data & Interpolation
Each measurement can then be weighted to trust some measurements more than others. Setting `weights` to 0 for measurements will lead to interpolation. 
```rust
use whittaker_eilers::WhittakerSmoother;

let x_input = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0];
let data_to_smooth = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0];
let mut weights = vec![1.0; x_input.len()];
weights[5] = 0.0;

let whittaker_smoother =
            WhittakerSmoother::new(2e4, 2, data_to_smooth.len(), Some(&x_input), Some(&weights))
            .unwrap();

let smoothed_data = whittaker_smoother.smooth(&data_to_smooth).unwrap();

println!("Smoothed data: {:?}", smoothed_data);

```


### Smoothing with cross validation
With this package, you can also calculate the cross validation error alongside the smoothed series. This shouldn't really be used in production where speed is necessary though!


```rust 
use whittaker_eilers::WhittakerSmoother;

let x_input = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0 ,11.0, 12.0, 13.0];
let data_to_smooth = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0, 11.0, 12.0, 13.0];

let whittaker_smoother = 
            WhittakerSmoother::new(2e4, 2, data_to_smooth.len(), Some(&x_input), None)
            .unwrap();

let smoothed_and_cross_validated = whittaker_smoother.smooth_and_cross_validate(&data_to_smooth).unwrap();

println!("Result: {:?}", smoothed_and_cross_validated);
```

### Automatic smoothing
Smoothing data requires a choice of Lambda. This can be done using visual inspection or by finding the lambda
which results in the lowest cross validation error. The `smooth_optimal` function runs the smoother for a variety of lambdas and returns the results with the ability to retrieve the optimal one.


```rust 
use whittaker_eilers::WhittakerSmoother;

let x_input = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0 ,11.0, 12.0, 13.0];
let data_to_smooth = vec![1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0, 11.0, 12.0, 13.0];

let mut whittaker_smoother = 
            WhittakerSmoother::new(2e4, 2, data_to_smooth.len(), Some(&x_input), None)
            .unwrap();

let results = whittaker_smoother.smooth_optimal(&data_to_smooth,  true).unwrap();

println!("Result: {:?}", results);

println!("Optimal result: {:?}", results.get_optimal());

```


---


You can use these methods in combination with each other for instance, interpolating measurements without providing an x input. For more advanced examples of usage take a look at the examples, tests, and benches in the [Github](https://github.com/AnBowell/whittaker-eilers) repository. Here's an image of some smoothed data from an example:

<img src="/examples/images/smoothed_data.png" alt="Time-series smoothed by Whittaker-Eilers method" width="800" />


## Further Reading
If you'd like to see a more detailed run through of the library, check out this [Medium post](https://medium.com/towards-data-science/the-perfect-way-to-smooth-your-noisy-data-4f3fe6b44440). Within it, I run through examples and benchmarks against other smoothing methods.

## Future Features
- Scatter plot smoothing
- Generic typing




## References
The algorithm implemented here mirrors a 2003 implementation by Paul H. C. Eilers in Matlab. I've included scripts and data from the original paper in the tests for this crate. The original paper and code can be found here:

[A Perfect Smoother](https://pubs.acs.org/doi/10.1021/ac034173t)
Paul H. C. Eilers
Analytical Chemistry 2003 75 (14), 3631-3636
DOI: 10.1021/ac034173t
