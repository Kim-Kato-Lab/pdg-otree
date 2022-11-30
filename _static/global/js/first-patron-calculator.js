function pi() {
  var min_multiply = 0;
  var max_multiply = 200;
  var send = parseInt(document.getElementById("send").value);

  var piP = document.getElementById("piP");
  var cal_piP = 100 - send;
  var cal_piP = Math.round(cal_piP);
  piP.innerText = cal_piP;

  var piD = document.getElementById("piD");
  var cal_minD = 100 - (min_multiply / 100 - 1) * send;
  var cal_minD = Math.round(cal_minD);
  var cal_maxD = 100 - (max_multiply / 100 - 1) * send;
  var cal_maxD = Math.round(cal_maxD);

  if (cal_minD == cal_maxD) {
    piD.innerText = cal_minD;
  } else if (cal_minD > cal_maxD) {
    piD.innerText =
      cal_maxD + "～" + cal_minD + "（メンバーDの選択で変化します）";
  } else {
    piD.innerText =
      cal_minD + "～" + cal_maxD + "（メンバーDの選択で変化します）";
  }

  var piR = document.getElementById("piR");
  var cal_minR = (send * min_multiply) / 100;
  var cal_minR = Math.round(cal_minR);
  var cal_maxR = (send * max_multiply) / 100;
  var cal_maxR = Math.round(cal_maxR);

  if (cal_minR == cal_maxR) {
    piR.innerText = cal_minR;
  } else if (cal_minR > cal_maxR) {
    piR.innerText =
      cal_maxR + "～" + cal_minR + "（メンバーDの選択で変化します）";
  } else {
    piR.innerText =
      cal_minR + "～" + cal_maxR + "（メンバーDの選択で変化します）";
  }
}
