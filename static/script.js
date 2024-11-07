function likePaste(pasteId) {
    fetch(`/like/${pasteId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.likes !== undefined) {
            document.querySelectorAll('.paste-card .actions span')[pasteId].textContent = `${data.likes} ❤️`;
        } else if (data.message) {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
