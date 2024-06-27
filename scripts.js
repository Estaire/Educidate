let previousProgressValue = null;

document.addEventListener("DOMContentLoaded", async function() {
    /* Commented out for testing purposes. Remove when successfully integrated with backend
    if (!sessionStorage.getItem('isLoggedIn')) {
        window.location.href = 'FrontPage.html';
    }
    */
    const contentPane = document.getElementById('content-pane');
    const buttons = document.querySelectorAll('.nav-button');
    const navPane = document.getElementById('nav-pane');
    const userAvatar = document.getElementById('userAvatar');
    const profilePopover = document.getElementById('profilePopover');
    const darkModeButton = document.getElementById('darkModeButton');
    const greeting = document.getElementById('greeting');
    const userName = 'User';
    let preferences = [];
    
    const contentFiles = {
        'Progress': './content/progress.html',
        'Majors': './content/majors.html',
        'Minors': './content/minors.html',
        'Electives': './content/electives.html',
        'Logout': './frontpage.html',
        'Sign Up': './content/SignUp.html'
    };

    const loadContent = async (contentFilePath, buttonText) => {
        try {
            if (buttonText === 'Logout') {
                logout();
                return;
            }
            
            buttonText = buttonText || 'Progress';
            const response = await fetch(contentFilePath);
            if (!response.ok) {
                throw new Error('Failed to load content');
            }
            const contentHTML = await response.text();
            
            contentPane.innerHTML = contentHTML;

            if (buttonText === 'Progress' && document.getElementById('progressValue')) {
                updateProgressCircle();
            }

            const newURL = window.location.href.split('?')[0] + `?page=${buttonText.toLowerCase()}`;
            window.history.pushState({path: newURL}, '', newURL);
        } catch (error) {
            console.error(error);
        }
    };
  
    await loadContent('content/progress.html');
  
    navPane.addEventListener('mouseleave', function() {
        this.style.minWidth = '75px';
        this.classList.add('collapsed');
    });
  
    navPane.addEventListener('mouseenter', function() {
        this.classList.remove('collapsed');
        setTimeout(() => {
            this.style.minWidth = '250px';
        }, 300);
    });
  
    buttons.forEach(button => {
        button.addEventListener('click', async function() {
            const buttonText = button.textContent.trim();
            const contentFilePath = contentFiles[buttonText];
            if (buttonText === 'Electives' && preferences.length === 0) {
                await loadContent('content/preferences.html');
                const checkboxes = document.querySelectorAll('.preference');
                const submitButton = document.getElementById('submitBtn');
                const maxPreferences = 3; 
                let selectedCount = 0;

                checkboxes.forEach(checkbox => {
                    checkbox.addEventListener('change', () => {
                        if (checkbox.checked) {
                            selectedCount++;
                        } else {
                            selectedCount--;
                        }
                        checkboxes.forEach(cb => {
                            cb.disabled = selectedCount >= maxPreferences && !cb.checked;
                        });
                    });
                });

                submitButton.addEventListener('click', async () => {
                    const selects = document.querySelectorAll('input[type="checkbox"]:checked');
                    selects.forEach(checkbox => {
                        preferences.push(checkbox.value);
                    });
                    const recommendations = await getRecommendations();
                    const lastThreeElements = recommendations[0].split(',').map(code => code.trim()).slice(-3);
                    await loadContent('content/electives.html')
                    const reselectButton = document.getElementById('reselectBtn');
                    const headingElement = document.getElementById('electives-heading');
                    const electives =  document.getElementById('electives');
                    const heading = headingElement.textContent;
                    headingElement.textContent = '';
                    let chars = heading.split('');

                    chars.forEach((char, index) => {
                        const span = document.createElement('span');
                        span.textContent = (char === ' ') ? '\u00A0' : char; // Use non-breaking space for actual spaces
                        headingElement.appendChild(span);
                    });

                    reselectButton.addEventListener('click', async function() {
                        await loadContent('content/preferences.html');
                    })

                    for (let i = 0; i < 3; i++) {
                        const p = document.createElement('p');
                        p.className = 'block-animation';
                        p.textContent = lastThreeElements[i];
                        electives.appendChild(p);
                        p.style.animationDelay = `${i + 0.5}s`;
                    } 
                })
            } else {
                await loadContent(contentFilePath, buttonText);
            }
        });
    });

    updateProgressCircle();

    function getGreeting() {
        const hour = new Date().getHours();
        if (hour < 12) {
            return `Good Morning, ${userName}`;
        } else if (hour < 18) {
            return `Good Afternoon, ${userName}`;
        } else {
            return `Good Evening, ${userName}`;
        }
    }

    greeting.textContent = getGreeting();

    userAvatar.addEventListener('click', function() {
        profilePopover.style.display = profilePopover.style.display === 'block' ? 'none' : 'block';
    });

    window.addEventListener('click', function(event) {
        if (!event.target.matches('.user-avatar')) {
            profilePopover.style.display = 'none';
        }
    });

    function updateDarkModeButton() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        const icon = darkModeButton.querySelector('i');
        if (isDarkMode) {
            darkModeButton.innerHTML = '<i class="fa-solid fa-sun"></i>Light Mode';
        } else {
            darkModeButton.innerHTML = '<i class="fa-solid fa-moon"></i>Dark Mode';
        }
    }

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        updateDarkModeButton();
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.removeItem('theme');
        }
    }

    darkModeButton.addEventListener('click', toggleDarkMode);

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }

    updateDarkModeButton();
});

function selectOption(button) {
    const buttons = document.querySelectorAll('.nav-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
}

function toggleNavOption(button) {
    button.classList.toggle('active');
}

function login(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'user' && password === 'password') {
        sessionStorage.setItem('isLoggedIn', 'true');

        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid credentials');
    }
}

function logout() {
    const overlay = document.createElement('div');
    overlay.classList.add('white-overlay');
    document.body.appendChild(overlay);

    setTimeout(() => {
        sessionStorage.removeItem('isLoggedIn');
        window.location.href = 'frontpage.html';
    }, 500);
}

function updateProgressCircle() {
    const progressValue = document.getElementById('progressValue');
    if (!progressValue) return;

    const progressCircle = document.querySelector('.progress-ring-fill');
    const percentage = parseFloat(progressValue.innerText);
    const circumference = 2 * Math.PI * progressCircle.r.baseVal.value;
    const dashOffset = circumference * (1 - percentage / 100);

    previousProgressValue = percentage;
    progressCircle.style.strokeDashoffset = dashOffset;

    if (percentage >= 0 && percentage < 25) {
        progressCircle.style.stroke = 'red';
    } else if (percentage >= 25 && percentage < 50) {
        progressCircle.style.stroke = 'orange';
    } else if (percentage >= 50 && percentage < 75) {
        progressCircle.style.stroke = 'yellow';
    } else if (percentage >= 75 && percentage <= 100) {
        progressCircle.style.stroke = 'green';
    }
}

async function getRecommendations() {
    const studentData = {
        "Courses_Completed": ['COMP1126']
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        console.log('Success:', data); 
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null; 
    }
}


                
