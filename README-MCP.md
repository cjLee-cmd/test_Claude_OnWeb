# Chrome DevTools MCP 설치 및 사용 가이드

## 설치 완료 항목

### 1. Chrome DevTools MCP 패키지 설치
```bash
npm install chrome-devtools-mcp
```
- ✅ 설치 완료: `node_modules/chrome-devtools-mcp/`
- 패키지 버전: latest
- 포함된 도구: Puppeteer 기반 브라우저 자동화

### 2. MCP 설정 파일 생성
`.claude.json` 파일이 프로젝트 루트에 생성되었습니다:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### 3. 구글 홈페이지 열기 스크립트
`open-google.js` 파일이 생성되었습니다. 이 스크립트는 Puppeteer를 사용하여:
- Chrome 브라우저를 headless 모드로 실행
- 구글 홈페이지 접속
- 스크린샷 저장
- 페이지 정보 출력

## 로컬 환경에서 사용 방법

### Chrome/Chromium 설치 (필수)
현재 컨테이너 환경에서는 브라우저 설치에 제약이 있습니다.
로컬 환경에서는 다음 중 하나를 설치하세요:

**macOS:**
```bash
# Homebrew 사용
brew install --cask google-chrome
```

**Ubuntu/Debian:**
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```

**Windows:**
[Chrome 다운로드 페이지](https://www.google.com/chrome/)에서 설치

### Puppeteer 설치 및 실행
```bash
# Puppeteer 설치
npm install puppeteer

# 스크립트 실행
node open-google.js
```

실행 결과:
- `google-homepage.png` 스크린샷 파일 생성
- 콘솔에 페이지 제목과 URL 출력

## Chrome DevTools MCP 기능

### 사용 가능한 도구 카테고리

1. **Input automation** (7개 도구)
   - `click`, `drag`, `fill`, `fill_form`, `handle_dialog`, `hover`, `upload_file`

2. **Navigation automation** (7개 도구)
   - `close_page`, `list_pages`, `navigate_page`, `navigate_page_history`, `new_page`, `select_page`, `wait_for`

3. **Emulation** (3개 도구)
   - `emulate_cpu`, `emulate_network`, `resize_page`

4. **Performance** (3개 도구)
   - `performance_analyze_insight`, `performance_start_trace`, `performance_stop_trace`

5. **Network** (2개 도구)
   - `get_network_request`, `list_network_requests`

6. **Debugging** (4개 도구)
   - `evaluate_script`, `list_console_messages`, `take_screenshot`, `take_snapshot`

## Claude Code에서 MCP 사용하기

Claude Code CLI를 통해 MCP 서버를 추가할 수 있습니다:
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

설정 후, Claude Code에서 다음과 같은 프롬프트를 사용할 수 있습니다:
```
Check the performance of https://developers.chrome.com
```

## 참고 자료
- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome DevTools MCP 블로그](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Model Context Protocol 문서](https://modelcontextprotocol.io/)

## 현재 환경 제약사항
- GUI 없는 컨테이너 환경
- Chrome/Chromium 설치 제한
- 일부 외부 네트워크 접근 제한

로컬 개발 환경에서는 모든 기능이 정상적으로 작동합니다.
