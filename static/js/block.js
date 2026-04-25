document.addEventListener("DOMContentLoaded", function () {
    const btnZ2 = document.querySelector('a[data-task="2"]');
    if (btnZ2) {
        if (btnZ2.dataset.z1Passed === "True") {
            btnZ2.classList.remove("btn-locked");
            btnZ2.classList.add("btn");
            btnZ2.style.pointerEvents = "auto";
            btnZ2.style.opacity = "1";
            btnZ2.href = "{{ url_for('zadanie2') }}";
        }
    }
    const btnZ3 = document.querySelector('a[data-task="3"]');
    if (btnZ3) {
        if (btnZ3.dataset.z2Passed === "True") {
            btnZ3.classList.remove("btn-locked");
            btnZ3.classList.add("btn");
            btnZ3.style.pointerEvents = "auto";
            btnZ3.style.opacity = "1";
            btnZ3.href = "{{ url_for('zadanie3') }}";
        }
    }
});