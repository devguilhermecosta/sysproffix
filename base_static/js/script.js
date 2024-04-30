// message animation
const message = document.querySelector('#message');
const MESSAGE_TIME_OUT = 5000  // 5s

if (message) {
  // open the message
  message.classList.add('messages_show');

  // get the progressbar and add the animation
  const progressBar = document.querySelector('#progress-bar');
  progressBar.style.animation = `progress ${MESSAGE_TIME_OUT}ms linear forwards`;

  // close the message
  setTimeout(() => {
    message.classList.remove('messages_show');
    message.classList.add('messages_close');
  }, MESSAGE_TIME_OUT);
}


// disable all buttons submit after click
const buttons = document.querySelectorAll('button[type=submit]');

if (buttons) {
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      form = btn.parentElement;
      btn.disabled = true;
      form.submit();
    })
  })
}
