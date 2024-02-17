document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('navbar');
    const landingPage = document.getElementById('landing-page');
    const landingPageHeight = landingPage.offsetHeight; // Height of landing page section

    function toggleStickyNavbar() {
        if (window.scrollY >= landingPageHeight) {
            navbar.classList.add('sticky');
        } else {
            navbar.classList.remove('sticky');
        }
    }

    window.addEventListener('scroll', toggleStickyNavbar);

});