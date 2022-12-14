function pi() {
  const min_send = 0;
  const max_send = 100;
  const input = document.getElementById("multiply");
  const multiply = input.value;

  // for debug
  // console.log(multiply);

  const alert_msg = "選択してください";

  if (!multiply) {
    return alert(alert_msg);
  }

  let p = document.getElementById("fd-calculator-result-p");
  p.innerText =
    min_send + "～" + max_send + "（メンバーＰの選択で変化します）";

  let d = document.getElementById("fd-calculator-result-d");
  const cal_minD = Math.round(100 - (multiply / 100 - 1) * min_send);
  const cal_maxD = Math.round(100 - (multiply / 100 - 1) * max_send);
  
  if (cal_minD == cal_maxD) {
    d.innerText = cal_minD;
  } else if (cal_minD > cal_maxD) {
    d.innerText =
      cal_maxD + "～" + cal_minD + "（メンバーＰの選択で変化します）";
  } else {
    d.innerText =
      cal_minD + "～" + cal_maxD + "（メンバーＰの選択で変化します）";
  }

  let r = document.getElementById("fd-calculator-result-r");
  const cal_minR = Math.round((min_send * multiply) / 100);
  const cal_maxR = Math.round((max_send * multiply) / 100);
  
  if (cal_minR == cal_maxR) {
    r.innerText = cal_minR;
  } else if (cal_minR > cal_maxR) {
    r.innerText =
      cal_maxR + "～" + cal_minR + "（メンバーＰの選択で変化します）";
  } else {
    r.innerText =
      cal_minR + "～" + cal_maxR + "（メンバーＰの選択で変化します）";
  }
}
