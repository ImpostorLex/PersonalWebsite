// List of topics
const topics = ["Cybersecurity", "PKM", "Portfolio", "Python", "About Me", "Capture the Flag", "Web Development"];

// Function to dynamically generate pills
function generatePills() {
    const containerWidth = document.getElementById('task-list').offsetWidth;
    let currentRow = document.createElement('div');
    document.getElementById('task-list').appendChild(currentRow);
    let currentRowWidth = 0;

    // Loop through topics and create pills
    topics.forEach(topic => {
        // Create pill element
        let pill = document.createElement('span');
        pill.textContent = topic;
        pill.className = 'pills';

        // Append the pill to the current row
        currentRow.appendChild(pill);

        // Update the width of the current row
        currentRowWidth += pill.offsetWidth;

        // Check if the current row is full or needs to be wrapped
        if (currentRowWidth >= containerWidth * 0.9) {
            // Create a new row
            currentRow = document.createElement('div');
            document.getElementById('task-list').appendChild(currentRow);
            currentRowWidth = 0;
        }
    });
}

// Call the function to generate pills
generatePills();