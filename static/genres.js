const editModal = document.getElementById('editGenre')

editModal.addEventListener('show.bs.modal', (e) => {
    button = e.relatedTarget;
    genreId = button.getAttribute('data-id')
    genreName = button.getAttribute('data-name')

    inputId = editModal.querySelector('#editGenreId')
    inputName = editModal.querySelector('#editGenreName')
    form = editModal.querySelector('#editGenreForm')

    inputId.value = genreId
    inputName.value = genreName

    form.action = `/admin/genres/${genreId}/edit`;
});