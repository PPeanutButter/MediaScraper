import json
import re
import argparse
from os import path
from HCY import HCYRequest
from HCY import build_request_from_hcy
from bs4 import BeautifulSoup, Tag


def base_path(file):
    return path.join(path.abspath(path.dirname(__file__)), file)


def search(key, proxy):
    def _get_name(_suggest):
        if _suggest["media_type"] == "tv":
            if 'name' in _suggest:
                return _suggest['name']
            else:
                return _suggest['original_name']
        else:
            if 'title' in _suggest:
                return _suggest['title']
            else:
                return _suggest['original_title']

    hcy = build_request_from_hcy(base_path('tmdb-s.hcy'))
    hcy.url = proxy + hcy.url
    hcy.params['query'] = key
    r = hcy.request().json()
    index = 0
    search_result = []
    for suggest in r['results']:
        if isinstance(suggest, dict) and suggest['media_type'] in ['movie', 'tv']:
            search_result.append(f'https://www.themoviedb.org/{suggest["media_type"]}/{suggest["id"]}')
            print(f'{index}\t{"TV-Shows" if suggest["media_type"] == "tv" else "Movie"}\t{_get_name(suggest)}')
            index += 1
    select = int(input("> "))
    save(search_result[select], proxy)


def save(url, proxy):
    print("Get info from", url, "using proxy", proxy if proxy else None)
    hcy = HCYRequest(proxy + url, 'GET', base_path('tmdb.hcy'))
    hcy.super_headers = {"accept-language": "en-US"}
    html = hcy.request().text
    post = re.search(r"/t/p/w1920_and_h800_multi_faces/(.*\.jpg)", html).group(1)
    cover = re.search(r"/t/p/w600_and_h900_bestv2/.*\.jpg", html).group(0)
    html = HCYRequest(proxy + url, 'GET', base_path('tmdb.hcy')).request().text
    selects = BeautifulSoup(html, 'html.parser').select_one('.header_poster_wrapper')
    title = selects.select_one('h2').text.strip().replace('\n', '')
    facts = [i.text.strip().replace('\n', '') for i in selects.select_one('.facts').contents if isinstance(i, Tag)]
    certification = facts[0]
    genres, runtime = facts[-2:]
    header_info = selects.select_one('.header_info')
    tagline = header_info.select_one('.tagline').text.strip().replace('\n', '') if header_info.select_one('.tagline') \
        else "暂无介绍"
    overview = header_info.select_one('.overview').text.strip().replace('\n', '')
    user_score_chart = float(selects.select_one('.user_score_chart').attrs['data-percent']).__int__()
    with open('.post', 'wb') as f:
        f.write(HCYRequest(f"{proxy}https://www.themoviedb.org/t/p/w1920_and_h1080_multi_faces/{post}", 'GET',
                           base_path('tmdb.hcy')).request().content)
        print('saving .post')
    with open('.cover', 'wb') as f:
        f.write(HCYRequest(f"{proxy}https://www.themoviedb.org{cover}", 'GET', base_path('tmdb.hcy')).request().content)
        print('saving .cover')
    with open('.info', 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict(
            title=title,
            certification=certification,
            genres=genres,
            runtime=runtime,
            tagline=tagline,
            overview=overview,
            user_score_chart=user_score_chart,
            url=url,
        ), ensure_ascii=False, indent=4))
        print('saving .info')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('param', type=str, help='pass a TMDB detail web url or just a name')
    parser.add_argument('--proxy', type=str, default='', help='http proxy that uses, e.g. http://ip:port/token/')
    args = parser.parse_args()
    if str(args.param).startswith('http'):
        save(args.param, args.proxy)
    else:
        search(args.param, args.proxy)