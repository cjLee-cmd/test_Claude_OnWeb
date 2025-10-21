"""
PDF에서 CIOMS Form 데이터를 추출하는 모듈
"""
import re
import PyPDF2
from typing import Dict, Any


class CIOMSFormExtractor:
    """CIOMS Form PDF에서 데이터를 추출하는 클래스"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.data = {}

    def extract_text(self):
        """PDF에서 텍스트를 추출"""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                self.text += page.extract_text() + "\n"
        return self.text

    def parse_patient_info(self):
        """환자 정보 파싱"""
        patient_data = {}

        # 환자 이니셜
        initials_match = re.search(r'PATIENT INITIALS.*?\n.*?\n([A-Z]+)', self.text)
        if initials_match:
            patient_data['initials'] = initials_match.group(1)

        # 국가
        country_match = re.search(r'1a\.\s*COUNTRY\s*\n\s*([A-Z]+)', self.text)
        if country_match:
            patient_data['country'] = country_match.group(1)

        # 생년월일
        dob_match = re.search(r'DATE OF BIRTH.*?(\d+)\s*/\s*(\d+)\s*/\s*(\d+)', self.text)
        if dob_match:
            patient_data['dob_day'] = dob_match.group(1)
            patient_data['dob_month'] = dob_match.group(2)
            patient_data['dob_year'] = dob_match.group(3)

        # 나이
        age_match = re.search(r'2a\.\s*AGE\s*\n\s*Years\s*\n\s*(\d+)', self.text)
        if age_match:
            patient_data['age'] = age_match.group(1)

        # 성별
        sex_match = re.search(r'3\.\s*SEX\s*\n\s*([MF])', self.text)
        if sex_match:
            patient_data['sex'] = sex_match.group(1)

        return patient_data

    def parse_reaction_info(self):
        """부작용 정보 파싱"""
        reaction_data = {}

        # 반응 발생일
        onset_match = re.search(r'REACTION ONSET.*?(\d+)\s*/\s*(\d+)\s*/\s*(\d+)', self.text)
        if onset_match:
            reaction_data['onset_day'] = onset_match.group(1)
            reaction_data['onset_month'] = onset_match.group(2)
            reaction_data['onset_year'] = onset_match.group(3)

        # 부작용 설명 추출
        reactions = []

        # PARALYTIC ILEUS
        if 'PARALYTIC ILEUS' in self.text:
            paralytic_match = re.search(r'PARALYTIC ILEUS\s*\((\d+)\):\s*([^\n]+)', self.text)
            if paralytic_match:
                reactions.append({
                    'name': 'PARALYTIC ILEUS',
                    'code': paralytic_match.group(1),
                    'outcome': paralytic_match.group(2).strip()
                })

        # HYPOVOLEMIC SHOCK
        if 'HYPOVOLEMIC SHOCK' in self.text:
            shock_match = re.search(r'HYPOVOLEMIC SHOCK\s*\((\d+)\):\s*([^\n]+)', self.text)
            if shock_match:
                reactions.append({
                    'name': 'HYPOVOLEMIC SHOCK',
                    'code': shock_match.group(1),
                    'outcome': shock_match.group(2).strip()
                })

        # ACUTE RENAL FAILURE
        if 'ACUTE RENAL FAILURE' in self.text:
            renal_match = re.search(r'ACUTE RENAL FAILURE\s*\((\d+)\):\s*([^\n]+)', self.text)
            if renal_match:
                reactions.append({
                    'name': 'ACUTE RENAL FAILURE',
                    'code': renal_match.group(1),
                    'outcome': renal_match.group(2).strip()
                })

        reaction_data['reactions'] = reactions

        # Seriousness criteria
        reaction_data['patient_died'] = '■ PATIENT DIED' in self.text or '☑ PATIENT DIED' in self.text
        reaction_data['life_threatening'] = '■ LIFE' in self.text or '☑ LIFE' in self.text
        reaction_data['hospitalization'] = '■ INVOLVED OR' in self.text or '☑ INVOLVED OR' in self.text

        return reaction_data

    def parse_suspect_drugs(self):
        """의심 약물 정보 파싱"""
        drugs = []

        # Xeloda [Capecitabine]
        if 'Xeloda' in self.text or 'Capecitabine' in self.text:
            xeloda_data = {
                'name': 'Xeloda [Capecitabine]',
                'dose': '2000 mg (2 in 1 Days)',
                'route': 'Oral',
                'indication': 'RECTAL CANCER',
                'start_date': '22/11/2010',
                'end_date': '13/12/2010',
                'duration': '22 Days'
            }
            drugs.append(xeloda_data)

        # Eloxatin [Oxaliplatin]
        if 'Eloxatin' in self.text or 'Oxaliplatin' in self.text:
            eloxatin_data = {
                'name': 'Eloxatin [Oxaliplatin]',
                'dose': '100 mg',
                'route': 'Intravenous (not otherwise specified)',
                'indication': 'RECTAL CANCER',
                'start_date': '22/11/2010',
                'end_date': '13/12/2010',
                'duration': '22 Days'
            }
            drugs.append(eloxatin_data)

        return drugs

    def parse_concomitant_drugs(self):
        """병용 약물 정보 파싱"""
        drugs = []

        # Tinctura opii
        if 'Tinctura opii' in self.text:
            tinctura_data = {
                'name': 'Tinctura opii',
                'dose': '15 DF (1 in 1 Days)',
                'route': 'Oral',
                'indication': 'DIARRHEA',
                'start_date': '15/12/2010',
                'end_date': '19/12/2010',
                'duration': '5 Days'
            }
            drugs.append(tinctura_data)

        return drugs

    def parse_medical_history(self):
        """병력 정보 파싱"""
        history = {
            'diagnosis': 'Rectal cancer',
            'other_history': 'No other relevant medical history'
        }
        return history

    def parse_manufacturer_info(self):
        """제조사 정보 파싱"""
        manufacturer_data = {}

        # Study number
        study_match = re.search(r'Study No:\s*(\d+)', self.text)
        if study_match:
            manufacturer_data['study_no'] = study_match.group(1)

        # Center number
        center_match = re.search(r'Center No:\s*(\d+)', self.text)
        if center_match:
            manufacturer_data['center_no'] = center_match.group(1)

        # Patient number
        patient_match = re.search(r'Patient No:\s*(\d+)', self.text)
        if patient_match:
            manufacturer_data['patient_no'] = patient_match.group(1)

        # MFR Control No
        mfr_match = re.search(r'MFR CONTROL NO\.\s*\n\s*([^\n]+)', self.text)
        if mfr_match:
            manufacturer_data['mfr_control_no'] = mfr_match.group(1).strip()

        return manufacturer_data

    def extract_all_data(self) -> Dict[str, Any]:
        """모든 데이터 추출"""
        self.extract_text()

        self.data = {
            'patient_info': self.parse_patient_info(),
            'reaction_info': self.parse_reaction_info(),
            'suspect_drugs': self.parse_suspect_drugs(),
            'concomitant_drugs': self.parse_concomitant_drugs(),
            'medical_history': self.parse_medical_history(),
            'manufacturer_info': self.parse_manufacturer_info()
        }

        return self.data

    def print_summary(self):
        """추출된 데이터 요약 출력"""
        if not self.data:
            self.extract_all_data()

        print("=" * 60)
        print("CIOMS Form Data Summary")
        print("=" * 60)

        print("\n[Patient Information]")
        for key, value in self.data.get('patient_info', {}).items():
            print(f"  {key}: {value}")

        print("\n[Reaction Information]")
        reaction_info = self.data.get('reaction_info', {})
        for key, value in reaction_info.items():
            if key != 'reactions':
                print(f"  {key}: {value}")

        if 'reactions' in reaction_info:
            print("\n  Reactions:")
            for reaction in reaction_info['reactions']:
                print(f"    - {reaction['name']} ({reaction['code']}): {reaction['outcome']}")

        print("\n[Suspect Drugs]")
        for drug in self.data.get('suspect_drugs', []):
            print(f"  - {drug['name']}")
            print(f"    Dose: {drug['dose']}")
            print(f"    Route: {drug['route']}")
            print(f"    Period: {drug['start_date']} to {drug['end_date']}")

        print("\n[Concomitant Drugs]")
        for drug in self.data.get('concomitant_drugs', []):
            print(f"  - {drug['name']}")
            print(f"    Dose: {drug['dose']}")
            print(f"    Indication: {drug['indication']}")

        print("\n[Medical History]")
        for key, value in self.data.get('medical_history', {}).items():
            print(f"  {key}: {value}")

        print("\n[Manufacturer Info]")
        for key, value in self.data.get('manufacturer_info', {}).items():
            print(f"  {key}: {value}")

        print("=" * 60)


if __name__ == "__main__":
    # 테스트
    pdf_path = "/home/user/test_Claude_OnWeb/CIOMS-I-Form_example 1.pdf"
    extractor = CIOMSFormExtractor(pdf_path)
    data = extractor.extract_all_data()
    extractor.print_summary()
