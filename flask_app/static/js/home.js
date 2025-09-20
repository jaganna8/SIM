// filter students on home page
document.addEventListener("DOMContentLoaded", function () {
    const filterButton = document.getElementById("submitFilter");
    if (filterButton) {
        filterButton.addEventListener("click", function (event) {
            event.preventDefault(); // prevent full page reload

            const form = document.querySelector('form');
            const formData = new FormData(form);
            const params = new URLSearchParams(formData).toString();

            fetch(`/filterStudents?${params}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('studentTableBody').innerHTML = html;
                })
                .catch(err => console.error('Error fetching filtered data:', err));
                });
    }
});

// select a student from home page and redirect to student page
document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("studentSelectSubmit");
    const selector = document.getElementById("studentsSelector");

    button.addEventListener("click", function (e) {
        e.preventDefault();

        const studentId = selector.value;
        if (!studentId) {
            alert("Please select a student first.");
            return;
        }

        fetch(`/loadStudentTables?student_id=${studentId}`)
            .then(response => response.json())
            .then(data => {
                document.querySelector("#studentInfoTable tbody").innerHTML = data.student_info;
                document.querySelector("#studentAttendanceTable tbody").innerHTML = data.attendance;
                document.querySelector("#studentClassesTable tbody").innerHTML = data.classes;
                document.querySelector("#studentGradesTable tbody").innerHTML = data.grades;
                document.querySelector(".studentGradTable tbody").innerHTML = data.graduation;
            })
            .catch(err => console.error("Error loading student tables:", err));
    });
});