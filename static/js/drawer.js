// Toggle Drawer Functionality
function toggleDrawer() {
    const drawer = document.getElementById('drawer');
    const toggleButton = document.getElementById('drawer-toggle');
    const icon = toggleButton.querySelector('.icon');

    drawer.classList.toggle('open');
    toggleButton.classList.toggle('open');

    // Change icon to "X" when drawer is open
    if (drawer.classList.contains('open')) {
        icon.textContent = '×'; // Unicode for "X"
    } else {
        icon.textContent = '☰'; // Unicode for "three lines"
    }
}

// Close Drawer on Click Outside
document.addEventListener('click', function (event) {
    const drawer = document.getElementById('drawer');
    const toggleButton = document.getElementById('drawer-toggle');

    if (!drawer.contains(event.target) && !toggleButton.contains(event.target)) {
        drawer.classList.remove('open');
        toggleButton.classList.remove('open');
        toggleButton.querySelector('.icon').textContent = '☰'; // Reset icon
    }
});