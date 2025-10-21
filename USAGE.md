# Chrome DevTools MCP 사용 방법

## 현재 환경 제약사항

이 프로젝트는 GUI 없는 컨테이너 환경에서 실행되고 있어 다음 제약이 있습니다:
- 브라우저 UI를 직접 표시할 수 없음
- 일부 외부 네트워크 접근 제한

## 로컬 환경에서 사용하기

### 1. HTML 데모 페이지 열기

구글 스타일 데모 페이지를 브라우저에서 직접 열어보세요:

```bash
# 프로젝트 디렉토리에서
open google-demo.html  # macOS
# 또는
xdg-open google-demo.html  # Linux
# 또는
start google-demo.html  # Windows
```

### 2. Chrome DevTools MCP로 실제 구글 페이지 열기

Chrome이 설치된 환경에서:

```bash
# Puppeteer 설치 (Chrome 포함)
npm install puppeteer

# 스크립트 실행
node open-google.js
```

실행 결과:
- Chrome이 headless 모드로 실행됩니다
- https://www.google.com 에 접속합니다
- `google-homepage.png` 스크린샷이 생성됩니다
- 페이지 제목과 URL이 출력됩니다

### 3. MCP 서버 직접 사용

`.claude.json` 설정이 완료되어 있어 Claude Code에서 다음과 같이 사용할 수 있습니다:

```bash
# MCP 서버가 자동으로 연결됩니다
# Claude Code에서 다음과 같은 프롬프트 사용:
"https://www.google.com 페이지의 성능을 분석해줘"
"구글 홈페이지 스크린샷을 찍어줘"
```

## 파일 구조

```
.
├── .claude.json          # MCP 서버 설정
├── google-demo.html      # 구글 스타일 데모 페이지
├── open-google.js        # Puppeteer 스크립트
├── README-MCP.md         # MCP 설치 가이드
└── USAGE.md             # 이 파일
```

## MCP 기능

Chrome DevTools MCP를 통해 다음 작업이 가능합니다:

- **페이지 탐색**: 웹사이트 열기, 이동, 새 탭 생성
- **입력 자동화**: 클릭, 폼 작성, 파일 업로드
- **성능 분석**: 성능 추적, 네트워크 요청 분석
- **디버깅**: 스크린샷, 콘솔 메시지, 스크립트 실행

자세한 내용은 README-MCP.md를 참고하세요.
