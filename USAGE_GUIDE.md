# MedDRA 폼 자동화 사용 가이드

## 프로젝트 개요

이 프로젝트는 CIOMS Form PDF에서 데이터를 자동으로 추출하여 MedDRA 웹 폼에 입력하는 자동화 소프트웨어입니다.

## 작업 흐름

```
1. PDF에서 데이터 추출
   ↓
2. 첫 번째 웹사이트 분석 (MedDRA-Auto-withoutServer/main.html)
   ↓
3. 두 번째 웹사이트 로그인 (MedDRA-DB)
   ↓
4. 새 폼 작성 페이지로 이동
   ↓
5. 추출된 데이터 입력
   ↓
6. 저장
   ↓
7. 폼 목록에서 확인
```

## 시스템 요구사항

### 필수 요구사항
- Python 3.7 이상
- Chrome 또는 Chromium 브라우저
- 인터넷 연결

### Python 패키지
requirements.txt에 명시된 패키지들이 자동으로 설치됩니다:
- selenium
- webdriver-manager
- PyPDF2
- pdfplumber
- python-dotenv

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/cjLee-cmd/test_Claude_OnWeb.git
cd test_Claude_OnWeb
```

### 2. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. Chrome/Chromium 브라우저 설치 (없는 경우)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

**macOS:**
```bash
brew install --cask google-chrome
```

**Windows:**
[Google Chrome 다운로드](https://www.google.com/chrome/)

## 사용 방법

### 방법 1: 자동 실행 스크립트 사용 (권장)

```bash
./run_automation.sh
```

이 스크립트는 다음을 자동으로 수행합니다:
1. 환경 확인 (Python, Chrome)
2. 패키지 설치
3. PDF 추출 테스트
4. 웹 자동화 실행

### 방법 2: 단계별 실행

#### 1단계: PDF 데이터 추출 테스트
```bash
python3 test_extraction.py
```

이 명령은:
- PDF에서 데이터를 추출합니다
- 추출된 데이터를 검증합니다
- `extracted_data.json` 파일로 저장합니다

#### 2단계: 웹 자동화 실행
```bash
python3 web_automation.py
```

이 명령은:
- 브라우저를 열어 자동화를 수행합니다
- 각 단계마다 스크린샷을 저장합니다
- 진행 상황을 콘솔에 출력합니다

### 방법 3: Python 코드에서 직접 사용

```python
from pdf_extractor import CIOMSFormExtractor
from web_automation import MedDRAAutomation

# PDF에서 데이터 추출
extractor = CIOMSFormExtractor("CIOMS-I-Form_example 1.pdf")
data = extractor.extract_all_data()

# 웹 자동화 실행
automation = MedDRAAutomation(headless=False)
automation.run_automation(
    pdf_path="CIOMS-I-Form_example 1.pdf",
    first_url="https://cjlee-cmd.github.io/MedDRA-Auto-withoutServer/main.html",
    second_url="https://cjlee-cmd.github.io/MedDRA-DB",
    username="acuzen",
    password="acuzen"
)
```

## 설정 변경

### 헤드리스 모드 활성화
브라우저 창을 표시하지 않고 백그라운드에서 실행하려면:

```python
automation = MedDRAAutomation(headless=True)
```

### 로그인 정보 변경
`web_automation.py`의 `main()` 함수에서 수정:

```python
username = "your_username"
password = "your_password"
```

### URL 변경
다른 웹사이트를 사용하려면:

```python
first_url = "https://your-first-site.com"
second_url = "https://your-second-site.com"
```

## 생성되는 파일

### 데이터 파일
- `extracted_data.json` - PDF에서 추출된 데이터 (JSON 형식)

### 스크린샷 파일
- `page1_source.html` - 첫 번째 웹사이트 소스 코드
- `page1_screenshot.png` - 첫 번째 웹사이트 스크린샷
- `login_page.png` - 로그인 페이지
- `after_login.png` - 로그인 후 화면
- `new_form_page.png` - 새 폼 작성 페이지
- `form_filled.png` - 데이터 입력 완료 화면
- `after_save.png` - 저장 후 화면
- `form_list.png` - 폼 목록 페이지

### 에러 스크린샷
문제 발생 시 다음 파일들이 생성됩니다:
- `error_page1.png`
- `error_login.png`
- `error_navigate.png`
- `error_fill.png`
- `error_save.png`
- `error_verify.png`

## 추출되는 데이터 필드

### 환자 정보 (Patient Information)
- `initials` - 환자 이니셜
- `country` - 국가
- `dob_day/month/year` - 생년월일
- `age` - 나이
- `sex` - 성별

### 부작용 정보 (Reaction Information)
- `onset_day/month/year` - 부작용 발생일
- `reactions` - 부작용 목록 (이름, 코드, 결과)
- `patient_died` - 환자 사망 여부
- `life_threatening` - 생명 위협 여부
- `hospitalization` - 입원 여부

### 의심 약물 (Suspect Drugs)
- `name` - 약물명
- `dose` - 용량
- `route` - 투여 경로
- `indication` - 적응증
- `start_date/end_date` - 투여 기간
- `duration` - 투여 기간

### 병용 약물 (Concomitant Drugs)
- 의심 약물과 동일한 필드

### 병력 (Medical History)
- `diagnosis` - 진단명
- `other_history` - 기타 병력

### 제조사 정보 (Manufacturer Information)
- `study_no` - 연구 번호
- `center_no` - 센터 번호
- `patient_no` - 환자 번호
- `mfr_control_no` - 제조사 관리 번호

## 문제 해결

### Chrome 드라이버 문제
```
Error: ChromeDriver not found
```

**해결책:**
webdriver-manager가 자동으로 설치하므로 보통 문제가 없지만, 수동 설치가 필요한 경우:
```bash
pip install webdriver-manager --upgrade
```

### PDF 추출 오류
```
Error: Cannot read PDF
```

**해결책:**
- PDF 파일 경로가 정확한지 확인
- PDF 파일이 손상되지 않았는지 확인
- PyPDF2와 pdfplumber 재설치:
  ```bash
  pip install PyPDF2 pdfplumber --upgrade
  ```

### 웹사이트 접속 오류
```
Error: Cannot access website
```

**해결책:**
- 인터넷 연결 확인
- 웹사이트 URL이 올바른지 확인
- 방화벽이나 프록시 설정 확인

### 로그인 실패
```
Error: Login failed
```

**해결책:**
- 로그인 정보가 정확한지 확인
- 웹사이트 구조가 변경되었는지 확인
- `login_page.png` 스크린샷 확인

### 폼 필드를 찾을 수 없음
```
Could not find field 'xxx'
```

**해결책:**
- 웹사이트 구조가 변경되었을 수 있습니다
- `web_automation.py`의 선택자(selector)를 업데이트해야 할 수 있습니다
- 생성된 스크린샷을 확인하여 페이지 구조를 분석하세요

## 커스터마이징

### 새로운 필드 추가
`pdf_extractor.py`에서 새로운 파싱 메서드 추가:

```python
def parse_new_field(self):
    """새로운 필드 파싱"""
    new_data = {}
    # 정규식 또는 문자열 검색으로 데이터 추출
    match = re.search(r'PATTERN', self.text)
    if match:
        new_data['field_name'] = match.group(1)
    return new_data
```

### 폼 입력 로직 수정
`web_automation.py`의 `fill_form_with_data()` 메서드 수정:

```python
def fill_form_with_data(self):
    # 새로운 필드 입력 로직 추가
    self._try_fill_field('new_field_id', 'value')
```

## 보안 주의사항

- 로그인 정보는 환경 변수나 별도의 설정 파일에 저장하세요
- 생성된 스크린샷에 민감한 정보가 포함될 수 있으므로 주의하세요
- Git에 커밋하기 전에 `.gitignore`에 다음을 추가하세요:
  ```
  *.png
  *.html
  extracted_data.json
  .env
  ```

## 라이선스 및 면책 조항

이 소프트웨어는 교육 및 테스트 목적으로 제작되었습니다. 실제 환경에서 사용하기 전에 충분한 테스트를 수행하세요.

## 지원 및 문의

문제가 발생하거나 질문이 있는 경우:
1. 생성된 스크린샷 파일들을 확인하세요
2. 콘솔 출력 로그를 확인하세요
3. GitHub Issues에 문의하세요

## 업데이트 히스토리

### v1.0 (2025-10-21)
- 초기 버전 릴리스
- PDF 데이터 추출 기능
- 웹 자동화 기능
- 데모용 예제 포함
