// 샘플 데이터 (10명의 임의 데이터)
const sampleData = [
    { index: 1, name: '김철수', phone: '010-1234-5678', address: '서울시 강남구 테헤란로 123' },
    { index: 2, name: '이영희', phone: '010-2345-6789', address: '서울시 서초구 서초대로 456' },
    { index: 3, name: '박민수', phone: '010-3456-7890', address: '부산시 해운대구 마린시티 789' },
    { index: 4, name: '정수진', phone: '010-4567-8901', address: '인천시 남동구 인주대로 321' },
    { index: 5, name: '최동훈', phone: '010-5678-9012', address: '대전시 유성구 대학로 654' },
    { index: 6, name: '강미래', phone: '010-6789-0123', address: '광주시 서구 상무대로 987' },
    { index: 7, name: '윤서준', phone: '010-7890-1234', address: '대구시 수성구 동대구로 159' },
    { index: 8, name: '임하늘', phone: '010-8901-2345', address: '울산시 남구 삼산로 753' },
    { index: 9, name: '한별이', phone: '010-9012-3456', address: '경기도 성남시 분당구 판교역로 246' },
    { index: 10, name: '송하람', phone: '010-0123-4567', address: '경기도 수원시 영통구 광교중앙로 135' }
];

// DOM 요소들
const sheet1Body = document.getElementById('sheet1Body');
const sheet2Body = document.getElementById('sheet2Body');
const testButton = document.getElementById('testButton');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

// 페이지 로드 시 시트 1에 샘플 데이터 채우기
function initializeSheet1() {
    sheet1Body.innerHTML = '';
    sampleData.forEach(data => {
        const row = createTableRow(data);
        sheet1Body.appendChild(row);
    });
}

// 테이블 행 생성 함수
function createTableRow(data) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${data.index}</td>
        <td>${data.name}</td>
        <td>${data.phone}</td>
        <td>${data.address}</td>
    `;
    return row;
}

// 프로그레스 바 업데이트 함수
function updateProgress(current, total) {
    const percentage = Math.round((current / total) * 100);
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${percentage}% (${current}/${total})`;
}

// 딜레이 함수 (애니메이션 효과를 위해)
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 데이터 복사 함수
async function copyDataFromSheet1ToSheet2() {
    // 버튼 비활성화
    testButton.disabled = true;

    // 시트 2 초기화
    sheet2Body.innerHTML = '';

    // 프로그레스 바 초기화
    updateProgress(0, sampleData.length);

    // 각 행을 순차적으로 복사
    for (let i = 0; i < sampleData.length; i++) {
        const data = sampleData[i];

        // 시트 1에서 현재 복사 중인 행 하이라이트
        const sheet1Rows = sheet1Body.querySelectorAll('tr');
        if (sheet1Rows[i]) {
            sheet1Rows[i].classList.add('copying');
        }

        // 약간의 딜레이 (복사 과정을 시각적으로 보여주기 위해)
        await delay(500);

        // 시트 2에 데이터 추가
        const newRow = createTableRow(data);
        newRow.classList.add('copied');
        sheet2Body.appendChild(newRow);

        // 프로그레스 바 업데이트
        updateProgress(i + 1, sampleData.length);

        // 복사 완료 후 하이라이트 제거
        if (sheet1Rows[i]) {
            sheet1Rows[i].classList.remove('copying');
            sheet1Rows[i].classList.add('copied');
        }

        // 추가된 행의 copied 클래스를 잠시 후 제거
        setTimeout(() => {
            newRow.classList.remove('copied');
        }, 500);
    }

    // 모든 복사가 완료된 후 시트 1의 copied 클래스 제거
    setTimeout(() => {
        const sheet1Rows = sheet1Body.querySelectorAll('tr');
        sheet1Rows.forEach(row => row.classList.remove('copied'));
    }, 1000);

    // 버튼 재활성화
    testButton.disabled = false;

    // 완료 메시지
    alert('데이터 복사가 완료되었습니다!');
}

// Test 버튼 클릭 이벤트 리스너
testButton.addEventListener('click', copyDataFromSheet1ToSheet2);

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    initializeSheet1();
    updateProgress(0, sampleData.length);
});
