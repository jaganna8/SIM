// tab handler
document.addEventListener("DOMContentLoaded", function () {
    const tabLinks = document.querySelectorAll(".tab-link");
    const tabContents = document.querySelectorAll(".tab-content");

    tabLinks.forEach(link => {
        link.addEventListener("click", () => {
            // Remove active class from all
            tabLinks.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));

            // Add active to clicked and show content
            link.classList.add("active");
            document.getElementById(link.dataset.tab).classList.add("active");
        });
    });
});

// render pie chart for completed credits
function renderGradPieChart(curr, remaining, required) {
    const currCredits = curr;
    const remainingCredits = remaining;
    const requiredCredits = required;

    // Update numbers in the legend
    document.getElementById("creditsEarned").innerText = currCredits;
    document.getElementById("creditsRemaining").innerText = remainingCredits;

    // Calculate percent
    const currPercent = (currCredits/requiredCredits) * 100;
    const remPercent = 100 - currPercent;

    // Style the piechart
    const pie = document.getElementById("creditsPieChart");
    pie.style.background = `conic-gradient(
        #4caf50 0% ${currPercent}%,
        #ddd ${currPercent}% ${remPercent}%
    )`;
}

// select a student on the student page
document.addEventListener("DOMContentLoaded", function () {
    const studentSelectBtn = document.getElementById("studentSelectSubmit");

    function loadStudentData (student_id){
        // Show hidden wrapper
        document.getElementById("studentTablesWrapper").style.display = "block";

        // Fetch tables dynamically
        fetch(`/loadStudentTables?student_id=${student_id}`)
            .then(res => res.json())
            .then(data => {
                document.querySelector("#studentInfoTable").innerHTML = data.student_info;
                document.querySelector("#studentAttendanceTable tbody").innerHTML = data.attendance;
                document.querySelector("#studentClassesTable tbody").innerHTML = data.classes;
                document.querySelector("#studentGradesTable tbody").innerHTML = data.grades;
                document.querySelector("#studentCreditsTable tbody").innerHTML = data.credits;
                document.querySelector("#gpaLabel").innerHTML = `GPA: ${data.gpa}`

                renderGradPieChart(data.curr_credits, data.remaining_credits, data.required_credits);
            })
            .catch(err => console.error("Error loading student data:", err));
    }

    // student selected via dropdown
    if (studentSelectBtn) {
        studentSelectBtn.addEventListener("click", function () {
            const studentId = document.getElementById("studentsSelector").value;

            if (!studentId) {
                alert("Please select a student.");
                return;
            }
            loadStudentData(studentId);
        });
    }

    const pathParts = window.location.pathname.split("/");
    if (pathParts[1] === "student" && pathParts[2]){
        const student_id = pathParts[2];
        loadStudentData(student_id)
    }
 
});

// filter by current classes only on student page
document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("currOnly");

    function loadClasses(){
        const studentId = document.getElementById("studentsSelector").value;
        const checked = checkbox.checked;
        fetch(`/getCurrClasses?student_id=${studentId}&current_only=${checked}`)
        .then(res => res.json())
        .then(data => {
            document.querySelector("#studentClassesTable tbody").innerHTML = data.classes;
        })
        .catch(err => console.error("Error loading classes:", err));
    }

    checkbox.addEventListener("change", loadClasses);
    
});