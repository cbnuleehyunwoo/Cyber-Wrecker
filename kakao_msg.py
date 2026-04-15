import requests
import json

def get_friends_list(access_token):
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("elements", [])
    return []

def send_to_me(access_token, news_items, header_title="뉴스 알림"):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    contents = []
    for item in news_items[:5]:
        title = item["title"]
        if len(title) > 40:
            title = title[:37] + "..."
            
        description = item.get("summary", item["press"])
        if len(description) > 50:
            description = description[:47] + "..."

        contents.append({
            "title": title,
            "description": f"[{item['press']}] {description}",
            "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbCj7C0%2FbtrKkXz3R5f%2F1H0p90H0G00H0G00H0G00H0G00H0G00H0G00H0%2Fimg.png",
            "link": {
                "web_url": item["link"],
                "mobile_web_url": item["link"]
            }
        })

    template_object = {
        "object_type": "list",
        "header_title": header_title,
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

    data = {"template_object": json.dumps(template_object)}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("result_code") == 0:
            print(f"[{header_title}] 나에게 보내기 성공!")
        else:
            print(f"전송 실패 응답: {result}")
    else:
        print(f"Error: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    # Test block
    pass
