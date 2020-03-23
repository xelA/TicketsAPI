function replace_texts(e) {
  // Find links
  e.innerHTML = e.innerHTML.replace(
    /((http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?)/ig, (_, url) => `<a class="link" href="${url}" target="_blank">${url}</a>`
  )

  // Find Discord emojis
  e.innerHTML = e.innerHTML.replace(
    /&lt;(a?):([^:]+):(\d+)&gt;/g, (_, a, name, id) => `<img class="emoji" src="https://cdn.discordapp.com/emojis/${id}.${a ? 'gif' : 'png'}" alt="${name}"/>`
  )
}

window.onload = function() {
  // Replace all emojis to <img>
  let msg = document.getElementsByClassName("msg")
  let context = document.getElementById("context")

  for (var i = 0; i < msg.length; i++) { replace_texts(msg[i]) }
  replace_texts(context)

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
