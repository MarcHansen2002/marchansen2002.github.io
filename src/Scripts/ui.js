const buttons = document.querySelectorAll(".sidebar button");
const panels = document.querySelectorAll(".panel");

buttons.forEach(btn=>{

btn.onclick = ()=>{

const id = btn.dataset.panel;

panels.forEach(p=>p.classList.remove("active"));

document.getElementById(id).classList.add("active");

};

});