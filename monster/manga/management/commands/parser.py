import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import json
import re
import options

def extract_text_between_braces(input_text:str):
    input_text = input_text.replace('\n', '')
    pattern = r"\{(.+)\}"
    match = re.search(pattern, input_text)

    if match:
        return json.loads('{'+match.group(1).strip()+'}')
    else:
        return None
    
    
async def get_json_from_url(url:str):
    browser = await launch(headless=True)
    page = await browser.newPage()

    await stealth(page) 

    await page.goto(url)

    content = await page.content()
    json_data = extract_text_between_braces(content)
    if json_data is not None:
        print(json.dumps(json_data, indent=4, ensure_ascii=False))
    
    await browser.close()
        
        
def main():
    return asyncio.get_event_loop().run_until_complete(get_json_from_url('https://mangalib.me/api/v2/comments?type=chapter&post_id=86908&order=best&page=1&chapterPage=1&user_id=425502'))
    
if __name__ == '__main__':       
    print(main())
    print(options.params)
    #    await page.screenshot({"path": "images/python.png", 'fullPage':True})

