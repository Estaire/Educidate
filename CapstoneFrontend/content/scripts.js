document.getElementById('course-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form from submitting and reloading the page

    var courseInput = document.getElementById('course-input');
    var courseValue = courseInput.value.trim(); // Get input value and trim whitespace

    if (courseValue) {
        var li = document.createElement('li'); // Create a new list item
        li.textContent = courseValue; // Set text of list item to input value
        document.getElementById('courses-list').appendChild(li); // Add list item to list
        courseInput.value = ''; // Clear input for next entry
    }
});