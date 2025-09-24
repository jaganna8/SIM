document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('create-account-form');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Simple client-side validation (example)
        if (!data.username || !data.password || !data.email) {
            alert('Please fill out all required fields.');
            return;
        }

        
    });
});