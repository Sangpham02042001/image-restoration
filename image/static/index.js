if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

let myImage = document.getElementById('id_image')
let previewTitle = document.getElementById('preview-title')
let uploadBtn = document.getElementById('submit_form')
uploadBtn.disabled = true
previewTitle.style.display = 'none'

myImage.onchange = () => {
  if (myImage.files && myImage.files[0]) {
    let src = URL.createObjectURL(myImage.files[0])
    document.getElementById('image-preview').src = src
    uploadBtn.disabled = false
    previewTitle.style.display = 'block'
  }
}

function handleSubmit(e) {
  e.preventDefault()
  console.log(myImage)
  if (myImage.files.length === 0) {
    return
  }
  let file = myImage.files[0]
  if (!file.type || !(new RegExp(/image\/*/).test(file.type))) {
    return
  }
  document.getElementById('image-preview').src = ""
  uploadBtn.disabled = true
  previewTitle.style.display = 'none'
  document.getElementById('form').submit()
}