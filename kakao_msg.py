import requests
import json

def get_friends_list(access_token):
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("elements", [])
    return []

def send_to_me(access_token, news_items, header_title="뉴스 알림", send_list=True, send_summary=True):
    """
    메시지를 분할하여 전송합니다.
    1. 기사 목록 (제목 + 링크)
    2. 기사 요약본 (텍스트)
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    if not news_items:
        return

    # --- 1. 기사 목록 메시지 (List Template) ---
    if send_list:
        list_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        contents = []
        for item in news_items[:5]:
            contents.append({
                "title": item["title"],
                "description": f"출처: {item['press']}",
                "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbCj7C0%2FbtrKkXz3R5f%2F1H0p90H0G00H0G00H0G00H0G00H0G00H0G00H0%2Fimg.png",
                "link": {
                    "web_url": item["link"],
                    "mobile_web_url": item["link"]
                }
            })

        list_template = {
            "object_type": "list",
            "header_title": f"📋 {header_title} 목록",
            "header_link": {"web_url": news_items[0]["link"], "mobile_web_url": news_items[0]["link"]},
            "contents": contents,
            "buttons": [{"title": "뉴스 홈 바로가기", "link": {"web_url": "https://news.naver.com", "mobile_web_url": "https://news.naver.com"}}]
        }
        
        requests.post(list_url, headers=headers, data={"template_object": json.dumps(list_template)})
        print("뉴스 목록 전송 완료")

    # --- 2. 요약본 메시지 (Text Template) ---
    if send_summary:
        summary_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        
        full_summary_text = f"✨ {header_title} 핵심 요약\n"
        full_summary_text += "="*20 + "\n\n"
        for i, item in enumerate(news_items[:5], 1):
            summary = item.get("summary", "요약 정보 없음")
            full_summary_text += f"{i}. {item['title']}\n📝 {summary}\n\n"

        text_template = {
            "object_type": "text",
            "text": full_summary_text,
            "link": {"web_url": "https://news.naver.com", "mobile_web_url": "https://news.naver.com"},
            "button_title": "뉴스 확인하기"
        }

        requests.post(summary_url, headers=headers, data={"template_object": json.dumps(text_template)})
        print("뉴스 요약본 전송 완료")

if __name__ == "__main__":
    pass
