function follower_dictator_payoff() {
  const send = js_vars.x;
  const type2 = js_vars.type2;
  const input = document.getElementById("multiply");
  const multiply = input.value;

  // for debug
  // console.log(multiply);
  console.log(type2)

  const alert_msg = "0から200の整数で入力してください";

  if (!multiply) {
    return alert(alert_msg);
  }

  if ((multiply < 0) | (200 < multiply)) {
    input.value = "";
    return alert(alert_msg);
  }

  if (multiply % 1 != 0) {
    input.value = "";
    return alert(alert_msg);
  }

  let p = document.getElementById("result-p");
  const cal_p = Math.round(100 - send);
  p.innerText = cal_p + "トークン";

  let d = document.getElementById("result-d");
  const cal_d = Math.round(100 - (multiply / 100 - 1) * send);

  let r = document.getElementById("result-r");
  const cal_r = Math.round((send * multiply) / 100);
  r.innerText = cal_r + "トークン";

  let text_d;
  if (type2) {
    text_d = cal_r + "トークン";
  } else {
    text_d = cal_d + "トークン";
  }
  d.innerText = text_d;

}
