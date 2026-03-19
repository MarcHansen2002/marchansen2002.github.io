const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

let particles=[];

function resize(){
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;
}

window.addEventListener("resize",resize);
resize();

for(let i=0;i<80;i++){

particles.push({

x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5)*0.15,
vy:(Math.random()-0.5)*0.15

});

}

function update(){

ctx.clearRect(0,0,canvas.width,canvas.height);

particles.forEach(p=>{

p.x+=p.vx;
p.y+=p.vy;

if(p.x<0||p.x>canvas.width)p.vx*=-1;
if(p.y<0||p.y>canvas.height)p.vy*=-1;

ctx.fillStyle="#38bdf8";
ctx.fillRect(p.x,p.y,2,2);

});

requestAnimationFrame(update);

}

update();