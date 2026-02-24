// ===== State =====
const state = {
  workMinutes: 25,
  breakMinutes: 5,
  remaining: 25 * 60,
  isRunning: false,
  isBreak: false,
  sessions: 0,
  interval: null,
};

// ===== Audio Context =====
let audioCtx = null;

function getAudioCtx() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioCtx;
}

function playBeep(frequency, duration, type = "sine", volume = 0.5) {
  const ctx = getAudioCtx();
  const oscillator = ctx.createOscillator();
  const gainNode = ctx.createGain();
  oscillator.connect(gainNode);
  gainNode.connect(ctx.destination);
  oscillator.type = type;
  oscillator.frequency.setValueAtTime(frequency, ctx.currentTime);
  gainNode.gain.setValueAtTime(volume, ctx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
  oscillator.start(ctx.currentTime);
  oscillator.stop(ctx.currentTime + duration);
}

function playStartSound() {
  if (!document.getElementById("sound-start").checked) return;
  playBeep(660, 0.15);
  setTimeout(() => playBeep(880, 0.2), 160);
}

function playEndSound() {
  if (!document.getElementById("sound-end").checked) return;
  playBeep(880, 0.2);
  setTimeout(() => playBeep(660, 0.15), 220);
  setTimeout(() => playBeep(440, 0.4), 400);
}

function playTickSound() {
  if (!document.getElementById("sound-tick").checked) return;
  playBeep(1000, 0.04, "square", 0.15);
}

// ===== Timer Logic =====
function formatTime(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

function updateDisplay() {
  document.getElementById("timer-display").textContent = formatTime(state.remaining);
  document.getElementById("mode-label").textContent = state.isBreak ? "休憩時間" : "作業時間";
  document.title = `${formatTime(state.remaining)} - ${state.isBreak ? "休憩" : "作業"} | ポモドーロ`;
}

function startTimer() {
  if (state.isRunning) return;
  state.isRunning = true;
  playStartSound();
  document.getElementById("btn-start").disabled = true;
  document.getElementById("btn-pause").disabled = false;

  state.interval = setInterval(() => {
    state.remaining--;
    updateDisplay();
    playTickSound();

    if (state.remaining <= 0) {
      clearInterval(state.interval);
      state.isRunning = false;
      playEndSound();

      if (!state.isBreak) {
        state.sessions++;
        document.getElementById("session-count").textContent = state.sessions;
        state.isBreak = true;
        state.remaining = state.breakMinutes * 60;
      } else {
        state.isBreak = false;
        state.remaining = state.workMinutes * 60;
      }

      updateDisplay();
      document.getElementById("btn-start").disabled = false;
      document.getElementById("btn-pause").disabled = true;
    }
  }, 1000);
}

function pauseTimer() {
  if (!state.isRunning) return;
  clearInterval(state.interval);
  state.isRunning = false;
  document.getElementById("btn-start").disabled = false;
  document.getElementById("btn-pause").disabled = true;
}

function resetTimer() {
  clearInterval(state.interval);
  state.isRunning = false;
  state.isBreak = false;
  state.remaining = state.workMinutes * 60;
  updateDisplay();
  document.getElementById("btn-start").disabled = false;
  document.getElementById("btn-pause").disabled = true;
}

// ===== Settings =====
function setActiveButton(groupId, value) {
  document.querySelectorAll(`#${groupId} .opt-btn`).forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.value === String(value));
  });
}

function setWorkTime(minutes) {
  state.workMinutes = minutes;
  setActiveButton("work-options", minutes);
  if (!state.isRunning && !state.isBreak) {
    state.remaining = minutes * 60;
    updateDisplay();
  }
}

function setBreakTime(minutes) {
  state.breakMinutes = minutes;
  setActiveButton("break-options", minutes);
  if (!state.isRunning && state.isBreak) {
    state.remaining = minutes * 60;
    updateDisplay();
  }
}

const THEME_MAP = { ダーク: "dark", ライト: "light", フォーカス: "focus" };

function setTheme(theme) {
  document.getElementById("app-body").className = `theme-${theme}`;
  document.querySelectorAll("#theme-options .opt-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.value === theme);
  });
}

// ===== Init =====
updateDisplay();
