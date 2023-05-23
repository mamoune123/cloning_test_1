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







// Card data
const cards = [
    {
      name: 'The Lion and the Mouse',
      title: 'Aesop\'s Fables',
      description: 'A lion helps a mouse',
      image: '/img/avataaars.png',
      text: 'Hoy en mi ventana brilla el sol. Y el corazón se pone triste contemplando la ciudad',
      id : '1'
    },
    {
      name: 'The Tortoise and the Hare',
      title: 'Aesop\'s Fables',
      description: 'A slow tortoise wins a race against a fast hare',
      image: '/img/avataaars.png',
      text: 'the tortoise is speedy',
      id : '2'
    },
    {
        name: 'The Boy Who Cried Wolf',
        title: 'Aesop\'s Fables',
        description: 'A boy learns the consequences of lying',
        image: '/img/wolf.jpg',
        text: 'HELP ! HELP ! there is a wolf !',
        id : '3'
      },
      {
        name: 'The Ant and the Grasshopper',
        title: 'Aesop\'s Fables',
        description: 'Creative genius',
        image: '/img/avataaars.png',
        text: 'An ant prepares for winter while a grasshopper enjoys the summer',
        id : '4'
      },
      {
        name: 'The Ugly Duckling',
        title: 'Hans Christian Andersen',
        description: 'A duckling discovers its true identity',
        image: '/img/duck.jpg',
        text: 'duck ! duck ! you are so ugly !',
        id : '5'
      }
    // Add more card objects as needed
  ];
  
  // Function to generate the HTML structure for the cards
  function generateCardHTML(card) {
    return `
      <div class="flip-card">
        <div class="flip-card-inner">
          <div class="flip-card-front">
            <img src="${card.image}" alt="Avatar" style="width:300px;height:300px;border-radius: 60px;">
          </div>
          <div class="flip-card-back">
            <h1>${card.name}</h1>
            <p>${card.title}</p>
            <p>${card.description}</p>
            
            <button id="${card.id}" class="send-text-btn btn btn-primary" data-text="${card.text}">Generate Story</button>
          </div>
        </div>  
      </div>
    `;
  }
  
  // Function to generate the card container
  function generateCardContainerHTML(cards) {
    return `
      <div class="card-container">
        ${cards.map(generateCardHTML).join('')}
      </div>
    `;
  }
  
  // Get the container element
  const container = document.getElementById('cardContainer');
  
  // Generate the card container HTML and insert it into the container element
  container.innerHTML = generateCardContainerHTML(cards);
  



  
  
  
//card send
cards.forEach((card) => {
    const generateBtn = document.getElementById(card.id);
    generateBtn.addEventListener('click', function() {
      const text = card.text;
      send3Data(text);
    });
  });

function send3Data(text) {
  $.ajax({
    type: 'POST',
    url: '/get_data',
    contentType: 'application/json',
    data: JSON.stringify({ text: text }),
    success: function(response) {
      console.log(response);
      window.location.href = 'waiting.html';
    },
    error: function(error) {
      console.log('Error sending data to the server.');
    }
  });
}