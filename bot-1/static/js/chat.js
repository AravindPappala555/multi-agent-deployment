const messagesEl = document.getElementById('messages');
const containerEl = document.getElementById('messagesContainer');
const inputEl = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const welcomeSplash = document.getElementById('welcomeSplash');

let conversationHistory = [];
let isThinking = false;
let splashRemoved = false;

/* ── Helpers ─────────────────────────────────────── */
function getTime() {
  return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

function removeSplash() {
  if (!splashRemoved && welcomeSplash) {
    welcomeSplash.style.transition = 'opacity 0.4s ease';
    welcomeSplash.style.opacity = '0';
    setTimeout(() => { welcomeSplash.remove(); splashRemoved = true; }, 400);
  }
}

function scrollToBottom() {
  containerEl.scrollTo({ top: containerEl.scrollHeight, behavior: 'smooth' });
}

/* ── Append a message row ────────────────────────── */
function appendMessage(role, text) {
  removeSplash();
  const row = document.createElement('div');
  row.className = `msg-row ${role === 'assistant' ? '' : 'user-row'}`;

  const avatar = document.createElement('div');
  avatar.className = `msg-avatar ${role === 'assistant' ? 'bot-avatar' : 'user-avatar'}`;
  avatar.textContent = role === 'assistant' ? 'AI' : 'You';

  const content = document.createElement('div');
  content.className = 'msg-content';

  const bubble = document.createElement('div');
  bubble.className = `bubble ${role === 'assistant' ? 'bot-bubble' : 'user-bubble'}`;
  bubble.textContent = text;

  const time = document.createElement('div');
  time.className = 'msg-time';
  time.textContent = getTime();

  content.appendChild(bubble);
  content.appendChild(time);
  row.appendChild(avatar);
  row.appendChild(content);
  messagesEl.appendChild(row);
  scrollToBottom();
  return bubble;
}

/* ── Typing indicator ─────────────────────────────── */
function showTyping() {
  const row = document.createElement('div');
  row.className = 'typing-row';
  row.id = 'typingRow';

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar bot-avatar';
  avatar.textContent = 'AI';

  const bubble = document.createElement('div');
  bubble.className = 'typing-bubble';
  bubble.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

  row.appendChild(avatar);
  row.appendChild(bubble);
  messagesEl.appendChild(row);
  scrollToBottom();
}

function removeTyping() {
  const t = document.getElementById('typingRow');
  if (t) t.remove();
}

/* ── Send message ─────────────────────────────────── */
async function sendMessage(text) {
  text = text.trim();
  if (!text || isThinking) return;

  isThinking = true;
  sendBtn.disabled = true;
  inputEl.value = '';
  inputEl.style.height = 'auto';
  sendBtn.disabled = true;

  appendMessage('user', text);
  conversationHistory.push({ role: 'user', content: text });
  showTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: conversationHistory })
    });
    const data = await res.json();
    removeTyping();

    const reply = data.reply || "I'm sorry, I couldn't process that. Please try again.";
    conversationHistory.push({ role: 'assistant', content: reply });
    appendMessage('assistant', reply);
  } catch (err) {
    removeTyping();
    appendMessage('assistant', 'Something went wrong. Please check your connection and try again.');
  }

  isThinking = false;
  sendBtn.disabled = inputEl.value.trim().length === 0;
  inputEl.focus();
}

/* ── Greeting on load ─────────────────────────────── */
async function loadGreeting() {
  showTyping();
  try {
    const res = await fetch('/api/greeting');
    const data = await res.json();
    removeTyping();
    const greeting = data.reply || "Welcome to Rasool Khan Real Estate Services! I'm Aira, your personal property advisor. May I know your name to get started?";
    conversationHistory.push({ role: 'user', content: 'Begin the conversation.' });
    conversationHistory.push({ role: 'assistant', content: greeting });
    appendMessage('assistant', greeting);
  } catch (e) {
    removeTyping();
    const fallback = "Welcome to Rasool Khan Real Estate Services! I'm Aira, your personal property advisor. May I know your name to get started?";
    conversationHistory.push({ role: 'assistant', content: fallback });
    appendMessage('assistant', fallback);
  }
}

/* ── Clear / new conversation ─────────────────────── */
clearBtn.addEventListener('click', () => {
  conversationHistory = [];
  splashRemoved = false;
  messagesEl.innerHTML = `
    <div class="welcome-splash" id="welcomeSplash">
      <div class="welcome-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <h2>Find your perfect home</h2>
      <p>Aira will guide you through a personalised property search, tailored to your lifestyle and budget.</p>
    </div>`;
  loadGreeting();
});

/* ── Input handling ──────────────────────────────── */
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
  sendBtn.disabled = inputEl.value.trim().length === 0 || isThinking;
});

inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) sendMessage(inputEl.value);
  }
});

sendBtn.addEventListener('click', () => sendMessage(inputEl.value));

/* ── Quick chips ─────────────────────────────────── */
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const msg = chip.dataset.msg;
    if (msg && !isThinking) sendMessage(msg);
  });
});

/* ── Boot ─────────────────────────────────────────── */
loadGreeting();
