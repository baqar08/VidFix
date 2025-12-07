document.addEventListener("DOMContentLoaded", () => {
  const start = document.querySelector("input[name='start']");
  const end = document.querySelector("input[name='end']");
  if (!start || !end) return;
  const hint = document.createElement("div");
  hint.className = "info-hint";
  end.parentElement.appendChild(hint);
  const update = () => {
    if (!start.value && !end.value) {
      hint.textContent = "Provide start and end times (seconds or HH:MM:SS).";
      return;
    }
    if (start.value && end.value) hint.textContent = `Trimming: ${start.value} → ${end.value}`;
    else if (start.value) hint.textContent = `Trimming from ${start.value} to end`;
    else hint.textContent = "Start from beginning to specified end time.";
  };
  start.addEventListener("input", update);
  end.addEventListener("input", update);
  update();
});
