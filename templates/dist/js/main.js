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
});



