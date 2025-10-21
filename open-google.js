const puppeteer = require('puppeteer');

(async () => {
  console.log('Chrome 브라우저를 시작합니다...');

  // 브라우저 실행 (headless 모드)
  const browser = await puppeteer.launch({
    headless: true,  // GUI 없는 환경에서 실행
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  console.log('새 페이지를 생성합니다...');
  const page = await browser.newPage();

  // 뷰포트 설정
  await page.setViewport({ width: 1280, height: 800 });

  console.log('구글 홈페이지로 이동합니다...');
  await page.goto('https://www.google.com', {
    waitUntil: 'networkidle0'
  });

  console.log('구글 홈페이지가 성공적으로 열렸습니다!');

  // 스크린샷 저장
  const screenshotPath = 'google-homepage.png';
  await page.screenshot({
    path: screenshotPath,
    fullPage: false
  });
  console.log(`스크린샷이 ${screenshotPath}에 저장되었습니다.`);

  // 페이지 제목 출력
  const title = await page.title();
  console.log(`페이지 제목: ${title}`);

  // URL 확인
  const url = page.url();
  console.log(`현재 URL: ${url}`);

  // 브라우저 종료
  await browser.close();
  console.log('브라우저가 종료되었습니다.');
})();
