(function() {
    window.addEventListener('load', (e) => {
        let data = retrieveExercises();
        console.log(data);
        const deleteForm = document.querySelector('#delete-account');
        deleteForm.addEventListener('submit', (e) => {
            e.preventDefault();
            confirmAction(function(e) {
                console.log("You did do it.");
                document.querySelector('.confirm').remove();
                deleteForm.submit();
                return true;
            }, function(e) {
                console.log("You didn't do it.");
                document.querySelector('.confirm').remove();
                return false;
            });
        });

    });

    function retrieveExercises() {
        return fetch('/api/exercise/log', {
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

    function deleteExercise(e) {
        let id = e.target.dataset.id;
        console.log(id);
        // return fetch(`/api/${exerciseId}/delete`, {
        //     method: 'POST',
        //     mode: 'same-origin',
        //     cache: 'no-cache',
        //     credentials: 'same-origin',
        // }).then(res => {
        //     return res.json();
        // }).catch(err => {
        //     console.log(err);
        // });
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
    