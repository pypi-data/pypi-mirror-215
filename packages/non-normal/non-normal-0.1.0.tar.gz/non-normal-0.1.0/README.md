# non-normal
Generate non-normal distributions with given a mean, variance, skewness and kurtosis

### Installation

Installs cleanly with a single invocation of the standard Python package tool:

```
$ pip install non-normal
```

### Usage

```
from non_normal import fleishman

# Input parameters for non-normal field
mean = 0
var = 1
skew = 2
ekurt = 6
size = 2**20

# Create an instance of the Fleishman class
ff = fleishman.Fleishman(mean=mean, var=var, skew=skew, ekurt=ekurt, size=size)

# Generate the field
ff.gen_field()
non_normal_data = ff.field

# Measure the stats of the generated samples
ff.field_stats

>>> {
'mean': 0.00029969955054414245, 
'var': 1.0019932680714605, 
'skew': 2.011601878030434, 
'ekurt': 6.139570248892955
}
```
