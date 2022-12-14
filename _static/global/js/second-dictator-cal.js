function pi() {
  const send = js_vars.x;
  const input = document.getElementById("multiply");
  const multiply = input.value;

  // for debug
  // console.log(multiply);

  const alert_msg = "選択してください";

  if (!multiply) {
    return alert(alert_msg);
  }

  let p = document.getElementById("sd-calculator-result-p");
  const cal_p = Math.round(100 - send);
  p.innerText = cal_p;

  let d = document.getElementById("sd-calculator-result-d");
  const cal_d = Math.round(100 - (multiply / 100 - 1) * send);
  d.innerText = cal_d;

  let r = document.getElementById("sd-calculator-result-r");
  const cal_r = Math.round((send * multiply) / 100);
  r.innerText = cal_r;
}
