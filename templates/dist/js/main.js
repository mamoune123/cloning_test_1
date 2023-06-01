(function($) {

	"use strict";

	$(".toggle-password").click(function() {

  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});

})(jQuery);
document.getElementById("signup-form").addEventListener("submit", function(event) {
  var password = document.getElementById("password-field").value;
  var confirmPassword = document.getElementById("confirm-password-field").value;

  if (password !== confirmPassword) {
      alert("Passwords do not match. Please try again.");
      event.preventDefault(); // Prevent form submission
  }
  
    var emailInput = document.getElementById("Email");
    var email = emailInput.value;
  
    // Regular expression pattern to match the email format
    var emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
  
    // Check if the email matches the pattern
    if (emailPattern.test(email)) {
      console.log("Email is valid");
      // Proceed with submitting the form or other actions
    } else {
      alert("needs a valid email");
      event.preventDefault(); 
      // Display an error message or perform other actions
    }
});



