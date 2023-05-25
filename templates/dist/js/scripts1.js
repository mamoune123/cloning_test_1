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



const themes =[
  {
    name: 'comptes et autres',
    image:'/img/duck.png',
  },
  {
    name: 'fable mythe et literature',
    image:'/img/duck.png',
  },
  {
    name: 'heroine et heros',
    image:'/img/duck.png',
  },
  {
    name: 'les animaux',
    image:'/img/duck.png',
  }
];





  
  // Function to generate the HTML structure for the cards
  function generateCardHTML(themes) {
    return `
    
    <div class="cards_item">
    <div class="cardHistoire">
    <a href="comptes.html">
      <img class="card-image" src="${themes.image}" alt="Image" onclick="saveTheme('${themes.name}')">
      </a>
      <div class="card_content">
        <h2 class="card_title">${themes.name}</h2>
      </div>
    </div>
  </div>
 `;
  }
  function saveTheme(themeName) {
    localStorage.setItem('selectedTheme', themeName);
  }
  
  // Function to generate the card container
  function generateCardContainerHTML(themes) {
    return `
      
        ${themes.map(generateCardHTML).join('')}
      
    `;
  }
  
  // Get the container element
  const container = document.getElementById('cardContainer');
  
  // Generate the card container HTML and insert it into the container element
  container.innerHTML = generateCardContainerHTML(themes);
  


