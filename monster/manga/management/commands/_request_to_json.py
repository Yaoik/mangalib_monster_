import requests
import json

headers = {
    'authority': 'api.lib.social',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://test-front.mangalib.me',
    'pragma': 'no-cache',
    'referer': 'https://test-front.mangalib.me/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'site-id': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

params = {
    'page': '1',
    'post_id': '969339',
    'post_page': '1',
    'post_type': 'chapter',
    'sort_by': 'votes_up',
    'sort_type': 'desc',
}

response = requests.get('https://api.lib.social/api/comments', params=params, headers=headers)
jsonn = json.dumps(response.json(), indent=4, ensure_ascii=False)
print(jsonn)
with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\comments_json_api.json', 'w+', encoding='UTF-8') as f:
    f.write(json.dumps(response.json(), indent=4, ensure_ascii=False))