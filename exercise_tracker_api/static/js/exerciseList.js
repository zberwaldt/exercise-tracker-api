(function() {
    window.addEventListener('load', (e) => {
        let id = document.querySelector('.exercise-list').dataset.id;
        let exerciseData = retrieveExercises(id);
        renderTableRows(exerciseData);
        let exerciseRows = document.querySelectorAll('.exercise');

        if(exerciseRows.length < 1) {
          
        } 

        let deleteButtons = document.querySelectorAll('.delete');
        deleteButtons.forEach(x => {
            x.addEventListener('click', deleteExercise);
        });

    });

    function retrieveExercises(id) {
        return fetch(`/api/exercise/log?user_id=${id}`, {
            method: 'GET',
            mode: 'same-origin',
            cache: "no-cache",
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => {
            return res.json();
        }).catch(err => {
            console.log(err);
        });
    }


    function deleteExercise() {
        let exerciseId = this.dataset.id;
        deleteTableRow(exerciseId);
        return fetch(`/api/exercise/${exerciseId}/delete`, {
            method: 'POST',
            mode: 'same-origin',
            cache: 'no-cache',
            credentials: 'same-origin',
        }).catch(err => console.log(err));
    }

    function renderTableRows(data) {

    }

    function deleteTableRow(id) {
        let row = document.querySelector(`#exercise-${id}`);
        row.remove();
    }

    function confirmAction(yesCallback, noCallback) {

        // Create the confirm dialog elements
        let fragment = document.createDocumentFragment();
        let confirmBtn = document.createElement('button');
        let cancelBtn = document.createElement('button');
        let div = document.createElement('div');
        let h4 = document.createElement('h4');
        
        h4.textContent="Are you sure?";
        div.appendChild(h4);
        
        confirmBtn.textContent = "Yes";
        confirmBtn.addEventListener('click', yesCallback);
        div.appendChild(confirmBtn);

        cancelBtn.textContent = "No";
        cancelBtn.addEventListener('click', noCallback);
        div.appendChild(cancelBtn);


        div.classList.add('confirm');
        
        fragment.appendChild(div);
        
        document.querySelector('main').appendChild(fragment);
        
    }
})();
    