# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random
from settings import PROXIES
# Start your middleware class
class ProxyMiddleware(object):
	def process_request(self, request, spider):
		proxy = random.choice(PROXIES)
		request.meta['proxy'] = "http://%s" % proxy['ip_port']
		#print '************using proxy:'+proxy['ip_port']
