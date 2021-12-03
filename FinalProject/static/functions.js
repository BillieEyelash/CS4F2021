function addBook(id)
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		   var button = document.getElementById(id);
		   button.innerHTML = "Added to your books";
		}
  };
  xhttp.open("POST", "/addBook", true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send("book=" + id);
}
