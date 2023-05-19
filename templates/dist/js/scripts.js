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
     var selectedOption1 = document.getElementById('Gender').options[document.getElementById('Gender').selectedIndex].text;
     var selectedOption2 = document.getElementById('Accent').options[document.getElementById('Accent').selectedIndex].text;
      send2Data(selectedOption1,selectedOption2)
      console.log("Sending data to Flask...");
      let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
      sendData(blob);
      window.location.href = 'page2.html';
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

    function sendData(data) {
        var form = new FormData();
        form.append('file', data, 'data.mp3');
        form.append('title', 'data.mp3');
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
    }

    startRecording.onclick = e => {
        console.log('Recording are started..');
        isRecording = true;
        startRecording.disabled = true;
        stopRecording.disabled = false;
        audioChunks = [];
        rec.start();
    };

    stopRecording.onclick = e => {
        console.log("Recording are stopped.");
        startRecording.disabled = false;
        stopRecording.disabled = true;
        rec.stop();
    };
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


  
  
  
