# This library contains a lot of functions to compare how similar two images are.
# we will specifically be using the euclidean distance, the smaller the value, the more similar they are.
from scipy.spatial import distance as dist

class Searcher(object):
	"""docstring for Searcher"""
	def __init__(self, index):
		# store the index that we will be searching over
		self.index = index

	def search(self, queryFeatures):

		results = {}

		# loop through all the key, value pairs in index
		for (k, features) in self.index.items():
			# calculate the euclidean distance between the two images
			d = dist.euclidean(features, queryFeatures)

			results[k] = d

		# sort the results, the smallest value means the most similar image
		results = sorted((v, k) for (k, v) in results.items())


		return results


