import math
import matplotlib.pyplot as plt
from collections import Counter
from .SummaryStatistics import SummaryStatistics


class Continuous(SummaryStatistics):
	

	def __init__(self, mu =0, sigma =1):
		SummaryStatistics.__init__(self, mu, sigma)

	def show_length(self):
		""" This function returns the length of the data set

		Args: 
			None
		Returns: 
			float : count elements of the list

		"""

		return len(self.data)


	def calculate_mean(self):
	
		"""Function to calculate the mean of the data set.
		
		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
					
		avg = 1.0 * sum(self.data) / len(self.data)
		
		self.mean = avg
		
		return self.mean



	def calculate_median(self):
	
		"""Function to calculate the median of the data set.
		
		Args: 
			None
		
		Returns: 
			float: median of the data set
	
		"""
					
		# sort the data set
		sorted_data = sorted(self.data)
		
		# get the length of the dataset using our function show length
		n = self.show_length()
		# find the middle point of the data
		midpoint = (n - 1) // 2

		#if the dataset is odd -> return middle value
		if midpoint % 2: # we use the modulus to check if the number is odd
			median = sorted_data[midpoint]

		# if dataset is even, calculate the mean between the two middle values
		else: 
			median = (sorted_data[midpoint] + sorted_data[midpoint + 1]) / 2.0

		self.median = median
		return self.median


	def calculate_mode(self):
	
		"""Function to calculate the mode of the data.
		
		Args: 
			None
		
		Returns: 
			float: mode of the data presented as a list
	
		"""
					
		counter = 0
		num = self.data[0]

		for i in self.data:
			current_frequency = self.data.count(i)
			if (current_frequency > counter):
				counter = current_frequency
				num = i

		self.mode = num

		return self.mode



	def calculate_stdev(self, sample=True):

		"""Function to calculate the standard deviation of the data set.
		
		Args: 
			sample (bool): whether the data represents a sample or population
		
		Returns: 
			float: standard deviation of the data set
	
		"""

		if sample:
			n = len(self.data) - 1
		else:
			n = len(self.data)
	
		mean = self.calculate_mean()
	
		sigma = 0
	
		for d in self.data:
			sigma += (d - mean) ** 2
		
		sigma = math.sqrt(sigma / n)
	
		self.stdev = sigma
		
		return self.stdev