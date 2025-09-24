// login
document.addEventListener('DOMContentLoaded', function () {
    const passwordToggle = document.getElementById("passwordToggle");
    const passwordInput = document.getElementById("password");
    // Toggle password visibility
    passwordToggle.addEventListener("click", () => {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
    });


    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const params = new URLSearchParams(formData).toString();
        console.log(params)
    });
});