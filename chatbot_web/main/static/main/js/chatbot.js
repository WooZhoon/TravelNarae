document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const chatSidebar = document.querySelector('.chat-sidebar');
    const chatWrapper = document.querySelector('.chat-wrapper');

    sidebarToggle.addEventListener('click', () => {
        chatSidebar.classList.toggle('collapsed');
        chatWrapper.classList.toggle('sidebar-collapsed');
    });

    const toggleHistory = document.getElementById('toggle-history');
    const sessionList = document.querySelector('.sidebar-session-list');

    if (toggleHistory && sessionList) {
        // 초기에 목록을 숨김
        sessionList.style.display = 'none';
        toggleHistory.addEventListener('click', () => {
            sessionList.style.display = sessionList.style.display === 'none' ? 'block' : 'none';
        });
    }

    // ✅ 페이지 전체를 아래로 자동 스크롤
    scrollToBottom();
});

console.log('chatbot.js loaded successfully!');

const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMain = document.querySelector('.chat-main');

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
    console.log('Received response:', data);
    appendMessage('assistant', data.reply);
  } catch (error) {
    console.error('Error sending message:', error);
    appendMessage('assistant', '메시지를 보내는 중 오류가 발생했습니다.');
  }
});

function appendMessage(sender, message) {
  console.log(`Appending message: [${sender}] ${message}`);
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  messageElement.textContent = message;
  chatMain.appendChild(messageElement);

  // ✅ 페이지 전체를 아래로 자동 스크롤
  scrollToBottom();
}

function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
