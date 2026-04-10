function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; path=/; expires=${d.toUTCString()}`;
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function deleteCookie(name) {
    document.cookie = `${name}=; Max-Age=-99999999; Path=/`;
}

window.onload = function() {
    if (!getCookie("cookieAccepted")) {
        showCookieBanner();
    }
    const resetLink = document.createElement("a");
    resetLink.href = "#";
    resetLink.textContent = "Вернуть cookie-баннер";
    resetLink.style.position = "fixed";
    resetLink.style.bottom = "0";
    resetLink.style.right = "0";
    resetLink.style.backgroundColor = "#fff";
    resetLink.style.padding = "5px 10px";
    resetLink.style.borderRadius = "4px";
    resetLink.style.boxShadow = "0 0 5px rgba(0,0,0,0.2)";
    resetLink.style.transform = "";
    resetLink.addEventListener("click", function(e) {
        e.preventDefault();
        deleteCookie("cookieAccepted");
        showCookieBanner();
    });
    document.body.appendChild(resetLink);
};

function showCookieBanner() {
    const banner = document.getElementById("cookie-banner");
    banner.style.display = "flex";
    document.getElementById("accept-cookies").addEventListener("click", function() {
        setCookie("cookieAccepted", "true", 365);
        banner.style.display = "none";
    });
}