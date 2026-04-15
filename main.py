import json
import os
import time
from crawler import search_news, get_article_summary
from kakao_auth import KakaoAuth
from kakao_msg import send_to_me
from dotenv import load_dotenv

TOKEN_FILE = "kakao_token.json"

def main():
    load_dotenv()
    # 1. Load authentication information
    REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    
    if not REST_API_KEY or not REDIRECT_URI:
        print(".env 파일에 KAKAO_REST_API_KEY와 KAKAO_REDIRECT_URI를 설정해주세요.")
        return
        
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
    keyword = input("검색할 뉴스 키워드를 입력하세요 (엔터 시 '최신 뉴스' 전송): ").strip()
    
    header_title = "오늘의 주요 뉴스"
    search_query = keyword if keyword else "최신 뉴스"
    if keyword:
        header_title = f"'{keyword}' 관련 뉴스"

    # 4. Search and Summarize News
    print(f"\n[{header_title}] 뉴스를 분석 중입니다. 잠시만 기다려 주세요...")
    # crawler.py의 search_news 내부에서 이미 요약과 URL 변환을 수행함
    news_items = search_news(search_query)
    
    if not news_items:
        print("관련 뉴스를 찾을 수 없습니다.")
        return

    # 5. Send to KakaoTalk
    print(f"\n{len(news_items)}개의 뉴스를 카카오톡으로 전송합니다.")
    send_to_me(access_token, news_items, header_title=header_title)

if __name__ == "__main__":
    main()
