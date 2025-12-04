document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("input[name='factor']");
  if (!input) return;
  const hint = document.createElement("div");
  hint.className = "info-hint";
  input.parentElement.appendChild(hint);
  const update = () => {
    const v = parseFloat(input.value);
    if (isNaN(v)) { hint.textContent = ""; return; }
    if (v > 1) hint.textContent = `Video will play ${v}x faster.`;
    else if (v < 1) hint.textContent = `Video will play ${(1/v).toFixed(1)}x slower.`;
    else hint.textContent = "Normal speed.";
  };
  input.addEventListener("input", update);
  update();
});
