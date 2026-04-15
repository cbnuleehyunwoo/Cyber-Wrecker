import json
import os
import time
import glob
from crawler import search_news, get_article_summary
from kakao_auth import KakaoAuth
from kakao_msg import send_to_me
from dotenv import load_dotenv

TOKEN_DIR = "tokens"

def main():
    load_dotenv()
    REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    
    if not REST_API_KEY or not REDIRECT_URI:
        print(".env 파일 설정을 확인하세요.")
        return

    # 1. 뉴스 검색어 입력
    print("="*30)
    print(" 멀티 유저 뉴스 봇 서비스를 시작합니다.")
    print("="*30)
    keyword = input("검색할 뉴스 키워드 (엔터 시 '최신 뉴스'): ").strip()
    
    search_query = keyword if keyword else "최신 뉴스"
    header_title = f"'{search_query}' 관련 뉴스"

    # 2. 뉴스 데이터 준비 (모든 유저에게 동일한 뉴스 전송)
    print(f"\n[{header_title}] 뉴스를 분석 중입니다...")
    news_items = search_news(search_query)
    if not news_items:
        print("관련 뉴스를 찾을 수 없습니다.")
        return

    # 3. 등록된 모든 토큰 파일 찾기
    token_files = glob.glob(os.path.join(TOKEN_DIR, "*.json"))
    if not token_files:
        print(f"'{TOKEN_DIR}' 폴더에 등록된 토큰 파일이 없습니다.")
        return

    print(f"총 {len(token_files)}명의 사용자에게 전송을 시작합니다.\n")

    # 4. 사용자별 전송 루프
    for token_file in token_files:
        user_name = os.path.basename(token_file).replace(".json", "")
        print(f">>> [{user_name}] 사용자에게 전송 시도...")
        
        auth = KakaoAuth(REST_API_KEY, REDIRECT_URI, token_file=token_file)
        access_token = auth.get_access_token()
        
        if access_token:
            send_to_me(access_token, news_items, header_title=header_title)
            time.sleep(1) # 유저 간 전송 간격
        else:
            print(f"!!! [{user_name}] 토큰 갱신 실패. 수동 갱신이 필요할 수 있습니다.")

    print("\n모든 전송 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
