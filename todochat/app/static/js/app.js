window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    if(document.querySelector('.invite__button.friends')){
        document.querySelector('.invite__button.friends').addEventListener("click", openFriendInfo);
    }
    if(document.querySelector('.create_server__button')){
        document.querySelector('.create_server__button').addEventListener("click", openChannelCreation);
    }
    
}
function openFriendInfo(){
    document.querySelector('.invite__button.remove').classList.toggle('button--opened')
}
let opened = false
const channelcreation = document.querySelector('.channelcreation')
function openNav() {
    document.querySelector('.content').classList.toggle('content--open');
    document.querySelector('.header').classList.toggle('header--dark');
    document.querySelector('.side__nav').classList.toggle('side__nav--open');
    document.querySelector('.header__button').classList.toggle('header__button--open');
    if (opened === false) {
        document.querySelector('.header__button').setAttribute('aria-label', 'Close navigation');
        document.querySelector('.header__button').setAttribute('aria-expanded', 'true');
        opened = true;
    }
    else if (opened === true) {
        document.querySelector('.header__button').setAttribute('aria-label', 'Open navigation');
        document.querySelector('.header__button').setAttribute('aria-expanded', 'false');
        opened = false;
    }
}
function openChannelCreation(){
    channelcreation.classList.toggle("opened")
    if (opened === false) {
        document.querySelector('.create_server__button').setAttribute('aria-label', 'Close navigation');
        document.querySelector('.create_server__button').setAttribute('aria-expanded', 'true');
        opened = true
    }
    else if (opened === true) {
        document.querySelector('.create_server__button').setAttribute('aria-label', 'Open navigation');
        document.querySelector('.create_server__button').setAttribute('aria-expanded', 'false');
        opened = true
    }
    openNav();
}