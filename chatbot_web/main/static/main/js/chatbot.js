document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const chatSidebar = document.querySelector('.chat-sidebar');
    const chatWrapper = document.querySelector('.chat-wrapper');
    const toggleHistory = document.getElementById('toggle-history');
    const sessionList = document.querySelector('.sidebar-session-list');

    sidebarToggle.addEventListener('click', () => {
        const isSidebarAboutToCollapse = !chatSidebar.classList.contains('collapsed');

        if (isSidebarAboutToCollapse) {
            // --- COLLAPSING THE SIDEBAR ---
            const isHistoryOpen = sessionList.style.maxHeight !== '0px';
            sessionStorage.setItem('chatHistoryWasOpen', isHistoryOpen.toString());

            if (isHistoryOpen) {
                // Collapse history list instantly
                sessionList.style.transition = 'none'; // Disable transition
                sessionList.style.maxHeight = '0px';
                sessionStorage.setItem('chatHistoryOpen', 'false');

                // Re-enable transition after a very short delay to allow DOM to update
                requestAnimationFrame(() => {
                    sessionList.style.transition = 'max-height 0.2s ease-in-out'; // Restore transition
                });
            }

            // Then collapse the sidebar
            chatSidebar.classList.add('collapsed');
            chatWrapper.classList.add('sidebar-collapsed');

        } else {
            // --- EXPANDING THE SIDEBAR ---
            // Expand the sidebar first
            chatSidebar.classList.remove('collapsed');
            chatWrapper.classList.remove('sidebar-collapsed');

            // Listen for the end of the sidebar's transition
            const onSidebarTransitionEnd = () => {
                chatSidebar.removeEventListener('transitionend', onSidebarTransitionEnd);

                const wasHistoryOpen = sessionStorage.getItem('chatHistoryWasOpen') === 'true';
                if (wasHistoryOpen) {
                    // Expand history list after sidebar is expanded
                    sessionList.style.maxHeight = sessionList.scrollHeight + 'px';
                    sessionStorage.setItem('chatHistoryOpen', 'true');
                }
            };
            chatSidebar.addEventListener('transitionend', onSidebarTransitionEnd);
        }
    });

    if (toggleHistory && sessionList) {
        // Check session storage to see if the list should be open
        const isHistoryOpen = sessionStorage.getItem('chatHistoryOpen') === 'true';

        if (isHistoryOpen) {
            // If it was open, expand it on page load
            sessionList.style.maxHeight = sessionList.scrollHeight + 'px';
        } else {
            // Otherwise, keep it collapsed
            sessionList.style.maxHeight = '0px';
        }

        toggleHistory.addEventListener('click', () => {
            const isCurrentlyCollapsed = sessionList.style.maxHeight === '0px';
            if (isCurrentlyCollapsed) {
                // Expand the list
                sessionList.style.maxHeight = sessionList.scrollHeight + 'px';
                sessionStorage.setItem('chatHistoryOpen', 'true');
            } else {
                // Collapse the list
                sessionList.style.maxHeight = '0px';
                sessionStorage.setItem('chatHistoryOpen', 'false');
            }
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
