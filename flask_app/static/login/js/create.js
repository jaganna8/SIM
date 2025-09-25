// create account
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

    // submit form + error handling
    const createPasswordError = document.getElementById("createpasswordError");
    const repeatPasswordError = document.getElementById("repeatpasswordError");

    const form = document.getElementById('createAccForm');
    if (!form) return;

    form.addEventListener('submit', async function (e) { 
        // check if passwords match
        if (createPasswordInput.value !== repeatPasswordInput.value) {
            createPasswordError.textContent = "Passwords do not match.";
            createPasswordError.style.opacity = 1;
            repeatPasswordError.textContent = "Passwords do not match.";
            repeatPasswordError.style.opacity = 1;
            return;
        }
        else{
            createPasswordError.textContent = "";
            createPasswordError.style.opacity = 0;
            repeatPasswordError.textContent = "";
            repeatPasswordError.style.opacity = 0; 
        }
    });
});