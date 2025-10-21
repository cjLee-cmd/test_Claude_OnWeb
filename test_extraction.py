"""
PDF 추출 기능을 테스트하는 스크립트
"""
import json
from pdf_extractor import CIOMSFormExtractor


def test_pdf_extraction():
    """PDF 추출 테스트"""
    print("=" * 70)
    print("PDF Data Extraction Test")
    print("=" * 70)

    pdf_path = "/home/user/test_Claude_OnWeb/CIOMS-I-Form_example 1.pdf"

    try:
        # PDF 추출기 생성
        extractor = CIOMSFormExtractor(pdf_path)

        # 데이터 추출
        print("\n[Step 1] Extracting data from PDF...")
        data = extractor.extract_all_data()
        print("✓ Data extraction successful!")

        # 요약 출력
        print("\n[Step 2] Displaying extracted data summary...")
        extractor.print_summary()

        # JSON으로 저장
        print("\n[Step 3] Saving data to JSON file...")
        output_file = "/home/user/test_Claude_OnWeb/extracted_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Data saved to: {output_file}")

        # 데이터 검증
        print("\n[Step 4] Validating extracted data...")
        validations = [
            ("Patient country", data.get('patient_info', {}).get('country') == 'GERMANY'),
            ("Patient age", data.get('patient_info', {}).get('age') == '62'),
            ("Patient sex", data.get('patient_info', {}).get('sex') == 'M'),
            ("Number of reactions", len(data.get('reaction_info', {}).get('reactions', [])) == 3),
            ("Number of suspect drugs", len(data.get('suspect_drugs', [])) == 2),
            ("Number of concomitant drugs", len(data.get('concomitant_drugs', [])) == 1),
        ]

        all_passed = True
        for test_name, result in validations:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}: {test_name}")
            if not result:
                all_passed = False

        print("\n" + "=" * 70)
        if all_passed:
            print("All tests PASSED!")
        else:
            print("Some tests FAILED. Please review the extraction logic.")
        print("=" * 70)

        return data

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_pdf_extraction()
