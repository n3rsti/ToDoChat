window.onload = function () {
    document.querySelector('.header__button').addEventListener("click", openNav);
    if(document.querySelector('.invite__button.friends')){
        document.querySelector('.invite__button.friends').addEventListener("click", openFriendInfo);
    }
    if($('.nav__add-button')){
        $('.nav__add-button').on("click", () => {
            $('.channelcreation').modal('show');
        })
    }
    if($('main.content')){
        $('main.content').on("click", ()=>{
            if($('main.content').hasClass('content--open')){
                openNav();
            }
        })
    }
    if(document.querySelector(".task_filter")){
        blankFormFilter();
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
    let btnIcon = button.querySelector('.fas');
    if(aria_expanded==="true"){
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
    let taskForm = document.querySelector('.task_section');
    taskForm.classList.toggle('task_section--open');
}
function confirmTaskDelete(comment_id){
    let confirmDeleteDiv = $(`.confirm${comment_id}`);
    console.log(confirmDeleteDiv)
    if(confirmDeleteDiv.css('z-index') === "-1"){
        confirmDeleteDiv.css('z-index', 1)
    }
    else {
        confirmDeleteDiv.css('z-index', -1)
    }
}
function removeServerUserModal(user){
    $('.server_remove_user_modal').modal('show');
    $('.removed_user_span').text(user);
    $('input[name ="removed_user"]').val(user);
}