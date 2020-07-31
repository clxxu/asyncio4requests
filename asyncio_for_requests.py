import asyncio, requests, time, requests_async
itr = 200
tag = 'https://jsonplaceholder.typicode.com/todos/'
urls = []
for i in range(1, itr):
   urls.append(tag + str(i))

def synchronous(urls):
   for url in urls:
       r = requests.get(url)
       print(r.json())
      
async def asynchronous_fail(urls):
   for url in urls:
       r = await requests_async.get(url)
       print(r.json())
      
async def asynchronous(urls):
   tasks = []
   for url in urls:
       task = asyncio.create_task(requests_async.get(url))
       tasks.append(task)
   responses = await asyncio.gather(*tasks)
   for response in responses:
       print(response.json())
      
async def asynchronous_ordered(urls):
   responses = [None] * len(urls)
   tasks = []
   for i in range(len(urls)):
       url = urls[i]
       task = asyncio.create_task(fetch(url, responses, i))
       tasks.append(task)
   await asyncio.gather(*tasks)
   for response in responses:
       print(response.json())

async def fetch(url, responses, i):
   response = await requests_async.get(url)
   responses[i] = response

async def asynchronous_ordered_batched(urls):
   batch_size = 10
   responses = [None] * len(urls)
   kiterations = int(len(urls) / batch_size) + 1
   for k in range(0, kiterations):
       tasks = []
       m = min((k + 1) * batch_size, len(urls))
       for i in range(k * batch_size, m):
           url = urls[i]
           task = asyncio.create_task(fetch(url, responses, i))
           tasks.append(task)
       await asyncio.gather(*tasks)
   for response in responses:
       print(response.json())

starttime = time.time()
synchronous(urls)
print(time.time() - starttime)

starttime = time.time()
asyncio.run(asynchronous_fail(urls))
print(time.time() - starttime)

starttime = time.time()
asyncio.run(asynchronous(urls))
print(time.time() - starttime)

starttime = time.time()
asyncio.run(asynchronous_ordered(urls))
print(time.time() - starttime)

starttime = time.time()
asyncio.run(asynchronous_ordered_batched(urls))
print(time.time() - starttime)