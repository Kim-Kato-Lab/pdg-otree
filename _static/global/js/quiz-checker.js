function check_q1() {
  liveSend("q1")
}

function check_q2() {
  liveSend("q2")
}

function check_q3() {
  liveSend("q3")
}

function check_q4() {
  liveSend("q4");
}

function check_q5() {
  liveSend("q5")
}

function liveRecv(data) {
  const btn = document.getElementById("next");
  if (data === "go") {
    btn.disabled = null;
  } else {
    btn.disabled = "disabled"
  }
}