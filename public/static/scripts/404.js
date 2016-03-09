var inputReady = true;
var input = $('.404-input');
input.focus();
$('.container').on('click', function(e) {
  input.focus();
});

input.on('keyup', function(e) {
  $('.new-output').text(input.val());
});

$('.four-oh-four-form').on('submit', function(e) {
  e.preventDefault();
  var val = $(this).children($('.404-input')).val().toLowerCase();
  var href;

  if (val === 'all iz well') {
    showKittens();
  } else {
    resetForm();
  }
});

function resetForm() {
  var message = "Sorry that command is not recognized."
  var input = $('.404-input');

  $('.new-output').removeClass('new-output');
  input.val('');
  $('.terminal').append('<p class="prompt">' + message + '</p><p class="prompt output new-output"></p>');

  $('.new-output').velocity(
    'scroll'
  ), {
    duration: 100
  }
}

function showKittens() {
    window.location.href = "http://dev.limberapp.xyz";
}
