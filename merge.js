document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("input[name='videos']");
    const fileList = document.querySelector(".file-list");

    if (!fileInput || !fileList) return;

    fileInput.addEventListener("change", () => {
        fileList.innerHTML = ""; // Clear current list
        const files = Array.from(fileInput.files);

        if (files.length === 0) {
            fileList.innerHTML = "<li>No files selected</li>";
            return;
        }

        files.forEach((file, index) => {
            const li = document.createElement("li");
            li.textContent = `${index + 1}. ${file.name} (${formatSize(file.size)})`;
            fileList.appendChild(li);
        });
    });

    function formatSize(bytes) {
        if (bytes === 0) return "0 B";
        const k = 1024;
        const sizes = ["B", "KB", "MB", "GB", "TB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    }
});
