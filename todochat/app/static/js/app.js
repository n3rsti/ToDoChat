window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    if(document.querySelector('.invite__button.friends')){
        document.querySelector('.invite__button.friends').addEventListener("click", openFriendInfo);
    }
    if(document.querySelector('.nav__add-button')){
        document.querySelector('.nav__add-button').addEventListener("click", openChannelCreation);
    }
    if(document.querySelector('.load_more')){
        document.querySelector('.load_more').addEventListener("click", loadGroups);
    }
    if(document.querySelector('.create_task')){
        document.querySelector('.create_task').addEventListener("click", collapseTaskForm);
        document.querySelector('.close_task').addEventListener("click", collapseTaskForm);
        window.scrollTo(0,document.body.scrollHeight);
    }
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    
}
window.addEventListener('resize', () => {
    // We execute the same script as before
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });
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
    openNav();
    channelcreation.classList.toggle("opened")
    if (opened === false) {
        document.querySelector('.nav__add-button').setAttribute('aria-label', 'Close navigation');
        document.querySelector('.nav__add-button').setAttribute('aria-expanded', 'true');
        document.querySelector('.content').classList.add('content--open');
        document.querySelector('.header__button').removeEventListener("click", openNav);
        opened = true;
    }
    else if (opened === true) {
        document.querySelector('.nav__add-button').setAttribute('aria-label', 'Open navigation');
        document.querySelector('.nav__add-button').setAttribute('aria-expanded', 'false');
        document.querySelector('.content').classList.remove('content--open');
        document.querySelector('.header__button').addEventListener("click", openNav);
        opened = true;
    }
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
function collapseFormSection(button, aria_expanded){
    $(`[name=${button.dataset.controls}]`).collapse('toggle');
    btnIcon = button.querySelector('.fas');
    if(aria_expanded=="true"){
        btnIcon.classList.remove('fa-minus');
        btnIcon.classList.add('fa-plus');
        button.setAttribute('aria-expanded', 'false');
    }
    else {
        btnIcon.classList.remove('fa-plus');
        btnIcon.classList.add('fa-minus');
        button.setAttribute('aria-expanded', 'true');
    }

}
function collapseTaskForm(){
    taskForm = document.querySelector('.task_section');
    taskForm.classList.toggle('task_section--open');
}