document.addEventListener("DOMContentLoaded", () => {
  const crf = document.querySelector("input[name='crf']");
  if (!crf) return;
  const hint = document.createElement("div");
  hint.className = "info-hint";
  crf.parentElement.appendChild(hint);
  const update = () => {
    const v = Number(crf.value);
    if (v <= 18) hint.textContent = "Ultra high quality — larger file";
    else if (v <= 23) hint.textContent = "High quality (recommended)";
    else if (v <= 30) hint.textContent = "Balanced size vs quality";
    else hint.textContent = "High compression — smaller file";
  };
  crf.addEventListener("input", update);
  update();
});
