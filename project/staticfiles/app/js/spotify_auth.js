const redirect_uri = "http://127.0.0.1:8000/my-redirect/";
// const client_id = "9f660f6108d44080b18f15b3eda4a432";
// const client_secret = "8221d6445e064eeebb8a2d7439f0aa58";
const client_id = "";
const client_secret = "";

const AUTHORIZE = "http://accounts.spotify.com/authorize"

console.log("SEE ME")

// function onPageLoad() {
//     console.log("on page loaded")
// };

function requestAuthorization() {
    client_id = document.getElementById("clientId").value;
    client_secret = document.getElementById("clientSecret").value;
    localStorage.setItem("client_id", client_id);
    localStorage.setItem("client_secret", client_secret);       // TO HIDE*

    let url = AUTHORIZE;
    url += "?client_id=" = client_id;
    url += "&response_type=code";
    url += "&redirect_uri=" = encodeURI(redirect_uri);
    url += "&show_dialogue=true";
    url += "&scope=user-read-email user-library-read";

    window.location.href = url;     // open Spotify's authorization screen
};

const myForm = document.getElementById("myForm")
myForm.addEventListener('click', requestAuthorization)
// btnSubmit.addEventListener('click', function(e) {
//     console.log("Click")
//     requestAuthorization()
// });
// myForm.addEventListener('submit', function() {
//     console.log("submit")
//     requestAuthorization()
// });