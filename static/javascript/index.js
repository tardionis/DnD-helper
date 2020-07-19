var extern = document.getElementsByTagName("link")[0].import;

$(document).ready({
  $.get("Schaumal.txt", function(ans){$("#box").html(ans);});
});

if ("import" in document.createElement("link")) {
  // HTML5-Imports werden unterstützt.
  window.addEventListener("load", function() {
    document.getElementsByTagName("html")[0].replaceChild(extern.getElementsByTagName("body")[0], document.getElementsByTagName("body")[0]);
  }, false);
}

function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("sidebar-table");//Hier id der Tabelle eintragen
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
