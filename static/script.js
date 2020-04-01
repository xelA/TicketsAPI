function unix_to_timestamp(e) {
  let unix = parseInt(e.innerText)
  let date = new Date(unix * 1000)
  let months_arr = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ]

  let day = date.getDate()
  let month = months_arr[date.getMonth()]
  let year = date.getFullYear()

  let hours = ("0" + date.getHours()).slice(-2)
  let minutes = ("0" + date.getMinutes()).slice(-2)
  let seconds = ("0" + date.getSeconds()).slice(-2)

  const converted_date = `${day}. ${month} ${year}, ${hours}:${minutes}`

  e.innerText = converted_date

  return converted_date
}

window.onload = function() {
  // Make all timestamps
  let timestamps = document.getElementsByClassName("timestamp")
  for (var i = 0; i < timestamps.length; i++) {
    let converted_date = unix_to_timestamp(timestamps[i])
  }

  unix_to_timestamp(document.getElementById("expire_date"))
  unix_to_timestamp(document.getElementById("created_at"))

  // Enlarge images
  const modal = document.getElementById('modal')

  function openModal(type) {
    modal.querySelector(`#${type}`).style.display = null
    modal.classList.add('opened')
  }

  function closeModal() {
    modal.classList.remove('opened')
    modal.classList.add('closing')
    setTimeout(() => {
      modal.classList.remove('closing')
      modal.querySelectorAll('div').forEach(el => (el.style.display = 'none'))
    }, 200)
  }

  modal.addEventListener('click', closeModal)

  let enlarge = document.getElementById('enlarge')
  enlarge.querySelector('img').addEventListener('click', e => e.stopPropagation())
  document.querySelectorAll('[data-enlargable]').forEach(el => {
    el.addEventListener('click', () => {
      enlarge.querySelector('a').href = el.src
      let target_image = enlarge.querySelector('img')
      target_image.src = el.src
      target_image.style.maxWidth = window.innerWidth - 200
      target_image.style.maxHeight = window.innerHeight - 200
      openModal('enlarge')
    })
  })
}
