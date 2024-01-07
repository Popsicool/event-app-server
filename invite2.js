// $(document)
//     .ready(function() {
//         $('.frame')
//             .click(function() {
//                 $('.top')
//                     .addClass('open');
//                 $('.message')
//                     .addClass('pull');
//             })
//     });

body = document.querySelector('.frame')
body.addEventListener('click', () => {
    document.querySelector('.top').classList.add("open")
    document.querySelector('.message').classList.add("pull")
    document.querySelector('.message').classList.add("message2")
})
// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var close_btn = document.getElementById("button_close_envelope");

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

close_btn.addEventListener('click', () => {
    document.querySelector('.top').classList.remove("open")
    document.querySelector('.message').classList.remove("pull")
})
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}