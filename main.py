# http://dushu.baidu.com/api/pc/getCatalog?data={book_id:4295084047}

# http://dushu.baidu.com/api/pc/getChapterContent?data={book_id:4295084047,cid:4295084047|150705,need_bookinfo:1}

# http://dushu.baidu.com/api/pc/getSearch?data={"word":"","pageNum":1}
import json

import aiofiles
import requests
import asyncio
import aiohttp


# 1.拿到所有章节的id和名称:getCatalog
# 2.拿到章节内容并下载

async def download(bid, cid, title):
    data = {
        "book_id": bid,
        "cid": f"{bid}|{cid}",
        "need_bookinfo": 1,
    }
    data = json.dumps(data)
    detail_url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(detail_url) as resp:
            res = await resp.json()
            async with aiofiles.open(f"{title}.txt", mode="w", encoding="utf-8") as f:
                await f.write(res['data']['novel']['content'])


async def getContent(url):
    res = requests.get(url).json()
    tasks = []
    for item in res['data']['novel']['items']:
        title = item['title']
        cid = item['cid']
        tasks.append(asyncio.create_task(download(book_id, cid, title)))
    await asyncio.wait(tasks)


# 根据搜索api获得书的id
def getBookId(name):
    search_url = 'http://dushu.baidu.com/api/pc/getSearch?data={"word":"' + name + '","pageNum":1}'
    return requests.get(search_url).json()['data']['list'][0]['book_id']


if __name__ == '__main__':
    book_name = input("请输入想看的书名：")
    book_id = getBookId(book_name)
    index_url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
    asyncio.run(getContent(index_url))
