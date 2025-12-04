document.addEventListener("DOMContentLoaded", () => {


  const forms = document.querySelectorAll(".tool-form");
  forms.forEach(form => {
    const input = form.querySelector("input[type=file]");
    if (!input) return;
    const setHint = () => {
      let hint = form.querySelector(".file-hint");
      if (!hint) {
        hint = document.createElement("div");
        hint.className = "file-hint";
        form.appendChild(hint);
      }
      if (!input.files || input.files.length === 0) hint.textContent = "No file selected";
      else if (input.multiple) hint.textContent = input.files.length + " files selected";
      else hint.textContent = input.files[0].name;
    };

    ["dragenter", "dragover"].forEach(ev => {
      form.addEventListener(ev, (e) => {
        e.preventDefault();
        form.classList.add("dragging");
      });
    });
    ["dragleave", "drop"].forEach(ev => {
      form.addEventListener(ev, (e) => {
        e.preventDefault();
        form.classList.remove("dragging");
      });
    });
    form.addEventListener("drop", (e) => {
      if (e.dataTransfer && e.dataTransfer.files) {
        input.files = e.dataTransfer.files;
        setHint();
      }
    });
    input.addEventListener("change", setHint);
    setHint();
  });
});
