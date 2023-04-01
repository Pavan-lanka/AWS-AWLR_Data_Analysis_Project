import math
import BaseException

class NoobError(BaseException):
	pass

if __name__ == '__main__':
	"""
	Always use proper docstrings. Check the Guidelines on Confluence.
	"""
	try:
		if 2 + 2 == 5:
			raise NoobError
	except Exception as e:
		print(e)
	finally:
		print('Write it. Code it. Shoot it. Publish it. Crochet it. Sauté it. Whatever. MAKE. - J. Wheedon') 