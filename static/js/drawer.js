document.addEventListener('DOMContentLoaded', function() {
    const drawer = document.getElementById('drawer');
    const drawerToggle = document.getElementById('drawer-toggle');
    const container = document.querySelector('.container');
    let isDrawerOpen = false;

    function toggleDrawer() {
        isDrawerOpen = !isDrawerOpen;
        drawer.classList.toggle('open');
        container.classList.toggle('drawer-open');
        
        // Update toggle button icon
        const icon = drawerToggle.querySelector('i');
        icon.classList.remove(isDrawerOpen ? 'fa-bars' : 'fa-times');
        icon.classList.add(isDrawerOpen ? 'fa-times' : 'fa-bars');
    }

    drawerToggle.addEventListener('click', toggleDrawer);

    // Close drawer when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInside = drawer.contains(event.target) || drawerToggle.contains(event.target);
        
        if (!isClickInside && isDrawerOpen) {
            toggleDrawer();
        }
    });

    // Prevent drawer close when clicking inside
    drawer.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});