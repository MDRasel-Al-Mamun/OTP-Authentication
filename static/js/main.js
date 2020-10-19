function ReSendOTP(username, mess_id) {
  mess = document.getElementById(mess_id);
  mess.innerText = 'Sending...';
  $.ajax({
    type: 'GET',
    url: '/authentication/resendOTP',
    data: { user: username },
    success: function (data) {
      mess.innerText = data;
    },
  });
}


$(document).ready(function () {
  $('#validation-form').validate({
    rules: {
      first_name: 'required',
      last_name: 'required',
      username: 'required',
      email: 'required',
      password: {
        required: true,
        minlength: 8,
      },
      confirm_password: {
        required: true,
        equalTo: '#passwordField',
      },
      agree: 'required',
    },
    messages: {
      first_name: 'Please enter your first name',
      last_name: 'Please enter your last name',
      username: 'Please enter a username',
      email: 'Please enter a valid email address',
      password: {
        required: 'Please provide a password',
        minlength: 'Your password must be at least 8 characters long',
      },
      confirm_password: {
        required: 'Confirm your password',
        equalTo: 'Password not match',
      },
      agree: ' ',
    },
    errorElement: 'p',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');

      if (element.prop('type') === 'checkbox') {
        error.insertAfter(element.next('label'));
      } else {
        error.insertAfter(element);
      }
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass('is-invalid').removeClass('is-valid');
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).addClass('is-valid').removeClass('is-invalid');
    },
  });
  if ($.fn.passwordStrength) {
    $('#passwordField').passwordStrength({
      minimumChars: 8,
    });
  }
});



const usernameField = document.querySelector('#userName');
const feedBackArea = document.querySelector('.usernameFeedBackArea');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');



usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;
  usernameField.classList.remove('is-invalid');
  feedBackArea.style.display = 'none';
  if (usernameVal.length > 0) {
    fetch('/authentication/validate_username', {
      body: JSON.stringify({ username: usernameVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add('is-invalid');
          feedBackArea.style.display = 'block';
          feedBackArea.innerHTML = `<p style="color:#dc3545";>${data.username_error}</p>`;
        }
      });
  }
});


emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;
  emailField.classList.remove('is-invalid');
  emailFeedBackArea.style.display = 'none';
  if (emailVal.length > 0) {
    fetch('/authentication/validate_email', {
      body: JSON.stringify({ email: emailVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add('is-invalid');
          emailFeedBackArea.style.display = 'block';
          emailFeedBackArea.innerHTML = `<p style="color:#dc3545";>${data.email_error}</p>`;
        }
      });
  }
});