// Get all input elements on the page
var inputElements = document.querySelectorAll('input');

// Check each input element to see if it's a hidden field
for (var i = 0; i < inputElements.length; i++) {
    if (inputElements[i].type === 'hidden') {
        console.log('Hidden input field found.');
        // You can access more information about the hidden input field if needed, for example:
        console.log('Name: ' + inputElements[i].name);
        console.log('Value: ' + inputElements[i].value);
        // Break out of the loop if you only want to find the first hidden input field
        // break;
    }
}

// If you want to check for a specific hidden input field by name, you can do the following:
// var specificHiddenField = document.querySelector('input[name="yourFieldName"]');
// if (specificHiddenField) {
//     console.log('Specific hidden input field found.');
// }
