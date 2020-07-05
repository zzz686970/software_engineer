import asyncio
import aiohttp
import aysnc_timeout
import uuid

async def get_url(url, session):
	file_name = str(uuid.uuid4())
	async with aysnc_timeout.timeout(120):
		async with session.get(url) as response:
			with open(file_name, 'wb') as fd:
				async for data in response.content.iter_chunked(1024):
					fd.write(data)

	return 'downloaded' + file_name

async def main(urls):
	async with aiohttp.ClientSession() as session:
		tasks = [get_url(url, session) for url in urls]
		return await async asyncio.gather(*tasks)

urls = [url1, url2, url3]
loop = asyncio.get_event_loop()
results = loop.run_until_complete(main(urls))


def download_in_chunks(url):

	resp = requests.get(url, stream=True)
	total_length = int(r.headers.get('content-length', 0))
	pbar = tqdm(
		total=total_length, initial=0,
		unit='B', unit_scale=True, desc=url.split('/')[-1])
	with open('test.txt','wb') as f:
		for chunk in resp.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				pbar.update(1024)

	pbar.close()
	if total_length != 0 and pbar.n != total_length:
		print("ERROR, something went wrong")


def down_multiple_files(url):
	path, url = url
	r = requests.get(url, stream=True)
	with open(path, 'wb') as f:
		for ch in r:
			f.write(ch)

from multiprocessing.pool import ThreadPool

if __name__ == '__main__':
	ThreadPool(9).imap_unordered(down_multiple_files, urls)