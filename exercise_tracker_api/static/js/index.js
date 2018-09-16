(function() {
    window.addEventListener('load', (e) => {
        if(document.querySelector('.error')) {
            document.querySelector('.error').addEventListener('animationend', (e) => {
                document.querySelector('.error').remove();
            });
        }
    });
})();