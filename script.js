document.addEventListener("DOMContentLoaded", function () {

    const addForm = document.getElementById("addCandidateForm");

    if (addForm) {
        addForm.addEventListener("submit", function (event) {
            const class10 = parseFloat(document.getElementById("class10").value);
            const class12 = parseFloat(document.getElementById("class12").value);
            const cgpa = parseFloat(document.getElementById("cgpa").value);
            const projects = parseInt(document.getElementById("projects").value);
            const hackathons = parseInt(document.getElementById("hackathons_count").value);
            const leetcode = parseInt(document.getElementById("leetcode").value);
            const codechef = parseInt(document.getElementById("codechef").value);
            const hackerrank = parseInt(document.getElementById("hackerrank").value);

            if (class10 < 0 || class10 > 100) {
                alert("Class 10 percentage must be between 0 and 100.");
                event.preventDefault();
                return;
            }

            if (class12 < 0 || class12 > 100) {
                alert("Class 12 percentage must be between 0 and 100.");
                event.preventDefault();
                return;
            }

            if (cgpa < 0 || cgpa > 10) {
                alert("CGPA must be between 0 and 10.");
                event.preventDefault();
                return;
            }

            if (projects < 0) {
                alert("Projects cannot be negative.");
                event.preventDefault();
                return;
            }

            if (hackathons < 0) {
                alert("Hackathons count cannot be negative.");
                event.preventDefault();
                return;
            }

            if (leetcode < 0 || codechef < 0 || hackerrank < 0) {
                alert("Coding scores cannot be negative.");
                event.preventDefault();
                return;
            }
        });
    }

    const skills = document.getElementById("skills");

    if (skills) {
        skills.addEventListener("blur", function () {
            let arr = skills.value.split(",");
            arr = arr.map(s => s.trim().toLowerCase()).filter(s => s);
            skills.value = arr.join(", ");
        });
    }

    const filterForm = document.getElementById("filterForm");

    if (filterForm) {
        filterForm.addEventListener("submit", function (event) {
            if (!confirm("Apply filter and rank candidates?")) {
                event.preventDefault();
            }
        });
    }

});