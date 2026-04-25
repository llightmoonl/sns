document.addEventListener("DOMContentLoaded", () => {
    const KEY = "accordionState";
    const accordionBlocks = document.querySelectorAll(".accordion-block");
    const submitButton = document.querySelector('button[type="submit"]');
    function saveState() {
        const state = {};
        accordionBlocks.forEach((block, index) => {
            state[index] = {
                isActive: block.classList.contains("active"),
                isUnlocked: !block.classList.contains("locked")
            };
        });
        localStorage.setItem(KEY, JSON.stringify(state));
    }
    function restoreState() {
        const saved = localStorage.getItem(KEY);
        if (!saved) return;
        const state = JSON.parse(saved);
        accordionBlocks.forEach((block, index) => {
            const blockState = state[index];
            if (!blockState) return;
            if (blockState.isUnlocked) block.classList.remove("locked");
            else block.classList.add("locked");
            if (blockState.isActive) {
                block.classList.add("active");
                const contentEl = block.querySelector(".accordion-content");
                setTimeout(() => {
                    contentEl.style.maxHeight = contentEl.scrollHeight + "px";
                }, 10);
                block.querySelector(".accordion-icon").textContent = "▲";
            }
        });
    }
    function checkButtonState() {
        const allUnlocked = Array.from(accordionBlocks).every(block => !block.classList.contains("locked"));
        if (submitButton) {
            submitButton.disabled = !allUnlocked;
            submitButton.style.opacity = allUnlocked ? "1" : "0.6";
            submitButton.style.cursor = allUnlocked ? "pointer" : "not-allowed";
        }
    }
    accordionBlocks.forEach((block, index) => {
        const header = block.querySelector(".accordion-header");
        const contentEl = block.querySelector(".accordion-content");
        if (index > 0) {
            block.classList.add("locked");
        }
        header.addEventListener("click", () => {
            if (block.classList.contains("locked")) {
                return;
            }
            if (block.classList.contains("active")) {
                block.classList.remove("active");
                contentEl.style.maxHeight = "0";
                block.querySelector(".accordion-icon").textContent = "▼";
                saveState();
                checkButtonState();
                return;
            }
            accordionBlocks.forEach(b => {
                if (b !== block && b.classList.contains("active")) {
                    b.classList.remove("active");
                    b.querySelector(".accordion-icon").textContent = "▼";
                    b.querySelector(".accordion-content").style.maxHeight = "0";
                }
            });
            block.classList.add("active");
            contentEl.style.maxHeight = contentEl.scrollHeight + "px";
            block.querySelector(".accordion-icon").textContent = "▲";
            const currentIndex = Array.from(accordionBlocks).indexOf(block);
            const nextBlockIndex = currentIndex + 1;
            if (nextBlockIndex < accordionBlocks.length) {
                const nextBlock = accordionBlocks[nextBlockIndex];
                nextBlock.classList.remove("locked");
                const isNowUnlockedLast = Array.from(accordionBlocks).slice(nextBlockIndex + 1).every(b => !b.classList.contains("locked"));
                if (isNowUnlockedLast) {
                    checkButtonState();
                }
            }
            saveState();
            checkButtonState();
        });
    });
    document.querySelectorAll(".fullscreen-btn").forEach(button => {
        button.addEventListener("click", function(event) {
             event.stopPropagation(); 
             const imgSrc = this.getAttribute("data-img-src");
             if (imgSrc) {
                 openFullscreenImage(imgSrc);
             }
         });
     });
    restoreState();
    checkButtonState();
});