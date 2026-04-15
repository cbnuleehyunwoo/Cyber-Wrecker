import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_article_summary(url):
    """
    기사 본문을 가져와서 요약합니다.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 다음/네이버 공통 본문 선택자
        content = soup.select_one('#dic_area, #articleBodyContents, #article_body, .article_view, .news_con, #newsEndContents, .dm-article-content')
        if content:
            for s in content(['script', 'style']):
                s.decompose()
            text = content.get_text(separator=' ', strip=True)
            return text[:120] + "..." if len(text) > 120 else text
        return "본문 요약을 가져올 수 없는 기사입니다."
    except Exception:
        return "요약 실패"

def get_news(keyword=None):
    """
    키워드가 있으면 Daum 뉴스 검색을, 없으면 Naver 랭킹 뉴스를 가져옵니다.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    news_items = []

    if keyword:
        # 1. 키워드 검색 (Daum News Search - 차단이 적고 정확함)
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://search.daum.net/search?w=news&q={encoded_keyword}&sort=recency"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Daum 뉴스 검색 결과 리스트 선택자
            items = soup.select('ul#dnsColl > li, ul#newsColl > li')
            
            for item in items:
                if len(news_items) >= 5:
                    break
                
                title_tag = item.select_one('.tit_main, .atc_tit a, .item-title a')
                if not title_tag:
                    title_tag = item.find('a', class_=lambda x: x and 'tit' in x)
                
                if title_tag:
                    link = title_tag['href']
                    title = title_tag.get_text(strip=True)
                    # 언론사 정보
                    press_tag = item.select_one('.info_item, .ext_info, .f_nb')
                    press = press_tag.get_text(strip=True) if press_tag else "뉴스"
                    
                    news_items.append({
                        "title": title,
                        "link": link,
                        "press": press,
                        "summary": get_article_summary(link)
                    })
        except Exception as e:
            print(f"Daum 검색 중 오류: {e}")
            
    # 검색 결과가 없거나 키워드가 없을 때 Naver 랭킹 뉴스 사용
    if not news_items:
        try:
            naver_base_url = "https://news.naver.com"
            naver_url = f"{naver_base_url}/main/ranking/popularDay.naver"
            response = requests.get(naver_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            ranking_boxes = soup.select('.rankingnews_box')
            for box in ranking_boxes[:3]: 
                press_name = box.select_one('.rankingnews_name').text.strip()
                items = box.select('.rankingnews_list li')
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
                            "press": f"[Naver] {press_name}",
                            "summary": get_article_summary(link)
                        })
        except Exception as e:
            print(f"Naver 랭킹 크롤링 중 오류: {e}")

    return news_items[:5]

if __name__ == "__main__":
    k = input("검색 키워드: ")
    res = get_news(k)
    for n in res:
        print(f"[{n['press']}] {n['title']}\n{n['link']}\n")
