import requests
import json

def get_friends_list(access_token):
    """
    Fetches the list of authorized friends.
    Requires 'friends' scope.
    """
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("elements", [])
    else:
        print(f"Error fetching friends list: {response.json()}")
        return []

def send_to_friends(access_token, friend_uuids, news_items):
    """
    Sends news items to multiple friends using List Template.
    'news_items' is a list of dicts from crawler.py
    """
    if not friend_uuids:
        print("No friends to send to.")
        return

    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Constructing the List Template
    contents = []
    for item in news_items[:5]: # Max 5 for List Template
        contents.append({
            "title": item["title"],
            "description": item["press"],
            "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbCj7C0%2FbtrKkXz3R5f%2F1H0p90H0G00H0G00H0G00H0G00H0G00H0G00H0%2Fimg.png", # Placeholder news icon
            "link": {
                "web_url": item["link"],
                "mobile_web_url": item["link"]
            }
        })

    template_object = {
        "object_type": "list",
        "header_title": "Daily News Ranking",
        "header_link": {
            "web_url": "https://news.naver.com",
            "mobile_web_url": "https://news.naver.com"
        },
        "contents": contents,
        "buttons": [
            {
                "title": "View More",
                "link": {
                    "web_url": "https://news.naver.com",
                    "mobile_web_url": "https://news.naver.com"
                }
            }
        ]
    }

    data = {
        "receiver_uuids": json.dumps(friend_uuids),
        "template_object": json.dumps(template_object)
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Messages sent successfully.")
    else:
        print(f"Error sending messages: {response.json()}")

def send_to_me(access_token, news_items):
    """
    Sends news items to myself (Kakao Memo).
    """
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    contents = []
    for item in news_items[:5]: # Max 5 for List Template
        title = item["title"]
        if len(title) > 40:
            title = title[:37] + "..."
            
        contents.append({
            "title": title,
            "description": item["press"],
            "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbCj7C0%2FbtrKkXz3R5f%2F1H0p90H0G00H0G00H0G00H0G00H0G00H0G00H0%2Fimg.png",
            "link": {
                "web_url": item["link"],
                "mobile_web_url": item["link"]
            }
        })

    template_object = {
        "object_type": "list",
        "header_title": "뉴스 테스트 알림",
        "header_link": {
            "web_url": "https://news.naver.com",
            "mobile_web_url": "https://news.naver.com"
        },
        "contents": contents,
        "buttons": [
            {
                "title": "더보기",
                "link": {
                    "web_url": "https://news.naver.com",
                    "mobile_web_url": "https://news.naver.com"
                }
            }
        ]
    }

    data = {
        "template_object": json.dumps(template_object)
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("result_code") == 0:
            print("나에게 보내기 성공! (카카오톡 '나와의 채팅방'을 확인하세요)")
        else:
            print(f"전송은 성공했으나 응답이 이상함: {result}")
    else:
        print(f"Error sending to me: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    from kakao_auth import KakaoAuth
    # Load tokens from file
    import os
    TOKEN_FILE = "kakao_token.json"
    if not os.path.exists(TOKEN_FILE):
        print("kakao_token.json 파일이 없습니다. kakao_auth.py를 먼저 실행하세요.")
    else:
        with open(TOKEN_FILE, "r") as f:
            tokens = json.load(f)
        
        # We need the original credentials to refresh if needed
        # For simplicity, let's assume current access_token is valid or refresh manually
        access_token = tokens.get("access_token")
        
        # Mock news items for testing
        test_news = [
            {"title": "테스트 뉴스 1", "press": "테스트 언론", "link": "https://news.naver.com"},
            {"title": "테스트 뉴스 2", "press": "테스트 언론", "link": "https://news.naver.com"}
        ]
        
        send_to_me(access_token, test_news)
