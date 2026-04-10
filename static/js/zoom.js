function openFullscreenImage(imgSrc) {
    const overlay = document.createElement("div");
    overlay.id = "image-overlay";
    overlay.style.position = "fixed";
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = "100vw";
    overlay.style.height = "100vh";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.9)";
    overlay.style.display = "flex";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";
    overlay.style.zIndex = "1001";
    overlay.style.cursor = "zoom-out";
    const container = document.createElement("div");
    container.style.position = "relative";
    container.style.width = "100%";
    container.style.height = "100%";
    container.style.maxWidth = "100vw";
    container.style.maxHeight = "100vh";
    const closeBtn = document.createElement("span");
    closeBtn.textContent = "×";
    closeBtn.style.position = "absolute";
    closeBtn.style.top = "20px";
    closeBtn.style.right = "20px";
    closeBtn.style.color = "#fff";
    closeBtn.style.fontSize = "40px";
    closeBtn.style.cursor = "pointer";
    closeBtn.style.zIndex = "1002";
    const img = document.createElement("img");
    img.src = imgSrc;
    img.alt = "Увеличенное изображение";
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "contain";
    img.style.border = "none";
    closeBtn.onclick = function() {
        document.body.removeChild(overlay);
        const originalImg = document.querySelector(`img[src="${imgSrc}"]`);
        if (originalImg) {
            originalImg.classList.remove("zoomed");
        }
    };
    overlay.onclick = function(event) {
        if (event.target === overlay) {
            document.body.removeChild(overlay);
            const originalImg = document.querySelector(`img[src="${imgSrc}"]`);
            if (originalImg) {
                originalImg.classList.remove("zoomed");
            }
        }
    };
    container.appendChild(img);
    overlay.appendChild(closeBtn);
    overlay.appendChild(container);
    document.body.appendChild(overlay);
}