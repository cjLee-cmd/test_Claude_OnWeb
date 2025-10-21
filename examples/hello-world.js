/**
 * Hello World 예제
 *
 * 가장 기본적인 예제 코드입니다.
 */

function helloWorld() {
  console.log('안녕하세요, test_Claude_OnWeb!');
}

function main() {
  helloWorld();
  console.log('이것은 예제 코드입니다.');
}

// 모듈로 사용할 경우
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { helloWorld };
}

// 직접 실행할 경우
if (require.main === module) {
  main();
}
