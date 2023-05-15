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

//-----------------------------file selection : 

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const fileListe = document.getElementById("file-list");

let files = [];

customBtn.addEventListener("click", function() {
realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
files = [...realFileBtn.files];
if (files.length > 0) {
    let html = "";
    files.forEach(file => {
    html += `<li>${file.name}</li>`;
    });
    fileListe.innerHTML = html;
    customTxt.innerHTML = files.length + " file(s) selected";
} else {
    fileListe.innerHTML = "";
    customTxt.innerHTML = "No file chosen, yet.";
}
});


  
  
  
//-------------------record stop 
// Get references to the buttons and the audio element
// Get the necessary elements
const recordBtn = document.getElementById("record-button");
const playBtn = document.getElementById("play-button");
const sendBtn = document.getElementById("send-button");

let recordedAudio = null;

// Handle the record button click event
recordBtn.addEventListener("click", function() {
  if (recordBtn.innerHTML === 'RECORD') {
    // Start recording
    recordBtn.innerHTML = 'STOP RECORDING';

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function(stream) {
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        mediaRecorder.start();

        mediaRecorder.addEventListener("dataavailable", function(event) {
          chunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", function() {
          // Convert the recorded audio chunks to a single Blob
          const recordedAudioBlob = new Blob(chunks, { type: "audio/wav" });
          
          // Create a new File object from the Blob
          const recordedAudioFile = new File([recordedAudioBlob], "recorded_audio.wav");
          
          // Store the recorded audio file in the recordedAudio variable
          recordedAudio = recordedAudioFile;
        });

        recordBtn.addEventListener("click", function() {
          // Stop recording
          mediaRecorder.stop();
          recordBtn.innerHTML = 'RECORD';
        });
      })
      .catch(function(err) {
        console.log("An error occurred: " + err);
      });
  } else {
    // Stop recording
    mediaRecorder.stop();
    recordBtn.innerHTML = 'RECORD';
  }
});


// Handle the play button click event
playBtn.addEventListener("click", function() {
  if (recordedAudio) {
    const audioPlayer = new Audio(URL.createObjectURL(recordedAudio));
    audioPlayer.play();
  }
});

// Handle the send button click event
sendBtn.addEventListener("click", function() {
  if (recordedAudio) {
    // Create a Blob URL for the recorded audio data
    const url = URL.createObjectURL(recordedAudio);

    // Create a new anchor element
    const a = document.createElement('a');
    
    // Set the href attribute to the Blob URL
    a.href = url;
    
    // Set the download attribute to the filename
    a.download = 'recorded_audio.wav';
    
    // Simulate a click on the anchor element to initiate the download
    a.click();
  }
});





// Handle the form submission event








  
//--------------------------------validate the upload imput is not empty 
function validateForm() {
  var textInput = document.getElementsByName('text')[0];
  var realFileInput = document.getElementById('real-file');

  if (textInput.value == "" && realFileInput.files.length == 0) {
      document.getElementById("error-message").innerHTML = "Please enter a story or select at least one file.";
      return false;
  } else {
      return true;
  }
}



//-----------------------------audio play pause.
function toggleAudio() {
    var audio = document.getElementById("output-audio");
    var playButton = document.getElementById("button_play");
    
    if (audio.paused) {
      audio.play();
      playButton.textContent = "Pause the synthesized voice";
    } else {
      audio.pause();
      playButton.textContent = "Play the synthesized voice";
    }
  }

//---------------try

const myForm = document.getElementById("myForm");
const generateStoryBtn = document.getElementById("generate-story-button");

generateStoryBtn.addEventListener("click", function() {
  myForm.submit();
});
  

  
  
  
