(function() {
    window.addEventListener('load', (e) => {

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
    