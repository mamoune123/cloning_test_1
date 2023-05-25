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








const cards = [
    {
      name: 'The Lion and the Mouse',
      title: 'Aesop\'s Fables',
      description: 'A lion helps a mouse',
      image: '/img/avataaars.png',
      text: 'Hoy en mi ventana brilla el sol. Y el corazón se pone triste contemplando la ciudad',
      id : '1',
      themes :'fable mythe et literature',
      favorite: false
    },
    {
      name: 'The Tortoise and the Hare',
      title: 'Aesop\'s Fables',
      description: 'A slow tortoise wins a race against a fast hare',
      image: '/img/avataaars.png',
      text: 'the tortoise is speedy',
      id : '2',
      themes :'heroine et heros',
      favorite: false
    },
    {
        name: 'The Boy Who Cried Wolf',
        title: 'Aesop\'s Fables',
        description: 'A boy learns the consequences of lying',
        image: '/img/wolf.jpg',
        text: 'HELP ! HELP ! there is a wolf !',
        id : '3',
        themes :'les animaux',
        favorite: false
      },
      {
        name: 'The Ant and the Grasshopper',
        title: 'Aesop\'s Fables',
        description: 'Creative genius',
        image: '/img/avataaars.png',
        text: 'An ant prepares for winter while a grasshopper enjoys the summer',
        id : '4',
        themes :'comptes et autres',
        favorite: false
      },
      {
        name: 'The Ugly Duckling',
        title: 'Hans Christian Andersen',
        description: 'A duckling discovers its true identity',
        image: '/img/duck.jpg',
        text: 'duck ! duck ! you are so ugly !',
        id : '5',
        themes :'comptes et autres',
        favorite: false
      },
      {
        name: 'The Little Mermaid',
        title: 'Hans Christian Andersen',
        description: 'A young mermaid\'s sacrifice for love',
        image: '/img/duck.png',
        text: 'Under the sea, a magical tale unfolds',
        id: '6',
        themes: 'les animaux',
        favorite: false
      },
      {
        name: 'Cinderella',
        title: 'Charles Perrault',
        description: 'A girl\'s journey from rags to riches',
        image: '/img/duck.png',
        text: 'With glass slippers, dreams come true',
        id: '7',
        themes: 'heroine et heros',
        favorite: false
      },
      {
        name: 'Rapunzel',
        title: 'Brothers Grimm',
        description: 'A girl with long, golden hair locked in a tower',
        image: '/img/duck.png',
        text: 'Let down your hair, let\'s embark on an adventure',
        id: '8',
        themes: 'fable mythe et literature',
        favorite: false
      }
      
    // Add more card objects as needed
  ];
  
  // Function to generate the HTML structure for the cards
  function generateCardHTML(card) {
    return `
    
    <div class="cards_item">
    <div class="cardHistoire">
    <label for="${card.name }" class="custom-checkbox">
    <input type="checkbox" id="${card.name}" ${card.favorite ? 'checked' : ''}/>
    <i class="glyphicon glyphicon-star-empty"></i>
    <i class="glyphicon glyphicon-star"></i>
  </label>
        <img class="card-image" src="https://picsum.photos/500/300/?image=10">
       
        <div class="card_content">
            <h2 class="card_title">${card.name}</h2>
            <p class="card_text">${card.description}</p>
            <button id="${card.id}" class="send-text-btn btn btn-primary" data-text="${card.text}">Generate Story</button>
            
        </div>
        
    </div>
    </div>
  
 
 `;
  }
  
  // Function to generate the card container
  function generateCardContainerHTML(cards) {
    return `
      
        ${cards.map(generateCardHTML).join('')}
      
    `;
  }
  
  // Get the container element
  const container = document.getElementById('cardContainer');
  const selectedTheme = localStorage.getItem('selectedTheme');

// Filter the cards array based on the selected theme name
  const filteredCards = cards.filter(card => card.themes === selectedTheme);
  const histoireTitle = document.getElementById('histoireTitle');

// Set the value of histoireTitle to the selected theme name
  histoireTitle.textContent = selectedTheme;
  // Generate the card container HTML and insert it into the container element
  container.innerHTML = generateCardContainerHTML(filteredCards);
  



  
  
  
//card send
filteredCards.forEach((card) => {
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

const checkboxes = document.querySelectorAll('input[type="checkbox"]');

checkboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', (event) => {
    const cardId = event.target.id;
    const card = cards.find((card) => card.id === cardId);

    if (card) {
      card.favorite = event.target.checked;
      console.log(card.favorite); // You can check the updated cards array in the console
    }
  });
});

