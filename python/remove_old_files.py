import sys, time, os

for f in os.listdir(folder):
	if os.stat(f).st_mtime < time.time() - 7 * 86400:
		if os.path.isfile(f):
			os.remove(os.path.join(foler, f))

## notice two functions
# os.path.getmtime(file)
# os.path.isfile(file)

## pathlib with arrow
from pathlib import Path
import arrow

removal_time = arrow.now().shift(hours=+5).shift(days=-7)
for item in Path(folder).glob('*'):
	if item.is_file():
		print(str(item.absolute()))
		item_time = arrow.get(item.stat().st_mtime)
		if item_time < removal_time:
			os.remove(item)

## for ftp
for file, group in ftp.mlsd('.'):
	if file.endswith('2019.csv') and group['modify'] < '20191111':
		ftp.delete(file)