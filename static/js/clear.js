document.addEventListener("DOMContentLoaded", function() {
    if (window.loggedInStatus === "False") {
        localStorage.removeItem("accordionState");
    }
});