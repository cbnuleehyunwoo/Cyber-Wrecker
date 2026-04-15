import requests
from bs4 import BeautifulSoup

def get_news_rankings():
    """
    Scrapes top news from Naver and Daum.
    Returns a list of dictionaries with 'title', 'link', and 'press'.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    news_items = []

    # 1. Naver News Ranking (Popular)
    try:
        naver_base_url = "https://news.naver.com"
        naver_url = f"{naver_base_url}/main/ranking/popularDay.naver"
        response = requests.get(naver_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ranking_boxes = soup.select('.rankingnews_box')
        # 언론사별 박스에서 더 많은 기사를 가져옵니다.
        for box in ranking_boxes[:3]: 
            press_name = box.select_one('.rankingnews_name').text.strip()
            items = box.select('.rankingnews_list li')
            # 각 언론사 박스에서 상위 2개씩 가져옵니다. (3박스 * 2개 = 최대 6개)
            for item in items[:2]: 
                title_tag = item.select_one('.list_title')
                link_tag = item.select_one('a')
                if title_tag and link_tag:
                    link = link_tag['href']
                    if link.startswith('/'):
                        link = naver_base_url + link
                    news_items.append({
                        "title": title_tag.text.strip(),
                        "link": link,
                        "press": f"[Naver] {press_name}"
                    })
    except Exception as e:
        print(f"Error scraping Naver: {e}")

    # 2. Daum News Ranking
    try:
        daum_url = "https://news.daum.net/ranking/popular"
        response = requests.get(daum_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Daum의 여러 구조에 대응하도록 선택자 보강
        items = soup.select('.list_news2 li, .item_ranking, .list_ranking li')
            
        for item in items[:3]:
            title_tag = item.select_one('.link_txt, .tit_main a, .link_txt')
            info_tag = item.select_one('.info_news, .txt_info')
            if title_tag:
                link = title_tag['href']
                news_items.append({
                    "title": title_tag.text.strip(),
                    "link": link,
                    "press": f"[Daum] {info_tag.text.strip() if info_tag else 'Daum'}"
                })
    except Exception as e:
        print(f"Error scraping Daum: {e}")

    # 최종적으로 중복 제거 및 5개만 반환
    unique_news = []
    seen_links = set()
    for item in news_items:
        if item['link'] not in seen_links:
            unique_news.append(item)
            seen_links.add(item['link'])

    return unique_news[:5]

if __name__ == "__main__":
    ranks = get_news_rankings()
    for i, news in enumerate(ranks, 1):
        print(f"{i}. [{news['press']}] {news['title']} - {news['link']}")
