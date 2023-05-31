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

    navigator
        .mediaDevices
        .getUserMedia({audio: true})
        .then(stream => { handlerFunction(stream) });

    function handlerFunction(stream) {
        rec = new MediaRecorder(stream);
        rec.ondataavailable = e => {
            audioChunks.push(e.data);
        }
    }
    let isRecording = false;
    document.getElementById('validate').addEventListener('click', function() {
      
        if(!isRecording){
            alert("Please Record your Voice first");
            return;
        }
      
      console.log("Sending data to Flask...");
      var filename = document.getElementById('file-name1').value;
      let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
      var blob2 = blob.slice();
      blob2.name = filename + '.mp3';
      blob.name = filename + '.mp3';
      console.log(filename);
      console.log(blob.name);
      sendData(blob,blob2);
      window.location.href= "/T";
    });
    
    function sendData(data,data1) {
         var filename = data.name;
         var filename1 = data1.name;
        var form = new FormData();
        form.append('file', data, filename);
        var form2 = new FormData();
        form2.append('file', data1, filename1);
        //Chrome inspector shows that the post data includes a file and a title.
        $.ajax({
            type: 'POST',
            url: '/save-record',
            data: form,
            cache: false,
            processData: false,
            contentType: false
        }).done(function(data) {
            console.log(data);
        });
        $.ajax({
          type: 'POST',
          url: '/save_mesvoix',
          data: form2,
          cache: false,
          processData: false,
          contentType: false
      }).done(function(data1) {
          console.log(data1);
      });
    }
    

var audioPlayer = document.createElement('audio');
document.body.appendChild(audioPlayer);

// Function to handle playing the recorded audio
function playRecording() {
    if(!isRecording ){
        alert("Please record your voice first");
        return;
    }
  var audioBlob = new Blob(audioChunks, { type: 'audio/mpeg-3' });
  var audioURL = URL.createObjectURL(audioBlob);
  audioPlayer.src = audioURL;
  audioPlayer.play();
}

// Event handler for the "PlayRecording" button
PlayRecording.onclick = function(e) {
  console.log("Playing the recorded audio");
  playRecording();
};

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
  }
  var micButton = document.getElementById("micButton");
  var isPulsing = false;
  
  micButton.addEventListener("click", function() {
    if (!isPulsing) {
      micButton.classList.add("pulse-animation");
      isPulsing = true;    
        console.log('Recording are started..');
        isRecording = true;
        startRecording.disabled = true;
        stopRecording.disabled = false;
        audioChunks = [];
        rec.start();
    } else {
      micButton.classList.remove("pulse-animation");
      isPulsing = false;
     
        console.log("Recording are stopped.");
        startRecording.disabled = false;
        stopRecording.disabled = true;
        rec.stop();
    
    }
  });


  
  var lang = localStorage.getItem("selectedLanguage");
  var contentElement = document.getElementById('content');
  console.log(lang);

// Update the content based on the language value
if (lang === 'english') {
  contentElement.innerHTML = `
    <p>
      When you're ready, press play and read these sentences out loud.
      <br>
      "Phrase 1"
      <br>
      "Phrase 2"
      <br>
      ...
    </p>
  `;
} else if (lang === 'Francais') {
  contentElement.innerHTML = `
    <p>
      Quand vous êtes prêts, appuyez sur play et lisez ces phrases à voix haute.
      <br>
      "Phrase 1"
      <br>
      "Phrase 2"
      <br>
      ...
    </p>
  `;
} else {
  contentElement.innerHTML = `
    <p>
      When you're ready, press play and read these sentences out loud.
      <br>
      "Phrase 1"
      <br>
      "Phrase 2"
      <br>
      ...
    </p>
  `;
}

  