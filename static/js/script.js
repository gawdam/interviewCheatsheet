// Drawer functionality
const drawer = document.getElementById('drawer');
const drawerTrigger = document.getElementById('drawerTrigger');
const drawerBackdrop = document.getElementById('drawerBackdrop');
const closeDrawer = document.getElementById('closeDrawer');

function openDrawer() {
    drawer.classList.add('open');
    drawerBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeDrawerHandler() {
    drawer.classList.remove('open');
    drawerBackdrop.classList.remove('open');
    document.body.style.overflow = '';
}

if (drawerTrigger) {
    drawerTrigger.addEventListener('click', openDrawer);
    closeDrawer.addEventListener('click', closeDrawerHandler);
    drawerBackdrop.addEventListener('click', closeDrawerHandler);
}

// File handling functions
function handleBoxClick() {
    document.getElementById('file-input').click();
}

function handleFile(file) {
    if (file && file.type === 'application/pdf') {
        const fileURL = URL.createObjectURL(file);
        const uploadBox = document.querySelector('.upload-box');
        const pdfPreview = document.getElementById('pdf-preview');
        
        // Hide all upload box content
        const elementsToHide = uploadBox.querySelectorAll('img, p, .pdf-instruction');
        elementsToHide.forEach(el => el.style.display = 'none');
        
        // Show and update the PDF preview
        pdfPreview.src = fileURL;
        pdfPreview.classList.remove('preview-hidden');
        pdfPreview.classList.add('preview-visible');
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
    event.currentTarget.classList.add('dragover');
}

function handleDragLeave(event) {
    event.currentTarget.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    
    const file = event.dataTransfer.files[0];
    handleFile(file);
}

// Form submission handling
const uploadForm = document.getElementById('upload-form');
if (uploadForm) {
    uploadForm.addEventListener('submit', function(event) {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.style.display = 'flex';
    });
}