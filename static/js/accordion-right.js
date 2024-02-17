
function isInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}


function handleAnimation() {
    var accordionItems = document.querySelectorAll('.accordion-item');
    accordionItems.forEach(function (item) {
        if (isInViewport(item)) {
            item.classList.add('visible');
        }
    });
}


window.addEventListener('scroll', handleAnimation);


handleAnimation();