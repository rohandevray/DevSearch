// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

// document.querySelector(".alert__close").style.zIndex = "100";
// document.querySelector(".alert").style.zIndex= "10";
// document.querySelector(".alert").style.position ="absolute";
// document.querySelector(".alert").style.left ="38%"
// document.querySelector(".alert").style.top ="20%"
// // document.querySelector(".alert").style.background= "transparent";


if (alertWrapper) {
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none',
   
  )
}