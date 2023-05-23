/*!
* Start Bootstrap - Freelancer v7.0.7 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
function handleSelectionChange() {
    var select1 = document.getElementById("Gender");
    var select2 = document.getElementById("select2");
  
    // Check the selected value of select1
    var selectedValue = select1.value;
  
    // Show or hide select2 based on the selected value of select1
    if (selectedValue === "option2") {
      select2.style.display = "block";
    } else {
      select2.style.display = "none";
    }
  }





///-------------



    
    document.getElementById('validate').addEventListener('click', function() {
     var selectedOption1 = document.getElementById('Gender').options[document.getElementById('Gender').selectedIndex].text;
     var selectedOption2 = document.getElementById('Accent').options[document.getElementById('Accent').selectedIndex].text;
      send2Data(selectedOption1,selectedOption2)
      console.log("Sending data to Flask...");
    });

    function send2Data(selectedOption,selectedOption1) {
      $.ajax({
        type: 'POST',
        url: '/save_selection',
        data: { option: selectedOption ,option2: selectedOption1},
        success: function(response) {
          console.log(response);
          // Handle the response from the server
        },
        error: function(error) {
          console.log('Error sending data to the server.');
          // Handle the error condition
        }
      });
    }

function handleGenderChange() {
    var genderSelect = document.getElementById("Gender");
    var languageSection = document.getElementById("languageSection");
  
    if (genderSelect.value === "female" || genderSelect.value === "male") {
      languageSection.style.display = "block";
    } else {
      languageSection.style.display = "none";
    }
  }
  
  function handleLanguageChange() {
    var languageSelect = document.getElementById("Language");
    var accentSection = document.getElementById("accentSection");
  
    if (languageSelect.value === "english") {
      accentSection.style.display = "block";
    } else {
      accentSection.style.display = "none";
    }
    var selectedOption = document.getElementById("Language").value;
  localStorage.setItem("selectedLanguage", selectedOption);
  console.log(selectedOption);
  }
  var micButton = document.getElementById("micButton");
  var isPulsing = false;

  
  
  
  
  
  
