function pi() {
  let send = js_vars.x;
  var multiply = parseInt(document.getElementById("multiply").value);

  var piP = document.getElementById("piP");
  var cal_piP = 100 - send;
  var cal_piP = Math.round(cal_piP);
  piP.innerText = cal_piP;

  var piD = document.getElementById("piD");
  var cal_piD = 100 - (multiply / 100 - 1) * send;
  var cal_piD = Math.round(cal_piD);
  piD.innerText = cal_piD;

  var piR = document.getElementById("piR");
  var cal_piR = (send * multiply) / 100;
  var cal_piR = Math.round(cal_piR);
  piR.innerText = cal_piR;
}
