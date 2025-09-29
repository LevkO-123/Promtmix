
// === Affiliate IDs ===
const PMX = {
  amazonTag: 'promtmix20-20',
  sovrnKey: '2422504'
};

// === Ripple on buttons ===
document.addEventListener('pointermove', e => {
  const t = e.target.closest('.button');
  if(!t) return;
  const rect = t.getBoundingClientRect();
  t.style.setProperty('--x', (e.clientX-rect.left)+'px');
  t.style.setProperty('--y', (e.clientY-rect.top)+'px');
});

// === Count-up helper ===
function animateNumber(el, from, to, ms=600){
  const start = performance.now();
  function step(now){
    const p = Math.min(1,(now-start)/ms);
    const val = from + (to-from)*p;
    el.textContent = (Math.round(val*100)/100).toString();
    if(p<1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// === Sovrn Commerce (VigLink) ===
(function(){
  if(PMX.sovrnKey && PMX.sovrnKey !== 'CHANGE_ME'){
    var s=document.createElement('script'); s.type='text/javascript'; s.async=true;
    window.vglnk = { key: PMX.sovrnKey };
    s.src='//cdn.viglink.com/api/vglnk.js';
    document.head.appendChild(s);
  }
})();

// === Amazon search links ===
function attachAmazonLinks(){
  document.querySelectorAll('a[data-amazon-query]').forEach(a=>{
    const q = encodeURIComponent(a.getAttribute('data-amazon-query'));
    a.href = 'https://www.amazon.com/s?k='+q+'&tag='+PMX.amazonTag;
    a.rel = 'sponsored nofollow noopener';
  });
}
document.addEventListener('DOMContentLoaded', attachAmazonLinks);

// === Matrix-like background (lightweight) ===
(function(){
  const canvas = document.createElement('canvas');
  canvas.style.position='fixed';canvas.style.left=0;canvas.style.top=0;
  canvas.style.width='100%';canvas.style.height='100%';canvas.style.zIndex=0;
  canvas.style.pointerEvents='none'; document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  function resize(){canvas.width=innerWidth;canvas.height=innerHeight}
  addEventListener('resize',resize); resize();
  let cols = Math.floor(innerWidth/18), ypos = Array(cols).fill(0);
  function draw(){
    ctx.fillStyle='rgba(4,18,10,0.12)'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='rgba(0,255,159,0.1)'; ctx.font='14px monospace';
    for(let i=0;i<ypos.length;i++){
      const text = String.fromCharCode(0x30A0 + Math.random()*96);
      ctx.fillText(text, i*18, ypos[i]*18);
      if(ypos[i]*18 > canvas.height && Math.random() > 0.975) ypos[i]=0;
      ypos[i]++;
    }
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
})();
