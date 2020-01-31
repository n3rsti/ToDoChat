window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    document.querySelector('.create_server__button').addEventListener("click", createServerMenu)
    document.querySelector('.create__exit').addEventListener("click", closeCreateMenu)
}
let opened = false
function openNav() {
    document.querySelector('.content').classList.toggle('content--open');
    document.querySelector('.header').classList.toggle('header--dark');
    document.querySelector('.side__nav').classList.toggle('side__nav--open');
    if (opened === false) {
        document.querySelector('.header__button').setAttribute('aria-label', 'Close navigation');
        document.querySelector('.header__button').setAttribute('aria-expanded', 'true');
        opened = true
    }
    else if (opened === true) {
        document.querySelector('.header__button').setAttribute('aria-label', 'Open navigation');
        document.querySelector('.header__button').setAttribute('aria-expanded', 'false');
        opened = true
    }
}
function createServerMenu(){
    openNav();
    document.querySelector('.create_server_menu').classList.toggle('create_server_menu--open');
    document.querySelector('.content').classList.toggle('section__news--blur');
}
function closeCreateMenu(){
    document.querySelector('.create_server_menu').classList.toggle('create_server_menu--open');
    document.querySelector('.content').classList.toggle('section__news--blur');
}