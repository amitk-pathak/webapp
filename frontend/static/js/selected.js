// results.js

// JavaScript to handle row selection and show details
const table = document.getElementById("results-table");
const showDetailsBtn = document.getElementById("show-details-btn");
const detailsSection = document.getElementById("details-section");
const detailName = document.getElementById("detail-name");
const detailTitle = document.getElementById("detail-title");

let selectedRow = null;

// Add click event listener to each row
table.querySelectorAll("tbody tr").forEach(row => {
    row.addEventListener("click", () => {
        // Remove 'selected' class from previously selected row
        if (selectedRow) {
            selectedRow.classList.remove("selected");
        }

        // Add 'selected' class to the clicked row
        row.classList.add("selected");
        selectedRow = row;

        // Enable the "Show Details" button
        showDetailsBtn.disabled = false;
    });
});

// Add click event listener to the "Show Details" button
showDetailsBtn.addEventListener("click", () => {
    if (selectedRow) {
        // Get data from the selected row
        const name = selectedRow.getAttribute("data-name");
        const title = selectedRow.getAttribute("data-title");

        // Display the details in the details section
        detailName.textContent = name;
        detailTitle.textContent = title;

        // Show the details section
        detailsSection.style.display = "block";
    }
});