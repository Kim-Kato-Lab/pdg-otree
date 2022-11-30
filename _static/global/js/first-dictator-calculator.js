function pi() {
  var min_send = 0;
  var max_send = 100;
  var multiply = parseInt(document.getElementById("multiply").value);

  var piP = document.getElementById("piP");
  piP.innerText =
    min_send + "～" + max_send + "（メンバーPの選択で変化します）";

  var piD = document.getElementById("piD");
  var cal_minD = 100 - (multiply / 100 - 1) * min_send;
  var cal_minD = Math.round(cal_minD);
  var cal_maxD = 100 - (multiply / 100 - 1) * max_send;
  var cal_maxD = Math.round(cal_maxD);

  if (cal_minD == cal_maxD) {
    piD.innerText = cal_minD;
  } else if (cal_minD > cal_maxD) {
    piD.innerText =
      cal_maxD + "～" + cal_minD + "（メンバーPの選択で変化します）";
  } else {
    piD.innerText =
      cal_minD + "～" + cal_maxD + "（メンバーPの選択で変化します）";
  }

  var piR = document.getElementById("piR");
  var cal_minR = (min_send * multiply) / 100;
  var cal_minR = Math.round(cal_minR);
  var cal_maxR = (max_send * multiply) / 100;
  var cal_maxR = Math.round(cal_maxR);

  if (cal_minR == cal_maxR) {
    piR.innerText = cal_minR;
  } else if (cal_minR > cal_maxR) {
    piR.innerText =
      cal_maxR + "～" + cal_minR + "（メンバーPの選択で変化します）";
  } else {
    piR.innerText =
      cal_minR + "～" + cal_maxR + "（メンバーPの選択で変化します）";
  }
}
