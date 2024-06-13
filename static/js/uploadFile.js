document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
});

function uploadFile(file) {
    const url = '/generate_qr';
    const formData = new FormData();
    formData.append('image', file);

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            displayMessage(data.error, 'error');
        } else {
            displayMessage(data.message, 'success');
            previewFile(file);
        }
    })
    .catch(error => {
        displayMessage('An error occurred while uploading the file.', 'error');
    });
}

function previewFile(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        const img = document.createElement('img');
        img.src = reader.result;
        document.getElementById('gallery').appendChild(img);
    }
}

function displayMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = type;
}