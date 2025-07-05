document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messages = document.getElementById('messages');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (text === '') return;

    const li = document.createElement('li');
    li.textContent = text;
    messages.appendChild(li);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
  });
});

