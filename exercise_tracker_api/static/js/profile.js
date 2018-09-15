(function() {
    window.addEventListener('load', (e) => {

        const deleteBtn = document.querySelector('#delete');
        deleteBtn.addEventListener('click', (e) => {
            if(!confirm("Are you sure you want to delete your account?")) {
                e.preventDefault();
                console.log('you decided to not remove your account.');
                return;
            } 
        
        });

        

    });
})();
    