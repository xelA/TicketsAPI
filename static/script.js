window.onload = function() {
  // Replace all emojis to <img>
  let msg = document.getElementsByClassName("msg")
  for (var i = 0; i < msg.length; i++) {
    msg[i].innerHTML = msg[i].innerHTML.replace(
      /&lt;(a?):([^:]+):(\d+)&gt;/g, (_, a, name, id) => `<img class="emoji" src="https://cdn.discordapp.com/emojis/${id}.${a ? 'gif' : 'png'}" alt="${name}"/>`
    )

    msg[i].innerHTML = msg[i].innerHTML.replace(
      /((http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?)/ig, (_, url) => `<a class="link" href="${url}" target="_blank">${url}</a>`
    )
  }

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
      enlarge.querySelector('img').src = el.src
      enlarge.querySelector('a').href = el.src
      openModal('enlarge')
    })
  })
}
