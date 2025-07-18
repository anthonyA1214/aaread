document.querySelectorAll('.addToLibraryBtn').forEach(btn => {
    btn.addEventListener('click', function() {
        const novelId = this.dataset.novelId;
        const button = this;

        fetch('/add-to-library', {
            method: 'POST',       
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({novel_id: novelId})   
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.innerHTML = '<i class="bi bi-check2"></i> Added';
                button.classList.remove('btn-primary');
                button.classList.add('btn-success');
                button.disabled = true;
            } else {
                alert(data.message || "Failed to add to library.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.querySelectorAll('.removeFromLibraryBtn').forEach(btn => {
    btn.addEventListener('click', function() {
        const novelId = this.dataset.novelId;
        const button = this;

        fetch('/remove-from-library', {
            method: 'POST',       
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({novel_id: novelId})   
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.innerHTML = '<i class="bi bi-check2"></i> Removed';
                button.classList.remove('btn-primary');
                button.classList.add('btn-danger');
                button.disabled = true;
            } else {
                alert(data.message || "Failed to remove from library.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
