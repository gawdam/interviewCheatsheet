// Show the loading screen when the form is submitted
document.getElementById('upload-form').addEventListener('submit', function(event) {
    // Show the loading screen
    document.getElementById('loading-screen').style.display = 'flex';
});

// Other existing functions for file handling
function handleBoxClick() {
  document.getElementById('file-input').click();
}

function handleFile(file) {
  if (file && file.type === 'application/pdf') {
    const fileURL = URL.createObjectURL(file);
    const uploadBox = document.querySelector('.upload-box');
    const pdfText = document.querySelector('.pdf-instruction');
    const iframe = document.querySelector('#pdf-preview');

    // Display the PDF in the iframe
    iframe.src = fileURL;
    iframe.classList.remove('preview-hidden');

    // Hide the default upload message
    uploadBox.querySelector('img').style.display = 'none';
    uploadBox.querySelector('p').style.display = 'none';
    pdfText.querySelector('p').style.display = 'none';
  } else {
    alert('Please upload a valid PDF file.');
  }
}

function handleFileInput(event) {
  const file = event.target.files[0];
  handleFile(file);
}

function handleDragOver(event) {
  event.preventDefault();
  const uploadBox = document.querySelector('.upload-box');
  uploadBox.classList.add('dragover');
}

function handleDragLeave() {
  const uploadBox = document.querySelector('.upload-box');
  uploadBox.classList.remove('dragover');
}

function handleDrop(event) {
  event.preventDefault();
  const uploadBox = document.querySelector('.upload-box');
  uploadBox.classList.remove('dragover');

  const file = event.dataTransfer.files[0];
  handleFile(file);
}
