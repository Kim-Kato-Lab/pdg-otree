function payoff() {
  const input_x = document.getElementById('send');
  const input_s = document.getElementById('multiply');
  const x = input_x.value;
  const s = input_s.value;

  const alert_msg_s = "メンバーDの選択を0から200の整数で入力してください";
  const alert_msg_x = "メンバーPの選択を0から100の整数で入力してください";

  if (!x) {
    return alert(alert_msg_x);
  }

  if ((x < 0) | (100 < x)) {
    input_x.value = "";
    return alert(alert_msg_x);
  }

  if (x % 1 != 0) {
    input_x.value = "";
    return alert(alert_msg_x);
  }

  if (!s) {
    return alert(alert_msg_s);
  }

  if ((s < 0) | (200 < s)) {
    input_s.value = "";
    return alert(alert_msg_s);
  }

  if (s % 1 != 0) {
    input_s.value = "";
    return alert(alert_msg_s);
  }

  liveSend({'x': x, 's': s})

  let p = document.getElementById("result-p");
  let d1 = document.getElementById("result-d-type1");
  let d2 = document.getElementById("result-d-type2");
  let r = document.getElementById("result-r");

  const cal_p = Math.round(100 - x);
  const cal_d = Math.round(100 - (s / 100 - 1) * x);
  const cal_r = Math.round((x * s) / 100);

  p.innerText = cal_p + 'トークン';
  if (d1 != null) {
    d1.innerText = cal_d + "トークン";
  }
  if (d2 != null) {
    d2.innerText = cal_r + "トークン";
  }
  r.innerText = cal_r + 'トークン';
}