// JavaScript to toggle collapsible sections
document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll(".collapsible-section");

    sections.forEach((section) => {
        const header = section.querySelector(".collapsible-header");
        const content = section.querySelector(".collapsible-content");
        const button = section.querySelector(".toggle-button");

        header.addEventListener("click", () => {
            const isCollapsed = content.style.display === "none" || !content.style.display;

            // Toggle content visibility
            content.style.display = isCollapsed ? "block" : "none";

            // Rotate the button
            button.classList.toggle("collapsed", !isCollapsed);
        });
    });
});

// Drawer functionality
let isDrawerOpen = false;

function toggleDrawer() {
    const drawer = document.getElementById('drawer');
    const drawerToggle = document.getElementById('drawer-toggle');
    
    isDrawerOpen = !isDrawerOpen;
    
    if (isDrawerOpen) {
        drawer.classList.add('open');
        drawerToggle.style.right = '420px'; // Move toggle button with drawer
    } else {
        drawer.classList.remove('open');
        drawerToggle.style.right = '20px';
    }
}

// Close drawer when clicking outside
document.addEventListener('click', (event) => {
    const drawer = document.getElementById('drawer');
    const drawerToggle = document.getElementById('drawer-toggle');
    
    if (isDrawerOpen && 
        !drawer.contains(event.target) && 
        !drawerToggle.contains(event.target)) {
        toggleDrawer();
    }
});

// Handle escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isDrawerOpen) {
        toggleDrawer();
    }
});

// Prevent drawer from closing when clicking inside
document.getElementById('drawer').addEventListener('click', (event) => {
    event.stopPropagation();
});

// Handle window resize
window.addEventListener('resize', () => {
    const drawerToggle = document.getElementById('drawer-toggle');
    if (isDrawerOpen) {
        drawerToggle.style.right = window.innerWidth <= 768 ? '10px' : '420px';
    }
});