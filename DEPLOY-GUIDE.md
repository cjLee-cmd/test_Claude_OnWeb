# GitHub Pages 배포 가이드

## ✅ 완료된 작업

1. ✅ GitHub Actions 워크플로우 생성 완료
2. ✅ `gh-pages` 브랜치 자동 생성 완료
3. ✅ 배포 준비 완료

## 🔧 GitHub Pages 활성화 방법

**이제 GitHub 웹사이트에서 다음 단계를 진행하세요:**

### 1단계: GitHub 저장소 설정으로 이동

```
https://github.com/cjLee-cmd/test_Claude_OnWeb/settings/pages
```

### 2단계: Source 설정

- **Source**를 `Deploy from a branch`로 선택
- **Branch**를 `gh-pages` 선택
- **Folder**를 `/ (root)` 선택
- **Save** 버튼 클릭

### 3단계: 배포 완료 확인

설정 후 1-2분 기다린 다음 아래 주소로 접속:

```
https://cjlee-cmd.github.io/test_Claude_OnWeb/
```

## 📋 페이지 구조

- **메인 페이지**: `https://cjlee-cmd.github.io/test_Claude_OnWeb/`
- **Google 데모**: `https://cjlee-cmd.github.io/test_Claude_OnWeb/google-demo.html`
- **문서**: `https://cjlee-cmd.github.io/test_Claude_OnWeb/README-MCP.md`

## 🔍 문제 해결

### 여전히 404 에러가 발생하는 경우:

1. **Actions 탭 확인**
   - `https://github.com/cjLee-cmd/test_Claude_OnWeb/actions`
   - "Deploy to GitHub Pages" 워크플로우가 성공적으로 완료되었는지 확인

2. **Branches 확인**
   - `https://github.com/cjLee-cmd/test_Claude_OnWeb/branches`
   - `gh-pages` 브랜치가 존재하는지 확인

3. **Pages 설정 재확인**
   - Settings → Pages
   - Source가 `gh-pages` 브랜치로 설정되어 있는지 확인

4. **캐시 제거**
   - 브라우저 캐시를 삭제하고 다시 접속

## 🎯 자동 배포

이제 `claude/install-google-devtools-011CUKiSXNN8YXmNJWkSNqeq` 브랜치에 푸시할 때마다:
- GitHub Actions가 자동 실행됩니다
- `gh-pages` 브랜치가 업데이트됩니다
- GitHub Pages가 자동으로 재배포됩니다

## 🚀 배포 상태 확인

**GitHub Actions:**
```
https://github.com/cjLee-cmd/test_Claude_OnWeb/actions
```

**GitHub Pages 설정:**
```
https://github.com/cjLee-cmd/test_Claude_OnWeb/settings/pages
```

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
