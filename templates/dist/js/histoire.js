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



////----------------------------------------Meme principe de la page favoris sauf que cette page meme les histoires non favoris son afficher, et son filter par selection de thèmes

  
  // Function to generate the HTML structure for the cards
  function generateCardHTML(histoire) {
    return `
    
    <div class="cards_item">
    <div class="cardHistoire">
    <label for="${histoire.titre }" class="custom-checkbox">
    <input type="checkbox" ${histoire.is_favori ? 'checked' : ''} value="${histoire.id_histoire}" name="${histoire.titre}" id="${histoire.titre}" 
    onchange="submitForm(event)" 
   />
    <i class="fas fa-star"></i>
    
  </label>
  

        <img class="card-image" src="${histoire.img}">
       
        <div class="card_content">
            <h2 class="card_title">${histoire.titre}</h2>
            <p class="card_text">${histoire.description}</p>
            <button id="${histoire.id_histoire}" class="send-text-btn btn btn-primary" data-text="${histoire.texte}">Get Your Voice</button>
            
        </div>
        
    </div>
    </div>
 `;
  }  
 

  function submitForm(e) {
    e.preventDefault();

    const checkbox = e.target;
    const isFavorite = checkbox.checked; 
    const favoriteId = checkbox.value;
    console.log(favoriteId);
    console.log(isFavorite);
    fetch('/update_favorite', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ favoriteId, isFavorite})
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
    
  }
 
  
  
  // Function to generate the card container
  function generateCardContainerHTML(histoires) {
    return `
      
        ${histoires.map(generateCardHTML).join('')}
      
    `;
  }
  
  // Get the container element
  const container = document.getElementById('cardContainer');
  const selectedTheme = localStorage.getItem('selectedTheme');

// Filter the cards array based on the selected theme name
  
  const histoireTitle = document.getElementById('histoireTitle');

// Set the value of histoireTitle to the selected theme name
  histoireTitle.textContent = selectedTheme;
  // Generate the card container HTML and insert it into the container element



  
  
  
//card send





fetch('/comptes')
  .then(response => response.json())
  .then(data => {
    console.log('Received data:', data); // Add this logging statement
    const histoires = data.histoires; // Update key to 'histoires'
    const filteredHistoires = histoires.filter(histoire => histoire.theme_nom === selectedTheme);
    console.log('Histoires:', histoires);
    // Generate the card container HTML and insert it into the container element
    container.innerHTML = generateCardContainerHTML(filteredHistoires);
    filteredHistoires.forEach((histoire) => {
      const generateBtn = document.getElementById(histoire.id_histoire);
      generateBtn.addEventListener('click', function() {
        const text = histoire.texte;
        localStorage.setItem('storyText', text);
        window.location.href = '/voix1';
      });
    });
  })
  .catch(error => {
    console.error('Error fetching histoires:', error);
  });

  