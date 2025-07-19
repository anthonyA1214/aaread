document.querySelectorAll('.toggleLibraryBtn').forEach(btn => {
    btn.addEventListener('click', function() {
        const novelId = this.dataset.novelId;
        const button = this;
        const inLibrary = button.classList.contains('in-library')

        fetch(inLibrary ? '/remove-from-library' : '/add-to-library', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ novel_id: novelId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (inLibrary) {
                    // Switched to not in library
                    button.innerHTML = '<i class="bi bi-plus"></i> Add to Library';
                    button.classList.remove('btn-success', 'in-library');
                    button.classList.add('btn-primary')
                } else {
                    // Switched to in library
                    button.innerHTML = '<i class="bi bi-check2"></i> In Library';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-success', 'in-library')
                }
            } else {
                alert(data.message || "Operation failed.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});