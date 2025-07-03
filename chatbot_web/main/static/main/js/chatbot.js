// chatbot.js

const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');

chatForm.addEventListener('submit', async () => {
  const msg = userInput.value.trim();
  if (!msg) return;

  // TODO: API 호출 및 응답 처리

  alert(`입력한 메시지: ${msg}`);  // 테스트용 알림

  userInput.value = '';

  
});
