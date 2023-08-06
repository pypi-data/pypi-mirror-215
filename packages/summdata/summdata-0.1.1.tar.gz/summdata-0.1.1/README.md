# Summdata
## Description
summdata is a Python package that provides summary statistics from a list of numbers stored in a text file. With summdata, you can easily compute various statistics, including the number of values, mean, median, mode, and standard deviation of your data.

summdata has two modules, `SummaryStatistics.py` and `SummaryContinuous.py`. The former sets up the data set and allows to read the txt file, and the second module contains the fonctions to calculate summary statistics based on continuous data. I created these two modules to add on other features such as treating categorical data later on.

## Installation
To install Summdata, go to the folder (summdata/) using the Terminal and run the following


```
pip install .

```

## Usage
summdata creates a class (Continuous()) from which you can read a txt file (/numbers.txt as file example), and calculate:

- the number of values: `.show_length()`
- the mean: `.calculate_mean()`
- the median: `.calculate_median()`
- the mode: `.calculate_mode()`
- the standard deviation: `.calculate_stdev()`




## Example
You can run `example.py`, which provides example of calculations you can do.

```python
from summdata import Continuous

# instantiate a class called stat
stat = Continuous()

#read txt file with numbers 
stat.read_data_file("numbers.txt")

# show number of values 
stat.show_length()

#calculate mean
stat.calculate_mean()

#calculate median
stat.calculate_median()

#calculate mode(s)
stat.calculate_mode()

#calculate standard deviation
stat.calculate_stdev()

```

## Versions

### 0.1.1

- Fixed `calculate_mode()`

## Progress

This package will be progressively updated to add the additional features:
- provide a summary of all calculation in one function.
- calculating variance
- provide a distribution plot of the data
- provide summary statistics of categorical data



## License
This project is licensed under the MIT License - see the LICENSE file for details.
