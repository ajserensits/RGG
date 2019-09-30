$(document).ready(init);

var PROTOCOL = window.location.protocol;
var HOST = window.location.hostname;
var BASE_PATH = PROTOCOL + "//" + HOST;

function init()
{
    attachEventHandlers();
}

function attachEventHandlers()
{
    $('#login_button').click(logIn);
}

function logIn()
{
    var username = $('#username').val();
    var password = $('#password').val();

    $.get(BASE_PATH + "/login/?user=" + username + "&password=" + password , function(data){
         console.log(data);
         if(data["Verified"] == "True") {
             var user = data["User"];
             var token = data["Token"];
             window.location.href = "admin.html?user=" + user + "&token=" + token;
         } else {
             alert("Could Not Authenticate\nReason: " + data["Reason"]);
         }
    });
}