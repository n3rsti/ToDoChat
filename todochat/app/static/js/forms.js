function blankFormFilter(){
    let sortFilterForm = document.querySelector('.task_sort_filter_form');

    sortFilterForm.addEventListener('submit', function () {
        let allInputs = sortFilterForm.getElementsByTagName('input');

        for (let i = 0; i < allInputs.length; i++) {
            let input = allInputs[i];
            if (input.name && !input.value) {
                input.name = '';
            }
        }

    });
}
