import requests
import shutil
from PIL import Image
from io import StringIO

### response.raw by default will not decode compressed responses
## use less memory
r = requests.get(url, stream = True)
if r.status_code == 200:
	with open('test.jpg', 'wb') as f:
		r.raw.decode_content = True
		shutil.copyfileobj(r.raw, f)

	## way 2
	#with open(path, 'wb') as f:
	#	for chunk in r.iter_content(1024):
	#		f.write(chunk)


## faster way
def download_iamge(url, image_name):
	r = requests.get(url, stream = True)
	if r.status_code == 200:
		i = Image.open(StringIO(r.content))
		# i = Image.open(r.raw)
		i.save(image_name)


# import wget
# wget.download(url, out = out_filepath)

# import urllib
# urllib.urlretrieve(url, 'test.jpg')
