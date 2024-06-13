document.addEventListener('DOMContentLoaded', function () {
    const moduleDrawerOptions = document.querySelectorAll('.moduleDrawerOption');
    moduleDrawerOptions.forEach(option => {
        option.addEventListener('click', function () {
            moduleDrawerOptions.forEach(option => {
                option.classList.remove('selected');
            });
            this.classList.add('selected');
            const selectedOption = this.getAttribute('data-value');
            document.getElementById('moduleDrawer').value = selectedOption;
        });
    });
});


function showQR() {
    const data = document.getElementById('data').value;
    const image = document.getElementById('image').files[0];
    const moduleDrawer = document.getElementById('moduleDrawer').value;
    const qrContainer = document.getElementById('qrContainer');
    const qrMessage = document.getElementById('qrMessage');

    const formData = new FormData();
    formData.append('data', data);
    formData.append('module_drawer', moduleDrawer);
    if (image) {
        formData.append('image', image);
    }

    qrMessage.textContent = 'Trying to show QR Code...';

    fetch('https://techwithtobi-23552367d09a.herokuapp.com/generate_qr_directly', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const qrImage = document.createElement('img');
        qrImage.src = url;
        qrImage.alt = 'QR Code';

        qrContainer.innerHTML = '';
        qrContainer.appendChild(qrImage);

        qrMessage.textContent = 'QR Code showed! If you like this one you can download this QR above';
    })
    .catch(error => {
        console.error('Error:', error);
        qrMessage.textContent = 'An error occurred while showing the QR Code.: ' + error;
    });
}

function downloadQR() {
    const data = document.getElementById('data').value;
    const image = document.getElementById('image').files[0];
    const moduleDrawer = document.getElementById('moduleDrawer').value;
    const qrMessage = document.getElementById('qrMessage');

    qrMessage.textContent = 'Generating QR Code...';

    const formData = new FormData();
    formData.append('data', data);
    formData.append('module_drawer', moduleDrawer);

    if (image) {
        formData.append('image', image)
    }

    fetch('https://techwithtobi-23552367d09a.herokuapp.com/generate_qr_directly', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'qrcode.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        qrMessage.textContent = 'QR Code generated and downloaded!';
    })
    .catch(error => {
        console.error('Error:', error);
        qrMessage.textContent = 'An error occurred while generating the QR Code.';
    });
}