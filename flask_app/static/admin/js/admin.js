document.addEventListener("DOMContentLoaded", function() {
    const dropdownHeaders = document.querySelectorAll(".dropdown-header");

    dropdownHeaders.forEach(header => {
        header.addEventListener("click", () => {
            const content = header.nextElementSibling; // the form wrapper
            content.classList.toggle("show");
            header.classList.toggle("active"); // rotates the caret
        });
    });
});