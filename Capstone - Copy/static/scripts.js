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
    
    const contentFiles = {
        'Progress': './content/progress.html',
        'Majors': './content/majors.html',
        'Minors': './content/minors.html',
        'Electives': './content/electives.html',
        'Logout': './frontpage.html'
    };

    const loadContent = async (contentFilePath, buttonText) => {
      try {
        buttonText = buttonText || 'Progress';
        const response = await fetch(contentFilePath);
        if (!response.ok) {
          throw new Error('Failed to load content');
        }
        const contentHTML = await response.text();
        
        contentPane.innerHTML = contentHTML;

        if (buttonText === 'Progress') {
            updateProgressCircle();
        }
        else if (buttonText === 'Logout'){
            logout();
        }
  
        const newURL = window.location.href.split('?')[0] + `?page=${buttonText.toLowerCase()}`;
        window.history.pushState({path: newURL}, '', newURL);
      } catch (error) {
        console.error(error);
      }
    };
  
    //await loadContent("content/progress.html");
  
    navPane.addEventListener('mouseleave', function() {
      this.classList.add('collapsed');
    });
  
    navPane.addEventListener('mouseenter', function() {
      this.classList.remove('collapsed');
    });
  
    /*buttons.forEach(button => {
      button.addEventListener('click', async function() {
        const buttonText = button.textContent.trim();
        const contentFilePath = contentFiles[buttonText];
        await loadContent(contentFilePath, buttonText);
      });
    });*/

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

function logout(){
    sessionStorage.removeItem('isLoggedIn');
    
    window.location.href = 'frontpage.html';
}

function updateProgressCircle() {
    const progressValue = document.getElementById('progressValue');
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