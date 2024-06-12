function downloadVideo() {

    const videoUrl = document.getElementById('videoUrl').value;
    const downloadMessage = document.getElementById('downloadMessage');

    downloadMessage.textContent = 'Downloading video...';

    fetch('https://techwithtobi-23552367d09a.herokuapp.com/download_video_directly', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'YouTubeVideo.mp4';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        downloadMessage.textContent = 'Video downloaded successfully!';
    })
    .catch(error => {
        console.error('Error:', error);
        downloadMessage.textContent = 'An error occurred while downloading the video.';
    });
}