function addBook(id)
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      // If user is not logged in display an error message
      if (this.responseText.localeCompare('error') == 0) {
        // Error message
        let alert = document.createElement('div');
        alert.innerHTML = 'You are not logged in! ';
        alert.role = 'alert';
        alert.classList.add('alert');
        alert.classList.add('alert-danger');
        // Link to login
        let link = document.createElement('a')
        link.href = 'login'
        link.innerHTML = 'Sign in here!'
        link.classList.add('alert-link')
        // Add link to error
        alert.appendChild(link)
        // Add error to the top of the page
        let parent = document.getElementById('body');
        let after = parent.children[0];
        parent.insertBefore(alert, after);
      } else {
        // If logged in modify button text
        let button = document.getElementById(id);
        button.innerHTML = 'saved';
      }
		}
  };
  xhttp.open('POST', '/addBook', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send('book=' + id);
}
