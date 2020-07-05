import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

def request_retry_session(retries = 3, backoff_factor = 0.3 , status_forcelist=(500, 502, 504), session = None,):
	"""requests retry

	customize requests retry method based on status code and retry time

	Arguments:
		 {[type]} -- [description]

	Keyword Arguments:
		retries {number} -- [description] (default: {3})
		backoff_factor {number} -- [description] (default: {0.3})
		status_forcelist {tuple} -- [description] (default: {(500, 502, 504)})
		session {[type]} -- [description] (default: {None})
	"""
	session = session or requests.Session()
	retry = Retry(
	              total = retries,
	              read = retries,
	              connect = retries,
	              backoff_factor = backoff_factor,
	              status_forcelist = status_forcelist,)
	adapter = HTTPAdapter(max_retries = retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	return session

t0 = time.time()
try:
	resp = request_retry_session().get('http://localhost:8080')

except Exception as e:
	print('failed: ', e.__class__.__name__)

else:
	print(resp.status_code)

finally:
	t1 = time.time()
	print(t1 - t0)