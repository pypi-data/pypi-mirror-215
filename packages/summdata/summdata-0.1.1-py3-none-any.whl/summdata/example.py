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

