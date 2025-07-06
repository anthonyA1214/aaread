function previewCover(event) {
    const input = event.target;
    const file = input.files[0];
    const preview = document.getElementById('coverPreview');
    const placeholder = document.getElementById('placeholder');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            placeholder.style.display = 'none';
            console.log("Image preview updated");
        };
        reader.readAsDataURL(file);
    } else {
        preview.src = '';
        preview.style.display = 'none';
        placeholder.style.display = 'flex';
    }
}
