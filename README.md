# Kakao Daily News Bot

이 서비스는 매일 네이버/다음 뉴스 랭킹을 크롤링하여 등록된 친구들에게 카카오톡 메시지를 전송합니다.

## 1. 사전 준비 (카카오 디벨로퍼스 설정)

1. [카카오 디벨로퍼스](https://developers.kakao.com/) 접속 및 로그인
2. **내 애플리케이션 추가**: 앱 이름과 사업자명을 자유롭게 입력
3. **REST API 키** 확인: `main.py`의 `CONFIG`에 입력
4. **플랫폼 등록**: [플랫폼] > [Web]에 `https://localhost:8000` 등록
5. **카카오 로그인 활성화**: [제품 설정] > [카카오 로그인] > 'ON'
6. **Redirect URI 등록**: `https://localhost:8000` 추가
7. **동의항목 설정**:
   - `카카오톡 메시지 전송` (권장: 필수 동의)
   - `카카오 서비스 내 친구목록` (권장: 선택 또는 필수 동의)
8. **비즈니스 앱 전환**: [내 애플리케이션] > [앱 권한] 등에서 개인 개발자 비즈니스 앱으로 전환해야 실제 친구에게 메시지를 보낼 수 있습니다. (테스트는 팀원만 가능)

## 2. 최초 인증 및 토큰 발급

1. 아래 URL을 브라우저에 입력하여 인증 코드를 받습니다 (REST_API_KEY 입력 필요).
   ```text
   https://kauth.kakao.com/oauth/authorize?client_id={REST_API}uri={REDIRECT_URI}&response_type=code&scope=talk_message,friends
   ```
2. 로그인 후 이동된 페이지의 주소창에서 `code=...` 부분을 복사합니다.
3. `kakao_auth.py`를 사용하여 최초 토큰을 저장합니다 (수동 실행 필요).

## 3. 리눅스 서버 배포 (Cron)

매일 아침 8시에 실행하려면 리눅스 서버에서 `crontab -e`를 입력하고 다음을 추가합니다.
```bash
0 8 * * * /usr/bin/python3 /path/to/news-bot/main.py
```

## 주의사항
- `kakao_token.json` 파일에는 중요한 인증 정보가 들어있으므로 외부에 노출되지 않도록 주의하세요.
- 친구가 메시지를 받으려면, 해당 친구도 위 2번의 인증 과정을 한 번 거쳐서 앱에 가입되어야 합니다.
