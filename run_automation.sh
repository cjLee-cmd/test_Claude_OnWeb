#!/bin/bash

# MedDRA 폼 자동화 실행 스크립트

echo "============================================================"
echo "MedDRA Form Automation Runner"
echo "============================================================"

# 1. 환경 확인
echo ""
echo "[Step 1] Checking environment..."

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Chrome 확인
if command -v google-chrome &> /dev/null; then
    echo "✓ Google Chrome found: $(google-chrome --version)"
elif command -v chromium &> /dev/null; then
    echo "✓ Chromium found: $(chromium --version)"
elif command -v chromium-browser &> /dev/null; then
    echo "✓ Chromium browser found: $(chromium-browser --version)"
else
    echo "⚠ Chrome/Chromium not found. Please install Chrome or Chromium browser."
    echo "  Ubuntu/Debian: sudo apt-get install chromium-browser"
    echo "  macOS: brew install --cask google-chrome"
    echo "  Windows: Download from https://www.google.com/chrome/"
    exit 1
fi

# 2. 패키지 설치
echo ""
echo "[Step 2] Installing required packages..."
pip3 install -r requirements.txt --quiet
echo "✓ Packages installed"

# 3. PDF 추출 테스트
echo ""
echo "[Step 3] Testing PDF extraction..."
python3 test_extraction.py
if [ $? -ne 0 ]; then
    echo "✗ PDF extraction test failed"
    exit 1
fi

# 4. 웹 자동화 실행
echo ""
echo "[Step 4] Running web automation..."
echo "This will open a browser window and perform the following:"
echo "  1. Analyze MedDRA-Auto-withoutServer/main.html"
echo "  2. Login to MedDRA-DB (ID: acuzen, PW: acuzen)"
echo "  3. Navigate to new form page"
echo "  4. Fill form with extracted data"
echo "  5. Save the form"
echo "  6. Verify in form list"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

python3 web_automation.py

echo ""
echo "============================================================"
echo "Automation completed!"
echo "============================================================"
echo ""
echo "Generated files:"
echo "  - extracted_data.json: Extracted data from PDF"
echo "  - page1_screenshot.png: First website screenshot"
echo "  - login_page.png: Login page screenshot"
echo "  - after_login.png: After login screenshot"
echo "  - new_form_page.png: New form page screenshot"
echo "  - form_filled.png: Filled form screenshot"
echo "  - after_save.png: After save screenshot"
echo "  - form_list.png: Form list page screenshot"
echo ""
