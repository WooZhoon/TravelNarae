document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const chatSidebar = document.querySelector('.chat-sidebar');
    const chatWrapper = document.querySelector('.chat-wrapper');
    const chatBox = document.getElementById('chatBox'); // chatBox 요소 가져오기

    sidebarToggle.addEventListener('click', () => {
        chatSidebar.classList.toggle('collapsed');
        chatWrapper.classList.toggle('sidebar-collapsed');
    });

    // 초기 로드 시 스크롤을 맨 아래로
    chatBox.scrollTop = chatBox.scrollHeight;
});

console.log('chatbot.js loaded successfully!');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // 폼 제출 방지

  const msg = userInput.value.trim();
  if (!msg) return;

  appendMessage('user', msg);
  userInput.value = '';

  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // CSRF 토큰 추가
      },
      body: JSON.stringify({ message: msg })
    });

    const data = await response.json();
    console.log('Received response:', data); // 디버깅 로그 추가
    appendMessage('bot', data.reply);
  } catch (error) {
    console.error('Error sending message:', error);
    appendMessage('bot', '메시지를 보내는 중 오류가 발생했습니다.');
  }
});

function appendMessage(sender, message) {
  console.log(`Appending message: [${sender}] ${message}`); // 디버깅 로그 추가
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);
  
  // chatBox 스크롤을 맨 아래로
  chatBox.scrollTop = chatBox.scrollHeight;
}

// CSRF 토큰을 가져오는 함수 (Django 문서에서 권장하는 방식)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}