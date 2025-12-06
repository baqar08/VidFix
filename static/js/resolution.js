document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("input[name='resolution']");
  if (!input) return;
  const hint = document.createElement("div");
  hint.className = "info-hint";
  input.parentElement.appendChild(hint);
  const presets = {"1920x1080":"Full HD (1080p)","1280x720":"HD (720p)","854x480":"SD (480p)","640x360":"nHD (360p)","426x240":"Low (240p)"};
  const update = () => {
    const v = (input.value || "").trim();
    hint.textContent = presets[v] || (v ? "Custom resolution" : "Enter widthxheight");
  };
  input.addEventListener("input", update);
  update();
});
