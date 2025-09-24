// login
document.addEventListener('DOMContentLoaded', function () {
    const createPasswordToggle = document.getElementById("createPasswordToggle");
    const createPasswordInput = document.getElementById("createPassword");
    const repeatPasswordToggle = document.getElementById("repeatPasswordToggle");
    const repeatPasswordInput = document.getElementById("repeatPassword");


    // Toggle password visibility
    createPasswordToggle.addEventListener("click", () => {
        const type = createPasswordInput.getAttribute("type") === "password" ? "text" : "password";
        createPasswordInput.setAttribute("type", type);
    });
    repeatPasswordToggle.addEventListener("click", () => {
        const type = repeatPasswordInput.getAttribute("type") === "password" ? "text" : "password";
        repeatPasswordInput.setAttribute("type", type);
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