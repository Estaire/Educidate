document.getElementById('button').addEventListener('click', function(e) {
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

document.getElementById('complete-button').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent form from submitting and reloading the page

    var courses = [];
    var listItems = document.querySelectorAll('#courses-list li');

    listItems.forEach(function(item) {
        courses.push(item.textContent);
    });

    fetch('/courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ courses: courses })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Optionally, handle the response data
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
