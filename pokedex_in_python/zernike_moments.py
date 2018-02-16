import mahotas


class ZernikeMoments(object):
	"""docstring for ZernikeMoments"""

	# We need to play around with radius to determine the exact value that is useful for the application
	# this is used to calculate the moments
	# start with 20's.
	def __init__(self, radius):
		self.radius = radius

	def describe(self, image):
		# return the zernike moments for the image.
		return mahotas.features.zernike_moments(image, self.radius)
