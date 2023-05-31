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
// function generateCardHTML(vois) {
//     return ` 
//     <div class="cards_item">
//     <div class="cardHistoire">
//     <img class="card-image" src="https://picsum.photos/500/300/?image=10">
//       <div class="card_content">
//         <h2 class="card_title">${vois.nom_file}</h2>
//         <p class="card_texte" style="color : black;">${vois.date_ajout} </p>
//       </div>
//     </div>
//   </div>
//  `;
//   }

//   function generateCardContainerHTML(voix) {
//     return `
      
//         ${voix.map(generateCardHTML).join('')}
      
//     `;
//   }
// const container = document.getElementById('cardContainer');
//   fetch('/voixget')
//   .then(response => response.json())
//   .then(data => {
//     const voix = data.voix;
//     // Generate the card container HTML and insert it into the container element
//     container.innerHTML = generateCardContainerHTML(voix);
//   })
//   .catch(error => {
//     console.error('Error fetching voix:', error);
//   });
function displayFiles(files) {
    var fileList = document.getElementById('file-list');

    // Parcours des fichiers
    files.forEach(function(file) {
      // Création de l'icône du fichier
      var fileIcon = document.createElement('div');
      fileIcon.setAttribute('id', file.id_voix);
      fileIcon.className = 'file-icon';
      fileIcon.innerHTML = '<img src="img/file_icon.png" alt="File Icon">' +
                           '<div class="file-name">' + file.nom_file + '</div>' +
                           '<div class="file-date">' + file.date_ajout + '</div>';

    var deleteIcon = document.createElement('span');
    deleteIcon.className = 'delete-icon';
    deleteIcon.innerHTML = '&times;';

    // Ajout de l'icône de suppression à l'icône du fichier
    fileIcon.appendChild(deleteIcon);

    // Ajout d'un gestionnaire d'événement pour la suppression du fichier
    deleteIcon.addEventListener('click', (function(icon) {
        return function() {
            deleteFile(file.nom_file,fileIcon);
          // Supprimer l'icône du fichier de l'affichage
          
        };
      })(fileIcon));
      // Ajout de l'icône du fichier à la liste
      fileList.appendChild(fileIcon);
   
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'form-check-input';
    checkbox.setAttribute('id', file.id_voix);
    checkbox.value = file.id_voix;
    checkbox.checked = file.selected ? true : false;
    fileIcon.appendChild(checkbox);
    checkbox.addEventListener('change', function() {
        var selected = this.checked; // Get the new value of the checkbox (true/false)
        updateSelected(file.id_voix, selected); 
        // Call the function to update the selected attribute
      });

    });
  }
function updateSelected(voixId, selected) {
    // Set up the data to be sent in the request body
    var data = {
      voixId: voixId,
      selected: selected
    };
  
    // Set up the fetch request
    fetch('/update_selected', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      if (response.ok) {
        // Request was successful, handle the response if needed
        console.log('Selected attribute updated successfully');
      } else {
        // Request failed, handle the error if needed
        console.error('Failed to update selected attribute');
      }
    })
    .catch(function(error) {
      // Error occurred during the request, handle the error if needed
      console.error('Error:', error);
    });
  }
  







  
  function deleteFile(fileName, fileIcon) {
    fetch('/delete-file', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ fileName: fileName })
    })
      .then(function(response) {
        if (response.ok) {
          // Remove the file icon from the display
          fileIcon.parentNode.removeChild(fileIcon);
        } else {
          console.log('Failed to delete the file:', response.statusText);
        }
      })
      .catch(function(error) {
        console.log('Error deleting the file:', error);
      });
  }
  // Appel AJAX pour récupérer la liste des fichiers depuis le serveur
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/voixget', true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      var files = response.voix;
      displayFiles(files);
    }
  };
  xhr.send();







 
  
 