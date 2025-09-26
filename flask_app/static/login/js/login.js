// login
document.addEventListener('DOMContentLoaded', function () {
    const passwordToggle = document.getElementById("passwordToggle");
    const passwordInput = document.getElementById("password");
    // Toggle password visibility
    passwordToggle.addEventListener("click", () => {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
    });
});