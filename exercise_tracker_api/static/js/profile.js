(function() {
    window.addEventListener('load', (e) => {

        const deleteBtn = document.querySelector('#delete');
        deleteBtn.addEventListener('click', confirmAction(function(e) {
            console.log("You did do it.");
            return;
        }, function(e) {
            console.log("You didn't do it.");
            e.preventDefault();
            return;
        }));

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
        div.appendChild(h4);
    
        fragment.appendChild(div);
        
        document.querySelector('main').appendChild(fragment);
        
    }
})();
    