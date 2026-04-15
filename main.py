import json
import os
from crawler import get_news_rankings
from kakao_auth import KakaoAuth
from kakao_msg import send_to_me

from dotenv import load_dotenv

TOKEN_FILE = "kakao_token.json"

def main():
    load_dotenv()
    # 1. Load authentication information from environment variables
    REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    
    if not REST_API_KEY or not REDIRECT_URI:
        print(".env 파일에 KAKAO_REST_API_KEY와 KAKAO_REDIRECT_URI를 설정해주세요.")
        return
        
    auth = KakaoAuth(REST_API_KEY, REDIRECT_URI)
    
    # Check if token exists
    if not os.path.exists(TOKEN_FILE):
        print("kakao_token.json 파일이 없습니다. kakao_auth.py를 먼저 실행하여 토큰을 생성하세요.")
        return

    # 2. Refresh/Get Access Token
    access_token = auth.get_access_token()
    if not access_token:
        print("Access Token을 가져오는 데 실패했습니다.")
        return

    # 3. Crawl News
    print("뉴스를 크롤링 중입니다...")
    news_items = get_news_rankings()
    
    if not news_items:
        print("크롤링된 뉴스가 없습니다.")
        return

    # 4. Send to KakaoTalk (Me)
    print(f"{len(news_items)}개의 뉴스를 카카오톡으로 전송합니다.")
    send_to_me(access_token, news_items)

if __name__ == "__main__":
    main()
