function opferWahl(opfer, ac) {
  getVisible("attacke");
  getVisible("gegenstand");
  document.getElementById("opfer").value = opfer;
  document.getElementById("ac").value = ac;
}

function reverseOpferWahl() {
  getInvisible("attacke");
  getInvisible("gegenstand");
  getInvisible("treffer");
}

function attackWahl(att, dam) {
  document.getElementById("attackWurf").placeholder = "add " + att;
  document.getElementById("damageWurf").placeholder = dam;
}

function treffer() {
  var ac = document.getElementById("ac").value;
  var attackWurf = document.getElementById("attackWurf").value;
  if (ac <= attackWurf) {
    getVisible("treffer");
  } else {
    getInvisible("attacke");
    getInvisible("gegenstand");
    getInvisible("treffer");
    alert("Der Schlag ging daneben")
  }
}

function getInvisible(id) {
  var x = document.getElementById(id);
  if (x.style.display === "") {
    x.style.display = "none";
  }
}

function getVisible(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "";
  }
}
