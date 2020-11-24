window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    if(document.querySelector('.invite__button.friends')){
        document.querySelector('.invite__button.friends').addEventListener("click", openFriendInfo);
    }
    if(document.querySelector('.create_server__button')){
        document.querySelector('.create_server__button').addEventListener("click", openChannelCreation);
    }
    if(document.querySelector('.load_more')){
        document.querySelector('.load_more').addEventListener("click", loadGroups);
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
        opened = true;
    }
    else if (opened === true) {
        document.querySelector('.create_server__button').setAttribute('aria-label', 'Open navigation');
        document.querySelector('.create_server__button').setAttribute('aria-expanded', 'false');
        opened = true;
    }
    openNav();
}
function loadGroups(){
    let button = document.querySelector('.load_more');
    let groups = document.querySelectorAll(".groups__li.base");
    button.setAttribute('aria-label', 'Hide additional groups');
    button.setAttribute('aria-expanded', 'true')
    button.innerText = "Hide";
    button.classList.toggle("opened");
    button.removeEventListener("click", loadGroups);
    button.addEventListener("click", hideGroups);
    for(let i = 5; i < groups.length; i++){
        groups[i].classList.toggle("opened")
    }
}
function hideGroups(){
    let button = document.querySelector('.load_more');
    let groups = document.querySelectorAll(".groups__li.base");
    button.setAttribute('aria-label', 'Show additional groups');
    button.setAttribute('aria-expanded', 'false');
    button.innerText = "Show more";
    button.classList.toggle("opened");
    button.removeEventListener("click", hideGroups);
    button.addEventListener("click", loadGroups);
    for(let i = 5; i < groups.length; i++){
        groups[i].classList.toggle("opened")
    }
}