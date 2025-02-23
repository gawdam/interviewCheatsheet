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

