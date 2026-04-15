import requests
import urllib.parse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import time
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
}

def get_real_url(google_url):
    """구글 RSS의 암호화된 주소를 실제 기사 주소로 변환합니다."""
    try:
        # 구글 리다이렉션 페이지에 접속
        session = requests.Session()
        resp = session.get(google_url, headers=HEADERS, timeout=10, allow_redirects=True)
        
        # 1. 자동 리다이렉트된 URL 확인
        final_url = resp.url
        
        # 2. 여전히 구글 주소라면 페이지 내부의 meta refresh 확인
        if "google.com" in final_url:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # <meta content="0;url=https://..." http-equiv="refresh"> 형태 추출
            meta = soup.find('meta', attrs={'http-equiv': 'refresh'})
            if meta:
                target = re.search(r'url=(.*)', meta['content'])
                if target:
                    return target.group(1)
        return final_url
    except:
        return google_url

def get_article_summary(url, rss_snippet=""):
    """기사 본문을 추출하며, 실패 시 RSS에서 제공하는 기본 스니펫을 반환합니다."""
    try:
        real_url = get_real_url(url)
        
        # 실제 기사 주소로 본문 긁기 시도
        resp = requests.get(real_url, headers=HEADERS, timeout=8)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 주요 언론사별 본문 태그 후보
        selectors = ['#dic_area', '#newsct_article', '#articleBodyContents', '.article_view', 'article', '#article_body']
        content_text = ""
        
        for s in selectors:
            content = soup.select_one(s)
            if content:
                # 불필요한 태그 제거
                for t in content(['script', 'style', 'header', 'footer']): t.decompose()
                content_text = ' '.join(content.get_text(separator=' ', strip=True).split())
                break

        # 본문 추출 성공 시 (글자 수 60자 이상 기준)
        if len(content_text) > 60:
            return (content_text[:140] + "...") if len(content_text) > 140 else content_text

        # 본문 추출 실패 시 RSS에 포함된 기본 요약(Snippet) 활용
        if rss_snippet:
            # HTML 태그 제거
            clean_snippet = BeautifulSoup(rss_snippet, "html.parser").get_text()
            return f"[미리보기] {clean_snippet[:120]}..."
            
        return "본문 요약을 가져올 수 없는 기사입니다."
    except:
        return f"[미리보기] {rss_snippet[:100]}..." if rss_snippet else "요약 실패"

def search_news(keyword, count=5):
    """구글 뉴스 RSS를 가져옵니다."""
    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_kw}&hl=ko&gl=KR&ceid=KR:ko"
    
    news_items = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        root = ET.fromstring(r.content)
        items = root.findall('./channel/item')

        for item in items[:count]:
            title_full = item.findtext('title', '')
            title = title_full.rsplit(' - ', 1)[0] if ' - ' in title_full else title_full
            press = title_full.rsplit(' - ', 1)[1] if ' - ' in title_full else "알 수 없음"
            
            news_items.append({
                "title": title,
                "press": press,
                "link": item.findtext('link', ''),
                "description": item.findtext('description', '') # 요약 실패 시 대비용
            })
    except Exception as e:
        print(f"에러: {e}")
    return news_items

if __name__ == "__main__":
    query = input("검색 키워드: ").strip()
    if query:
        print(f"\n🔍 '{query}' 관련 뉴스를 분석 중입니다. 잠시만 기다려주세요...\n")
        results = search_news(query)
        
        for i, n in enumerate(results, 1):
            # 실제 요약 실행
            summary = get_article_summary(n['link'], n['description'])
            print(f"{i}. [{n['press']}] {n['title']}")
            print(f"   요약: {summary}")
            print(f"   링크: {n['link']}")
            print("-" * 60)
            time.sleep(0.8) # 차단 방지