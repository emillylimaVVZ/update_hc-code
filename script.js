function menuOnClick() {
  document.getElementById("menu-bar").classList.toggle("change");
  document.getElementById("nav").classList.toggle("change");
  document.getElementById("menu-bg").classList.toggle("change-bg");
}





document.querySelectorAll('.packet-loss').forEach(function(td) {
  const packetLoss = parseFloat(td.innerText);
  if (packetLoss <= 20) {
    td.classList.add('green');
  } else if (packetLoss >= 80) {
    td.classList.add('red');
  }
});

document.querySelectorAll('.avg-time').forEach(function(td) {
  const avgTime = parseFloat(td.innerText.replace('ms', ''));
  if (avgTime <= 20) {
    td.classList.add('green');
  } else if (avgTime >= 80) {
    td.classList.add('red');
  }
});


