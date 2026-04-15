import requests
import json
import os
from dotenv import load_dotenv

TOKEN_FILE = "kakao_token.json"

class KakaoAuth:
    def __init__(self, rest_api_key, redirect_uri):
        self.rest_api_key = rest_api_key
        self.redirect_uri = redirect_uri
        self.tokens = self.load_tokens()

    def load_tokens(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        return None

    def save_tokens(self, tokens):
        self.tokens = tokens
        with open(TOKEN_FILE, "w") as f:
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
            print("No refresh token available.")
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
            print(f"Error refreshing token: {response.json()}")
            return False

    def get_access_token(self):
        self.refresh_access_token()
        return self.tokens.get("access_token")

if __name__ == "__main__":
    load_dotenv()
    REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    
    # 이 부분에 새로 발급받은 인증 코드를 넣으세요.
    AUTH_CODE = "YOUR_NEW_AUTH_CODE_HERE"

    if AUTH_CODE == "YOUR_NEW_AUTH_CODE_HERE":
        print("kakao_auth.py의 AUTH_CODE 변수에 인증 코드를 입력하고 실행하세요.")
    else:
        auth = KakaoAuth(REST_API_KEY, REDIRECT_URI)
        if auth.get_first_token(AUTH_CODE):
            print("토큰이 성공적으로 저장되었습니다 (kakao_token.json)")
        else:
            print("토큰 저장에 실패했습니다.")
