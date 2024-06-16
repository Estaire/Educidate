/*document.getElementById('dropdownButton').addEventListener('click', function() {
    document.getElementById('dropdownContent').classList.toggle('show');
});

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
        var dropdowns = document.getElementsByClassName('dropdown-content');
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
*/
function toggleDropdownItem() {
    var button = document.getElementById('dropdownButton');
    var dropdownContent = document.getElementById('dropdownContent');
    var currentText = button.textContent.trim();
    
    if (currentText.includes('Majors')) {
        button.innerHTML = 'Minors <span class="triangle">&#9660;</span>';
        dropdownContent.innerHTML = '<p onclick="toggleDropdownItem()">Majors</p>';
    } else {
        button.innerHTML = 'Majors <span class="triangle">&#9660;</span>';
        dropdownContent.innerHTML = '<p onclick="toggleDropdownItem()">Minors</p>';
    }
}

function selectOption(button) {
    const buttons = document.querySelectorAll('.nav-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
}

document.addEventListener("DOMContentLoaded", function() {
    const contentPane = document.getElementById('content-pane');
    const buttons = document.querySelectorAll('.nav-button');

    const contentFiles = {
        'Progress': './content/progress.html',
        'Majors': './content/majors.html',
        'Minors': './content/minors.html',
        'Electives': './content/electives.html'
    };

    buttons.forEach(button => {
        button.addEventListener('click', async function() {
            const buttonText = button.textContent.trim();
            const contentFilePath = contentFiles[buttonText];
            
            try {

                const response = await fetch(contentFilePath);
                if (!response.ok) {
                    throw new Error('Failed to load content');
                }
                const contentHTML = await response.text();
                
                contentPane.innerHTML = contentHTML;

                const newURL = window.location.href.split('?')[0] + `?page=${buttonText.toLowerCase()}`;
                window.history.pushState({path: newURL}, '', newURL);
            } catch (error) {
                console.error(error);
            }
        });
    });
});

function toggleNavOption(button) {
    button.classList.toggle('active');
}

const navPane = document.getElementById('nav-pane');

navPane.addEventListener('mouseleave', function() {
    this.classList.add('collapsed');
});

navPane.addEventListener('mouseenter', function() {
    this.classList.remove('collapsed');
});
