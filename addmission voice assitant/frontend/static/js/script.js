/* =========================================================
   COLLEGE ADMISSION ASSISTANT – FULL JS (UPDATED)
   - Theme Toggle (Persistent)
   - Chatbot (Backend Connected)
   - Voice Input (Speech → Text)
   - Voice Output (Text → Speech)
   - Safe for All Pages
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  /* ================= THEME TOGGLE ================= */
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");

  if (themeToggle) {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      body.classList.add("dark");
      themeToggle.textContent = "☀️";
    }

    themeToggle.addEventListener("click", () => {
      body.classList.toggle("dark");
      const isDark = body.classList.contains("dark");
      themeToggle.textContent = isDark ? "☀️" : "🌙";
      localStorage.setItem("theme", isDark ? "dark" : "light");
    });
  }

  /* ================= VOICE SETTINGS ================= */
  const voiceToggle = document.getElementById("voiceToggle");
  let voiceEnabled = localStorage.getItem("voice") === "on";

  if (voiceToggle && voiceEnabled) {
    voiceToggle.classList.add("active");
  }

  /* ================= TEXT TO SPEECH ================= */
  function speak(text) {
    if (!voiceEnabled || !("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = "en-IN";
    msg.rate = 0.95;
    speechSynthesis.speak(msg);
  }

  /* ================= SPEECH TO TEXT ================= */
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;

  if (recognition) {
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;
  }

  /* ================= CHAT ELEMENTS ================= */
  const chatBody = document.getElementById("chatBody");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  /* ================= CHAT UI HELPERS ================= */
  function scrollChat() {
    if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;
  }

  function userBubble(text) {
    if (!chatBody) return;
    const div = document.createElement("div");
    div.className = "msg user";
    div.textContent = text;
    chatBody.appendChild(div);
    scrollChat();
  }

  function typingBubble() {
    if (!chatBody) return;
    const div = document.createElement("div");
    div.className = "msg bot typing";
    div.id = "typing";
    div.textContent = "AI is typing…";
    chatBody.appendChild(div);
    scrollChat();
  }

  function removeTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
  }

  function botBubble(text) {
    removeTyping();
    if (!chatBody) return;
    const div = document.createElement("div");
    div.className = "msg bot";
    div.textContent = text;
    chatBody.appendChild(div);
    scrollChat();
    speak(text);
  }

  /* ================= BACKEND CHAT ================= */
  async function sendToBackend(message) {
    typingBubble();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      botBubble(data.reply || "Sorry, I did not understand.");

    } catch (error) {
      botBubble("Server error. Please try again later.");
    }
  }

  /* ================= SEND MESSAGE ================= */
  function sendMessage() {
    if (!userInput) return;
    const text = userInput.value.trim();
    if (!text) return;

    userInput.value = "";
    userBubble(text);
    sendToBackend(text);
  }

  if (sendBtn) sendBtn.addEventListener("click", sendMessage);

  if (userInput) {
    userInput.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  /* ================= MIC TOGGLE ================= */
  if (voiceToggle) {
    voiceToggle.addEventListener("click", () => {
      voiceEnabled = !voiceEnabled;
      localStorage.setItem("voice", voiceEnabled ? "on" : "off");
      voiceToggle.classList.toggle("active");

      if (!recognition) {
        alert("Speech recognition is not supported in this browser.");
        return;
      }

      if (voiceEnabled) {
        recognition.start();
        speak("Listening");
      } else {
        recognition.stop();
        speechSynthesis.cancel();
      }
    });
  }

  /* ================= MIC RESULT ================= */
  if (recognition) {
    recognition.onresult = event => {
      const text = event.results[0][0].transcript;
      userBubble(text);
      sendToBackend(text);
    };

    recognition.onerror = () => {
      botBubble("Sorry, I could not understand your voice.");
    };
  }

  /* ================= WELCOME MESSAGE ================= */
  if (chatBody) {
    setTimeout(() => {
      botBubble(
        "Hello 👋 I am your AI Admission Assistant. You can ask me about courses, fees, eligibility, or the admission process."
      );
    }, 600);
  }

});
