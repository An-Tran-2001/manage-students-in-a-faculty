const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");
const message = document.getElementById("message");
const submit = document.querySelector('#submit');

var check = function () {
    if (password.value ==
        confirm_password.value) {
        message.style.color = 'green';
        message.innerHTML = 'matching';
        submit.disabled = false;
    } else {
        message.style.color = 'red';
        message.innerHTML = 'not matching';
        submit.disabled = true;
    }
}

console.log(check);