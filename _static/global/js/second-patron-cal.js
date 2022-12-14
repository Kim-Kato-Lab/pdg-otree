function pi() {
  const multiply = js_vars.x;
  const input = document.getElementById("send");
  const send = input.value;

  // for debug
  // console.log(send);

  const alert_msg = "0から100の整数で入力してください";

  if (!send) {
    return alert(alert_msg);
  }

  if ((send < 0) | (100 < send)) {
    input.value = "";
    return alert(alert_msg);
  }

  if (send % 1 != 0) {
    input.value = "";
    return alert(alert_msg);
  }

  let p = document.getElementById("fd-calculator-result-p");
  const cal_p = Math.round(100 - send);
  p.innerText = cal_p;

  let d = document.getElementById("fd-calculator-result-d");
  const cal_d = Math.round(100 - (multiply / 100 - 1) * send);
  d.innerText = cal_d;

  var r = document.getElementById("fd-calculator-result-r");
  const cal_r = Math.round((send * multiply) / 100);
  r.innerText = cal_r;
}
