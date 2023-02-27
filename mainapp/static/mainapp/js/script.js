const catalogContainer = document.querySelector('.catalog');

function getActiveElement() {
    return catalogContainer.querySelector('.catalog__category_active');
}

function getContainer(element) {
    return catalogContainer.querySelector(`.${element.id}-container`)
}

function openContainer(container) {
    container.classList.add('catalog__lists-container_opened');
}

function closeContainer(evt) {
    const container = catalogContainer.querySelector('.catalog__lists-container_opened');
    if (container) {
        container.classList.remove('catalog__lists-container_opened');
    }
}

function addActiveClass(element) {
    element.classList.add('catalog__category_active');
}

function removeActiveClass() {
    const element = getActiveElement();
    if (element) {
        element.classList.remove('catalog__category_active');
    }
}

function setStartState(evt) {
    const element = getActiveElement();
    const container = getContainer(element);
    openContainer(container);
}

function scroll(container) {
    container.scrollIntoView({behavior: "smooth", block: "start", inline: "start"});
}

function showCategoryDetails(evt) {
    const categoryElement = evt.target.closest('.catalog__category');
    const closeBtnElement = evt.target.closest('.btn_style_close');

    if (categoryElement) {
        const container = getContainer(categoryElement);

        closeContainer();
        removeActiveClass();
        addActiveClass(categoryElement)
        openContainer(container);
        scroll(container);
    } else if (closeBtnElement) {
        removeActiveClass();
        closeContainer();
    }
}


catalogContainer.addEventListener('click', showCategoryDetails );
window.addEventListener('load', setStartState);