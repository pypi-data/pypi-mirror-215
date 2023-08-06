let current = 15

let countdownTimer = setInterval(() => {
  current--
  document.querySelector('#countdown').innerHTML = current

  if (current == 0) {
    clearInterval(countdownTimer)
    location.reload()
  }
}, 1000)
