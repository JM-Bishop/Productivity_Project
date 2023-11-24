// Get all the play/pause buttons
var buttons = document.querySelectorAll('.play-pause');

// Add event listeners to the buttons
buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        // Get the progress bar for this task
        var progressBar = this.nextElementSibling.querySelector('.progress');

        // Start or pause the timer
        if (this.textContent === 'Play') {
            this.textContent = 'Pause';
            // Start the timer
        } else {
            this.textContent = 'Play';
            // Pause the timer
        }
    });
});