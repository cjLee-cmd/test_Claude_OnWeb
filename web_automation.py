"""
MedDRA 폼 자동화 스크립트
1. MedDRA-Auto-withoutServer/main.html 페이지에서 데이터 파악
2. MedDRA-DB 사이트에 로그인하여 폼 작성
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pdf_extractor import CIOMSFormExtractor


class MedDRAAutomation:
    """MedDRA 폼 자동화 클래스"""

    def __init__(self, headless=False):
        """
        초기화
        Args:
            headless: 헤드리스 모드 사용 여부
        """
        self.headless = headless
        self.driver = None
        self.wait = None
        self.data = None

    def setup_driver(self):
        """Selenium WebDriver 설정"""
        print("Setting up Chrome WebDriver...")

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("WebDriver setup complete!")
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            raise

    def load_data_from_pdf(self, pdf_path: str):
        """
        PDF에서 데이터 로드
        Args:
            pdf_path: PDF 파일 경로
        """
        print(f"\nLoading data from PDF: {pdf_path}")
        extractor = CIOMSFormExtractor(pdf_path)
        self.data = extractor.extract_all_data()
        print("Data extracted from PDF successfully!")
        extractor.print_summary()
        return self.data

    def analyze_first_website(self, url: str):
        """
        첫 번째 웹사이트 분석 (MedDRA-Auto-withoutServer/main.html)
        Args:
            url: 웹사이트 URL
        """
        print(f"\n[Step 1] Analyzing first website: {url}")
        try:
            self.driver.get(url)
            time.sleep(3)

            # 페이지 소스 저장
            page_source = self.driver.page_source
            with open('/home/user/test_Claude_OnWeb/page1_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print("Page source saved to page1_source.html")

            # 페이지 스크린샷
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/page1_screenshot.png')
            print("Screenshot saved to page1_screenshot.png")

            # 폼 필드 분석
            print("\nAnalyzing form fields...")
            form_fields = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(form_fields)} input fields")

            for i, field in enumerate(form_fields[:10]):  # 처음 10개만 출력
                field_type = field.get_attribute("type")
                field_name = field.get_attribute("name")
                field_id = field.get_attribute("id")
                field_placeholder = field.get_attribute("placeholder")
                print(f"  Field {i+1}: type={field_type}, name={field_name}, id={field_id}, placeholder={field_placeholder}")

            return True

        except Exception as e:
            print(f"Error analyzing first website: {e}")
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_page1.png')
            return False

    def login_to_meddra_db(self, url: str, username: str, password: str):
        """
        MedDRA-DB 사이트에 로그인
        Args:
            url: 로그인 페이지 URL
            username: 사용자 ID
            password: 비밀번호
        """
        print(f"\n[Step 2] Logging in to MedDRA-DB: {url}")
        try:
            self.driver.get(url)
            time.sleep(3)

            # 페이지 소스 저장
            page_source = self.driver.page_source
            with open('/home/user/test_Claude_OnWeb/login_page_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print("Login page source saved")

            # 스크린샷
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/login_page.png')
            print("Login page screenshot saved")

            # 로그인 필드 찾기 시도
            print("\nLooking for login fields...")

            # 여러 가능한 선택자로 시도
            username_selectors = [
                (By.ID, "username"),
                (By.ID, "user"),
                (By.ID, "userId"),
                (By.NAME, "username"),
                (By.NAME, "user"),
                (By.NAME, "id"),
                (By.XPATH, "//input[@type='text']"),
                (By.XPATH, "//input[@placeholder='ID' or @placeholder='Username' or @placeholder='사용자 ID']")
            ]

            password_selectors = [
                (By.ID, "password"),
                (By.ID, "passwd"),
                (By.ID, "pwd"),
                (By.NAME, "password"),
                (By.NAME, "passwd"),
                (By.NAME, "pwd"),
                (By.XPATH, "//input[@type='password']")
            ]

            username_field = None
            password_field = None

            # Username 필드 찾기
            for by, selector in username_selectors:
                try:
                    username_field = self.driver.find_element(by, selector)
                    print(f"Found username field with {by}={selector}")
                    break
                except NoSuchElementException:
                    continue

            # Password 필드 찾기
            for by, selector in password_selectors:
                try:
                    password_field = self.driver.find_element(by, selector)
                    print(f"Found password field with {by}={selector}")
                    break
                except NoSuchElementException:
                    continue

            if not username_field or not password_field:
                print("Could not find login fields. Analyzing page structure...")
                # 모든 input 필드 출력
                all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                print(f"\nFound {len(all_inputs)} input fields:")
                for i, inp in enumerate(all_inputs):
                    print(f"  Input {i+1}:")
                    print(f"    type: {inp.get_attribute('type')}")
                    print(f"    name: {inp.get_attribute('name')}")
                    print(f"    id: {inp.get_attribute('id')}")
                    print(f"    placeholder: {inp.get_attribute('placeholder')}")
                return False

            # 로그인 정보 입력
            print(f"\nEntering credentials...")
            username_field.clear()
            username_field.send_keys(username)
            print(f"Username entered: {username}")

            password_field.clear()
            password_field.send_keys(password)
            print("Password entered")

            # 로그인 버튼 찾기
            login_button_selectors = [
                (By.ID, "login"),
                (By.ID, "loginBtn"),
                (By.ID, "submit"),
                (By.NAME, "login"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//input[@type='submit']"),
                (By.XPATH, "//button[contains(text(), '로그인') or contains(text(), 'Login')]")
            ]

            login_button = None
            for by, selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(by, selector)
                    print(f"Found login button with {by}={selector}")
                    break
                except NoSuchElementException:
                    continue

            if login_button:
                login_button.click()
                print("Login button clicked")
                time.sleep(3)

                # 로그인 후 페이지 확인
                self.driver.save_screenshot('/home/user/test_Claude_OnWeb/after_login.png')
                print("After login screenshot saved")

                # 현재 URL 확인
                current_url = self.driver.current_url
                print(f"Current URL after login: {current_url}")

                return True
            else:
                print("Could not find login button")
                # 모든 버튼 출력
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                print(f"\nFound {len(all_buttons)} buttons:")
                for i, btn in enumerate(all_buttons):
                    print(f"  Button {i+1}: {btn.text}, id={btn.get_attribute('id')}")
                return False

        except Exception as e:
            print(f"Error during login: {e}")
            import traceback
            traceback.print_exc()
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_login.png')
            return False

    def navigate_to_new_form(self):
        """새 폼 작성 페이지로 이동"""
        print("\n[Step 3] Navigating to new form page...")
        try:
            # '새 폼 작성' 링크나 버튼 찾기
            possible_selectors = [
                (By.LINK_TEXT, "새 폼 작성"),
                (By.PARTIAL_LINK_TEXT, "새 폼"),
                (By.PARTIAL_LINK_TEXT, "작성"),
                (By.XPATH, "//a[contains(text(), '새 폼') or contains(text(), '작성')]"),
                (By.XPATH, "//button[contains(text(), '새 폼') or contains(text(), '작성')]")
            ]

            for by, selector in possible_selectors:
                try:
                    element = self.driver.find_element(by, selector)
                    print(f"Found new form link/button with {by}={selector}")
                    element.click()
                    time.sleep(3)
                    self.driver.save_screenshot('/home/user/test_Claude_OnWeb/new_form_page.png')
                    return True
                except NoSuchElementException:
                    continue

            print("Could not find '새 폼 작성' button/link")
            # 모든 링크 출력
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            print(f"\nFound {len(all_links)} links:")
            for i, link in enumerate(all_links[:20]):  # 처음 20개만
                print(f"  Link {i+1}: {link.text}, href={link.get_attribute('href')}")

            return False

        except Exception as e:
            print(f"Error navigating to new form: {e}")
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_navigate.png')
            return False

    def fill_form_with_data(self):
        """폼에 데이터 입력"""
        print("\n[Step 4] Filling form with extracted data...")
        try:
            if not self.data:
                print("No data available to fill form")
                return False

            # 페이지 분석
            print("\nAnalyzing form fields...")
            form_fields = self.driver.find_elements(By.TAG_NAME, "input")
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            selects = self.driver.find_elements(By.TAG_NAME, "select")

            print(f"Found {len(form_fields)} input fields, {len(textareas)} textareas, {len(selects)} select fields")

            # 필드 매핑 및 입력 (예시)
            patient_info = self.data.get('patient_info', {})

            # 환자 이니셜 입력 시도
            if 'initials' in patient_info:
                self._try_fill_field('initials', patient_info['initials'])
                self._try_fill_field('patient_initials', patient_info['initials'])

            # 국가 입력
            if 'country' in patient_info:
                self._try_fill_field('country', patient_info['country'])

            # 나이 입력
            if 'age' in patient_info:
                self._try_fill_field('age', patient_info['age'])

            # 성별 입력
            if 'sex' in patient_info:
                self._try_fill_field('sex', patient_info['sex'])
                self._try_fill_field('gender', patient_info['sex'])

            # 스크린샷 저장
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/form_filled.png')
            print("Form filled screenshot saved")

            return True

        except Exception as e:
            print(f"Error filling form: {e}")
            import traceback
            traceback.print_exc()
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_fill.png')
            return False

    def _try_fill_field(self, field_name, value):
        """필드에 값을 입력 시도"""
        selectors = [
            (By.ID, field_name),
            (By.NAME, field_name),
            (By.XPATH, f"//input[@id='{field_name}']"),
            (By.XPATH, f"//input[@name='{field_name}']")
        ]

        for by, selector in selectors:
            try:
                field = self.driver.find_element(by, selector)
                field.clear()
                field.send_keys(str(value))
                print(f"  Filled field '{field_name}' with value '{value}'")
                return True
            except NoSuchElementException:
                continue

        print(f"  Could not find field '{field_name}'")
        return False

    def save_form(self):
        """폼 저장"""
        print("\n[Step 5] Saving form...")
        try:
            # '저장' 버튼 찾기
            save_selectors = [
                (By.ID, "save"),
                (By.ID, "saveBtn"),
                (By.NAME, "save"),
                (By.XPATH, "//button[contains(text(), '저장') or contains(text(), 'Save')]"),
                (By.XPATH, "//input[@type='submit' and contains(@value, '저장')]")
            ]

            for by, selector in save_selectors:
                try:
                    save_button = self.driver.find_element(by, selector)
                    print(f"Found save button with {by}={selector}")
                    save_button.click()
                    time.sleep(3)
                    self.driver.save_screenshot('/home/user/test_Claude_OnWeb/after_save.png')
                    return True
                except NoSuchElementException:
                    continue

            print("Could not find save button")
            return False

        except Exception as e:
            print(f"Error saving form: {e}")
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_save.png')
            return False

    def verify_form_list(self):
        """폼 목록 페이지에서 확인"""
        print("\n[Step 6] Verifying in form list...")
        try:
            # '폼 목록' 페이지로 이동
            list_selectors = [
                (By.LINK_TEXT, "폼 목록"),
                (By.PARTIAL_LINK_TEXT, "목록"),
                (By.XPATH, "//a[contains(text(), '폼 목록') or contains(text(), '목록')]")
            ]

            for by, selector in list_selectors:
                try:
                    list_link = self.driver.find_element(by, selector)
                    print(f"Found form list link with {by}={selector}")
                    list_link.click()
                    time.sleep(3)
                    self.driver.save_screenshot('/home/user/test_Claude_OnWeb/form_list.png')
                    print("Form list page screenshot saved")
                    return True
                except NoSuchElementException:
                    continue

            print("Could not find form list link")
            # 현재 페이지에서 확인
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/verification.png')
            return False

        except Exception as e:
            print(f"Error verifying form: {e}")
            self.driver.save_screenshot('/home/user/test_Claude_OnWeb/error_verify.png')
            return False

    def run_automation(self, pdf_path: str, first_url: str, second_url: str, username: str, password: str):
        """
        전체 자동화 프로세스 실행
        Args:
            pdf_path: PDF 파일 경로
            first_url: 첫 번째 웹사이트 URL
            second_url: 두 번째 웹사이트 URL (MedDRA-DB)
            username: 로그인 ID
            password: 로그인 비밀번호
        """
        try:
            # WebDriver 설정
            self.setup_driver()

            # 1. PDF에서 데이터 로드
            self.load_data_from_pdf(pdf_path)

            # 2. 첫 번째 웹사이트 분석
            if not self.analyze_first_website(first_url):
                print("\nWarning: Failed to analyze first website, continuing...")

            # 3. 두 번째 웹사이트 로그인
            if not self.login_to_meddra_db(second_url, username, password):
                print("\nError: Failed to login to MedDRA-DB")
                return False

            # 4. 새 폼 작성 페이지로 이동
            if not self.navigate_to_new_form():
                print("\nWarning: Failed to navigate to new form page, trying to continue...")

            # 5. 폼에 데이터 입력
            if not self.fill_form_with_data():
                print("\nWarning: Failed to fill form completely")

            # 6. 저장
            if not self.save_form():
                print("\nWarning: Failed to save form")

            # 7. 폼 목록에서 확인
            if not self.verify_form_list():
                print("\nWarning: Failed to verify in form list")

            print("\n" + "=" * 60)
            print("Automation process completed!")
            print("=" * 60)
            print("\nGenerated files:")
            print("  - page1_source.html: First website page source")
            print("  - page1_screenshot.png: First website screenshot")
            print("  - login_page.png: Login page screenshot")
            print("  - after_login.png: After login screenshot")
            print("  - new_form_page.png: New form page screenshot")
            print("  - form_filled.png: Filled form screenshot")
            print("  - after_save.png: After save screenshot")
            print("  - form_list.png: Form list page screenshot")

            return True

        except Exception as e:
            print(f"\nError during automation: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # WebDriver 종료
            if self.driver:
                print("\nClosing browser...")
                time.sleep(3)  # 마지막 확인을 위해 잠시 대기
                self.driver.quit()


def main():
    """메인 함수"""
    print("=" * 60)
    print("MedDRA Form Automation Script")
    print("=" * 60)

    # 설정
    pdf_path = "/home/user/test_Claude_OnWeb/CIOMS-I-Form_example 1.pdf"
    first_url = "https://cjlee-cmd.github.io/MedDRA-Auto-withoutServer/main.html"
    second_url = "https://cjlee-cmd.github.io/MedDRA-DB"
    username = "acuzen"
    password = "acuzen"

    # 자동화 실행
    automation = MedDRAAutomation(headless=False)
    success = automation.run_automation(pdf_path, first_url, second_url, username, password)

    if success:
        print("\nAutomation completed successfully!")
    else:
        print("\nAutomation completed with warnings/errors. Check the screenshots for details.")

    return success


if __name__ == "__main__":
    main()
