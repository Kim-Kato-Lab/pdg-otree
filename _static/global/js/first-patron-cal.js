function pi() {
  const min_multiply = 0;
  const max_multiply = 200;
  const input = document.getElementById("send");
  const send = input.value;

  // for debug
  // console.log(send);

  const alert_msg = "0から100の整数で入力してください";

  if (!send) {
    return alert(alert_msg);
  }

  if (send < 0 | 100 < send) {
    input.value = '';
    return alert(alert_msg);
  }

  if (send % 1 != 0) {
    input.value = '';
    return alert(alert_msg);
  }

  let p = document.getElementById("sd-calculator-result-p");
  const cal_p = Math.round(100 - send);
  p.innerText = cal_p

  let d = document.getElementById("sd-calculator-result-d");
  const cal_minD = Math.round(100 - (min_multiply / 100 - 1) * send);
  const cal_maxD = Math.round(100 - (max_multiply / 100 - 1) * send);
  
  if (cal_maxD == cal_maxD) {
    d.innerHTML = cal_minD;
  } else if (cal_minD > cal_maxD) {
    d.innerHTML =
      cal_maxD + "～" + cal_minD + "（メンバーＤの選択で変化します）";
  } else {
    d.innerHTML = 
      cal_minD + '～' + cal_maxD + "（メンバーＤの選択で変化します）";
  }

  let r = document.getElementById("sd-calculator-result-r");
  const cal_minR = Math.round((send * min_multiply) / 100);
  const cal_maxR = Math.round((send * max_multiply) / 100);

  if (cal_minR == cal_maxR) {
    r.innerText = cal_minR;
  } else if (cal_minR > cal_maxR) {
    r.innerText =
      cal_maxR + "～" + cal_minR + "（メンバーＤの選択で変化します）";
  } else {
    r.innerText =
      cal_minR + "～" + cal_maxR + "（メンバーＤの選択で変化します）";
  }
}
