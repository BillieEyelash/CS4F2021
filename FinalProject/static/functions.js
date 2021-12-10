function addBook(id)
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText.localeCompare('error') == 0) {
        let alert = document.createElement('div');
        alert.innerHTML = 'You are not logged in!';
        alert.role = 'alert';
        alert.classList.add('alert');
        alert.classList.add('alert-danger');
        let parent = document.getElementById('body');
        let after = parent.children[0];
        parent.insertBefore(alert, after);
      } else {
        let button = document.getElementById(id);
        button.innerHTML = 'saved';
      }
		}
  };
  xhttp.open('POST', '/addBook', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send('book=' + id);
}
