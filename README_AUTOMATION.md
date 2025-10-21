# MedDRA Form Automation

## 개요
이 프로젝트는 CIOMS Form PDF에서 데이터를 추출하여 MedDRA 웹 폼에 자동으로 입력하는 자동화 도구입니다.

## 주요 기능

### 1. PDF 데이터 추출 (`pdf_extractor.py`)
- CIOMS Form PDF에서 환자 정보, 부작용 정보, 의심 약물, 병용 약물 등을 자동 추출
- 정규식을 사용한 지능형 데이터 파싱
- 추출된 데이터 요약 출력

### 2. 웹 자동화 (`web_automation.py`)
- Selenium을 사용한 웹 브라우저 자동화
- MedDRA-Auto-withoutServer 페이지 분석
- MedDRA-DB 로그인 및 폼 작성
- 자동 저장 및 확인

## 사용 방법

### 1. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. PDF 데이터 추출 테스트
```bash
python pdf_extractor.py
```

### 3. 전체 자동화 실행
```bash
python web_automation.py
```

## 설정

### 웹사이트 URL
- 첫 번째 사이트: `https://cjlee-cmd.github.io/MedDRA-Auto-withoutServer/main.html`
- 두 번째 사이트 (로그인): `https://cjlee-cmd.github.io/MedDRA-DB`

### 로그인 정보
- ID: `acuzen`
- PW: `acuzen`

## 파일 구조
```
test_Claude_OnWeb/
├── pdf_extractor.py          # PDF 데이터 추출 모듈
├── web_automation.py          # 웹 자동화 메인 스크립트
├── requirements.txt           # Python 패키지 의존성
├── CIOMS-I-Form_example 1.pdf # 예제 PDF 파일
└── README_AUTOMATION.md       # 이 문서
```

## 생성되는 파일
자동화 실행 중 다음 파일들이 생성됩니다:
- `page1_source.html` - 첫 번째 웹사이트 소스
- `page1_screenshot.png` - 첫 번째 웹사이트 스크린샷
- `login_page.png` - 로그인 페이지 스크린샷
- `after_login.png` - 로그인 후 스크린샷
- `new_form_page.png` - 새 폼 페이지 스크린샷
- `form_filled.png` - 폼 입력 완료 스크린샷
- `after_save.png` - 저장 후 스크린샷
- `form_list.png` - 폼 목록 페이지 스크린샷

## 클래스 및 메서드

### CIOMSFormExtractor
- `extract_text()`: PDF에서 텍스트 추출
- `parse_patient_info()`: 환자 정보 파싱
- `parse_reaction_info()`: 부작용 정보 파싱
- `parse_suspect_drugs()`: 의심 약물 파싱
- `parse_concomitant_drugs()`: 병용 약물 파싱
- `extract_all_data()`: 모든 데이터 추출
- `print_summary()`: 추출된 데이터 요약 출력

### MedDRAAutomation
- `setup_driver()`: Selenium WebDriver 설정
- `load_data_from_pdf()`: PDF에서 데이터 로드
- `analyze_first_website()`: 첫 번째 웹사이트 분석
- `login_to_meddra_db()`: MedDRA-DB 로그인
- `navigate_to_new_form()`: 새 폼 작성 페이지 이동
- `fill_form_with_data()`: 폼 데이터 입력
- `save_form()`: 폼 저장
- `verify_form_list()`: 폼 목록에서 확인
- `run_automation()`: 전체 프로세스 실행

## 주의사항
- Chrome 브라우저가 설치되어 있어야 합니다
- 인터넷 연결이 필요합니다
- 웹사이트 구조가 변경되면 스크립트 수정이 필요할 수 있습니다

## 문제 해결
- 스크린샷 파일을 확인하여 어느 단계에서 문제가 발생했는지 확인
- 에러 메시지와 함께 생성되는 `error_*.png` 파일 확인
- 헤드리스 모드를 비활성화하여 브라우저 동작 직접 확인 가능

## 라이선스
이 프로젝트는 테스트 및 데모 목적으로 제작되었습니다.
