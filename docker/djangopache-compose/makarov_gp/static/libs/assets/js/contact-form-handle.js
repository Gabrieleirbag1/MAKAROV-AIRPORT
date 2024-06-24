const nameInput = document.getElementById("name");
const mailInput = document.getElementById("email");
const subjectInput = document.getElementById("subject");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("contact-form-submit-button");

const modalButton =  document.getElementById("modalButton");
const modalBody = document.getElementById("modalBody");
const modalTitle = document.getElementById("contactFormModalLabel");

function validateEmail(email) {//email -> str
    //regex = is email a valid email format
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return regex.test(email);
}

sendButton.addEventListener("click", function(event) {
    event.preventDefault();

    // check if all fields are filled & email is valid
    if (nameInput.value.trim() !== "" && 
        validateEmail(mailInput.value) &&
        subjectInput.value.trim() !== "" && 
        messageInput.value.trim() !== "") 
    {
        modalButton.textContent = "Close";
        modalTitle.textContent = "Your message has been sent!";
        modalBody.textContent = "Thank you for contacting us, " + nameInput.value + "! We will get back to you as soon as possible.";

        nameInput.value = "";
        mailInput.value = "";
        subjectInput.value = "";
        messageInput.value = "";

        document.getElementById("hiddenModalButton").click(); // Only trigger click if all validations pass
    } else {
        //console.log("Validation failed. Not all fields are filled or email is invalid.");
        modalButton.textContent = "Close";
        modalTitle.textContent = "Validation failed!";
        modalBody.textContent = "Please make sure all fields are filled and email is valid.";

        document.getElementById("hiddenModalButton").click();
    }
});

