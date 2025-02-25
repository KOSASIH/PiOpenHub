// Client-side validation scripts
function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    return emailRegex.test(email);
}

function validateForm() {
    const emailInput = document.getElementById('email').value;
    if (!validateEmail(emailInput)) {
        alert('Please enter a valid email address.');
        return false;
    }
    return true;
}
