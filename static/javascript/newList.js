function addColumn() {
  var itm = document.getElementById("column").lastChild;
  var cln = itm.cloneNode(true);
  //cln.firstChild.value = "";
  document.getElementById("column").appendChild(cln);
}
