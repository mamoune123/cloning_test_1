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

function extractRelativePath(fullPath) {
  const parentPath = '/Users/mac/Desktop/Cloning_test/templates/dist/';

  // Check if the fullPath starts with the parentPath
  if (fullPath.startsWith(parentPath)) {
    // Extract the relative path by removing the parentPath
    const relativePath = fullPath.substring(parentPath.length);
    return relativePath;
  }

  // Return the fullPath as is if it doesn't start with the parentPath
  return fullPath;
}
//Generation des histoires clonnées
function generateCardHTML(histoire) {
  return `
  
<div class="cards_item">
  <div class="cardHistoire">
  <img class="card-image" src="${histoire.img}">
      <div class="card_content">
          <h2 class="card_title">${histoire.titre}</h2>
          <h2 class="card_text">${histoire.nom_file} crée le ${histoire.date_ajout}</h2>
          
          <button id="${histoire.id_clone}" class="send-text-btn btn btn-primary">Réecouter ?</button>
      </div>
  </div>
</div>
`;
}  
const container = document.getElementById('cardContainer');

function generateCardContainerHTML(histoires) {
  return `
    
      ${histoires.map(generateCardHTML).join('')}
    
  `;
} 
 


fetch('/voice_card')//recolte des histoires clonnées
  .then(response => response.json())
  .then(data => {
    console.log('Received data:', data); // Add this logging statement
    const histoire = data.mes_histoires; // Update key to 'histoires'
    console.log('Histoires:', histoire);
    // Generate the card container HTML and insert it into the container element
    container.innerHTML = generateCardContainerHTML(histoire);
    histoire.forEach((histoire) => {
      const sendButtons = document.getElementById(histoire.id_clone);
      sendButtons.addEventListener('click', function() {
        const cloneID = this.id;
        window.location.href = '/recoute/' + cloneID;
      });
    });

  })
  .catch(error => {
    console.error('Error fetching histoires:', error);
  });

