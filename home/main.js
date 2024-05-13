// main.js
   document.addEventListener('DOMContentLoaded', function() {
        const addPostForm = document.getElementById('add-post-form');
        addPostForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(addPostForm);
            fetch('/add_post', {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Handle response
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle error
            });
        });
    });
