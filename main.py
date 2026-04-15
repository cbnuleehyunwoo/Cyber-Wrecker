import json
import os
from crawler import get_news
from kakao_auth import KakaoAuth
from kakao_msg import send_to_me

TOKEN_FILE = "kakao_token.json"

def main():
    # 1. Load authentication information
    REST_API_KEY = "51ffe34ebcb77969698dfcf06b97d267"
    REDIRECT_URI = "https://www.google.com/"
    
    auth = KakaoAuth(REST_API_KEY, REDIRECT_URI)
    
    if not os.path.exists(TOKEN_FILE):
        print("kakao_token.json 파일이 없습니다. kakao_auth.py를 먼저 실행하세요.")
        return

    # 2. Get Access Token
    access_token = auth.get_access_token()
    if not access_token:
        print("Access Token을 가져오는 데 실패했습니다.")
        return

    # 3. User Input for Topic
    print("="*30)
    print(" 뉴스 봇 서비스를 시작합니다.")
    print("="*30)
    keyword = input("검색할 뉴스 키워드를 입력하세요 (엔터 시 '조회수 높은 뉴스' 전송): ").strip()
    
    header_title = "조회수 높은 최근 뉴스"
    if keyword:
        header_title = f"'{keyword}' 관련 뉴스"

    # 4. Crawl News with Summary
    print(f"\n[{header_title}] 뉴스를 크롤링 및 요약 중입니다. 잠시만 기다려 주세요...")
    news_items = get_news(keyword if keyword else None)
    
    if not news_items:
        print("관련 뉴스를 찾을 수 없습니다.")
        return

    # 5. Send to KakaoTalk
    print(f"{len(news_items)}개의 뉴스를 요약하여 카카오톡으로 전송합니다.")
    send_to_me(access_token, news_items, header_title=header_title)

if __name__ == "__main__":
    main()
