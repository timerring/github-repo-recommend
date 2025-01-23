import aiohttp
import asyncio
import sys

# https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-issues-and-pull-requests
# I have tried to use asyncio.gather to request concurrently.
# But due to the github api limit, it will only return the same result.

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer <your_github_token>",
    "X-GitHub-Api-Version": "2022-11-28"
}

def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}% Complete\n')
    sys.stdout.flush()

async def fetch(session, url, params):
    async with session.get(url, headers=headers, params=params) as response:
        return await response.json()

async def main():
    page = 1
    url_list = []
    async with aiohttp.ClientSession() as session:
        params = {
            "q": "【开源自荐】",
            "page": page,
            "per_page": 100
        }

        response_data = await fetch(session, "https://api.github.com/search/issues", params)

        if response_data:
            # print(response_data)
            total_count = response_data['total_count']
            total_pages = (total_count // 100) + (1 if total_count % 100 > 0 else 0)
            # Only the first 1000 search results are available
            page_permit = total_pages if total_pages < 10 else 10
            print(page_permit)
            for page in range(1, page_permit + 1):
                print_progress_bar(page, page_permit)
                params["page"] = page
                response_data = await fetch(session, "https://api.github.com/search/issues", params)
                for item in response_data['items']:
                    url_list.append(item['url'].split('/issues/', 1)[0])
            
            url_list = list(set(url_list))
            with open('url_list.txt', 'a') as f:
                f.write('\n'.join(url_list))
            for url in url_list:
                print(url)
        else:
            print(f"request failed")

asyncio.run(main())
