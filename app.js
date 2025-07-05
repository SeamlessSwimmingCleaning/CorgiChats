document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  const input = document.getElementById('message-input');
  const messagesList = document.getElementById('messages');

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    const li = document.createElement('li');
    li.textContent = text;
    messagesList.appendChild(li);
    input.value = '';

    messagesList.scrollTop = messagesList.scrollHeight;
  });
});
