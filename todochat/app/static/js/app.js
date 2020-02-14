window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    if(document.querySelector('.invite__button.friends')){
        document.querySelector('.invite__button.friends').addEventListener("click", openFriendInfo);
    }
}
function openFriendInfo(){
    document.querySelector('.invite__button.remove').classList.toggle('button--opened')
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