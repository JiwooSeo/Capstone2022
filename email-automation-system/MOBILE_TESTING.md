# 모바일에서 테스트하기

이 가이드는 PC/서버에서 백엔드를 실행하고 모바일 기기에서 프론트엔드를 테스트하는 방법을 설명합니다.

## 1️⃣ PC/서버에서 백엔드 실행

### 단계 1: IP 주소 확인

#### Windows
```bash
ipconfig
# IPv4 주소 찾기 (예: 192.168.1.100)
```

#### Mac/Linux
```bash
ifconfig
# inet 주소 찾기 (예: 192.168.1.100)
```

### 단계 2: 환경변수 설정

`backend/.env` 파일 생성 후 IP 주소 추가:

```bash
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/email_automation

# Gmail OAuth (Google Cloud Console에서 받은 값)
GMAIL_CLIENT_ID=your_google_client_id
GMAIL_CLIENT_SECRET=your_google_client_secret
GMAIL_REDIRECT_URI=http://192.168.1.100:3000/auth/callback

# OpenAI
OPENAI_API_KEY=sk-your_openai_key

# 보안
JWT_SECRET_KEY=your_secret_key_here
ENCRYPTION_KEY=your_fernet_key_here

# Redis
REDIS_URL=redis://localhost:6379

# 애플리케이션
DEBUG=True
ENVIRONMENT=development

# CORS - 모바일 IP 주소 추가 (중요!)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://192.168.1.100:3000,http://192.168.1.100:8000
```

**⚠️ IP 주소를 자신의 PC/서버 IP로 변경하세요!**

### 단계 3: Docker Compose로 실행

```bash
cd email-automation-system

# 모든 서비스 시작
docker-compose up -d

# 데이터베이스 마이그레이션
docker-compose exec backend alembic upgrade head

# 로그 확인
docker-compose logs -f backend
```

또는 수동으로:

```bash
# 백엔드만 실행
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

**접근 가능한 주소:**
- 백엔드 API: `http://192.168.1.100:8000`
- API 문서: `http://192.168.1.100:8000/docs`

---

## 2️⃣ 모바일에서 프론트엔드 접근

### 단계 1: 모바일과 PC가 같은 네트워크에 연결

Wi-Fi를 통해 같은 네트워크에 연결되어 있는지 확인하세요.

### 단계 2: 모바일 브라우저에서 접근

모바일의 웹 브라우저를 열고 다음 주소 입력:

```
http://192.168.1.100:3000
```

**IP 주소를 자신의 PC/서버 IP로 변경하세요!**

### 단계 3: 로그인 테스트

1. "Sign in with Google" 버튼 클릭
2. Google 계정으로 로그인
3. 대시보드, 캘린더, 설정 페이지 접근

---

## 🔧 모바일에서 개발하기 (선택사항)

### Next.js 개발 서버를 모바일에서 접근하게 하기

`frontend/.env.local` 생성:

```bash
NEXT_PUBLIC_API_URL=http://192.168.1.100:8000/api
```

프론트엔드 시작:

```bash
cd frontend
npm install
npm run dev

# 출력: Local: http://localhost:3000
```

모바일에서 접근:

```
http://192.168.1.100:3000
```

---

## 🌐 Google OAuth 설정 (모바일용)

Google Cloud Console에서 OAuth 설정을 수정해야 합니다.

### 1. Authorized redirect URIs 추가

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 프로젝트 선택
3. "OAuth 동의 화면" 또는 "사용자 인증 정보" 클릭
4. OAuth 2.0 클라이언트 ID 편집
5. **Authorized redirect URIs** 에 추가:
   ```
   http://192.168.1.100:3000/api/auth/google-callback
   ```
6. 저장

### 2. 백엔드 환경변수 업데이트

```bash
GMAIL_REDIRECT_URI=http://192.168.1.100:3000/api/auth/google-callback
```

---

## 📱 모바일 테스트 체크리스트

- [ ] 모바일 브라우저에서 `http://192.168.1.100:3000` 접근 가능
- [ ] "Sign in with Google" 버튼이 표시됨
- [ ] Google 로그인 완료 후 대시보드로 리다이렉트
- [ ] 대시보드에 통계 표시
- [ ] 캘린더 페이지 접근 가능
- [ ] 설정 페이지에서 사용자 정보 표시
- [ ] 로그아웃 버튼 작동

---

## 🐛 모바일에서 문제 해결

### 문제 1: "연결할 수 없음"

**원인**: PC와 모바일이 같은 네트워크에 없음

**해결**:
```bash
# 현재 PC의 IP 확인
ipconfig (Windows) 또는 ifconfig (Mac/Linux)

# 모바일 Wi-Fi 설정에서 같은 네트워크 선택
```

### 문제 2: CORS 오류

**원인**: 백엔드의 ALLOWED_ORIGINS에 모바일 IP가 없음

**해결**:
```bash
# backend/.env 수정
ALLOWED_ORIGINS=http://localhost:3000,http://192.168.1.100:3000

# 백엔드 재시작
docker-compose restart backend
```

### 문제 3: Google 로그인 실패

**원인**: Redirect URI가 일치하지 않음

**해결**:
1. Google Cloud Console에서 설정 확인
2. `GMAIL_REDIRECT_URI` 환경변수 확인
3. 백엔드 로그 확인: `docker-compose logs backend`

### 문제 4: API 응답 없음

**원인**: 백엔드가 실행 중이 아님

**해결**:
```bash
# 백엔드 상태 확인
docker-compose ps

# 로그 보기
docker-compose logs -f backend

# 수동 시작
python app/main.py
```

---

## 📊 모바일 테스트용 API 엔드포인트

모바일 브라우저 DevTools에서 테스트 가능:

### 건강 상태 확인
```bash
curl http://192.168.1.100:8000/health
```

### API 문서 (모바일 브라우저)
```
http://192.168.1.100:8000/docs
```

---

## 💡 팁

1. **localhost 대신 IP 사용**: 항상 `192.168.1.100` 같은 실제 IP 사용
2. **Wi-Fi 연결 확인**: 모바일과 PC가 같은 네트워크에 연결되어 있는지 확인
3. **방화벽 확인**: 방화벽이 8000, 3000 포트를 차단하지 않는지 확인
4. **개발자 도구**: 모바일 브라우저의 개발자 도구에서 네트워크/콘솔 확인

---

## 🔄 빠른 재시작

모바일 테스트 중 변경사항을 적용하려면:

```bash
# 백엔드 재시작
docker-compose restart backend

# 또는 프론트엔드 새로고침
# 모바일 브라우저에서 Ctrl+Shift+R (또는 Cmd+Shift+R) 눌러 캐시 무효화
```

---

## 📝 로그 확인

모바일에서 오류가 발생하면 PC에서 로그 확인:

```bash
# 모든 로그
docker-compose logs -f

# 백엔드만
docker-compose logs -f backend

# 실시간 모니터링
docker-compose logs -f --tail=100
```
