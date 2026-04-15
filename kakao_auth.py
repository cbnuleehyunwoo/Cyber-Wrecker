import requests
import json
import os
from dotenv import load_dotenv

class KakaoAuth:
    def __init__(self, rest_api_key, redirect_uri, token_file="kakao_token.json"):
        self.rest_api_key = rest_api_key
        self.redirect_uri = redirect_uri
        self.token_file = token_file
        self.tokens = self.load_tokens()

    def load_tokens(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                return json.load(f)
        return None

    def save_tokens(self, tokens):
        self.tokens = tokens
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(os.path.abspath(self.token_file)), exist_ok=True)
        with open(self.token_file, "w") as f:
            json.dump(tokens, f)

    def get_first_token(self, auth_code):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.rest_api_key,
            "redirect_uri": self.redirect_uri,
            "code": auth_code
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.save_tokens(response.json())
            return True
        else:
            print(f"Error getting token: {response.json()}")
            return False

    def refresh_access_token(self):
        if not self.tokens or "refresh_token" not in self.tokens:
            print(f"No refresh token for {self.token_file}")
            return False

        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.rest_api_key,
            "refresh_token": self.tokens["refresh_token"]
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            new_tokens = response.json()
            if "refresh_token" not in new_tokens:
                new_tokens["refresh_token"] = self.tokens["refresh_token"]
            self.save_tokens(new_tokens)
            return True
        else:
            print(f"Error refreshing token for {self.token_file}: {response.json()}")
            return False

    def get_access_token(self):
        if self.refresh_access_token():
            return self.tokens.get("access_token")
        return None

if __name__ == "__main__":
    import sys
    load_dotenv()
    REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    
    # 사용법: python kakao_auth.py <파일명(tokens/user1.json)> <인증코드>
    if len(sys.argv) < 3:
        print("사용법: python kakao_auth.py tokens/user_name.json <AUTH_CODE>")
    else:
        file_path = sys.argv[1]
        auth_code = sys.argv[2]
        auth = KakaoAuth(REST_API_KEY, REDIRECT_URI, token_file=file_path)
        if auth.get_first_token(auth_code):
            print(f"성공: {file_path}에 토큰이 저장되었습니다.")
        else:
            print("실패: 인증 코드를 확인하세요.")
