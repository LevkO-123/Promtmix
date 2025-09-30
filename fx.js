
const PMX = { amazonTag:'promtmix20-20', sovrnKey:'2422504' };

document.addEventListener('pointermove', e=>{ const t=e.target.closest('.button'); if(!t) return; const r=t.getBoundingClientRect(); t.style.setProperty('--x',(e.clientX-r.left)+'px'); t.style.setProperty('--y',(e.clientY-r.top)+'px'); });
function countTo(el,val,ms=500){ const s=performance.now(); const f=parseFloat(el.getAttribute('data-from')||0); const step=(n)=>{const p=Math.min(1,(n-s)/ms); const v=f+(val-f)*p; el.textContent=(Math.round(v*100)/100); if(p<1) requestAnimationFrame(step); else el.setAttribute('data-from', val);}; requestAnimationFrame(step); }
function attachAmazonLinks(){ document.querySelectorAll('a[data-amazon-query]').forEach(a=>{ const q=encodeURIComponent(a.getAttribute('data-amazon-query')); a.href='https://www.amazon.com/s?k='+q+'&tag='+PMX.amazonTag; a.rel='sponsored nofollow noopener'; }); }
(function(){ if(PMX.sovrnKey){ var s=document.createElement('script'); s.async=true; window.vglnk={key:PMX.sovrnKey}; s.src='//cdn.viglink.com/api/vglnk.js'; document.head.appendChild(s); } })();

function openDrawer(){ document.querySelector('.drawer').classList.add('open'); document.querySelector('.drawer-backdrop').classList.add('open'); }
function closeDrawer(){ document.querySelector('.drawer').classList.remove('open'); document.querySelector('.drawer-backdrop').classList.remove('open'); }

(function(){ const c=document.createElement('canvas'); c.width=innerWidth; c.height=innerHeight; c.style.position='fixed'; c.style.inset=0; c.style.zIndex=1; c.style.pointerEvents='none'; c.style.opacity=.12; document.body.appendChild(c); const x=c.getContext('2d'); function r(){c.width=innerWidth;c.height=innerHeight}; addEventListener('resize',r); let t=0; (function L(){ x.clearRect(0,0,c.width,c.height); for(let i=0;i<3;i++){ x.beginPath(); for(let px=0;px<c.width;px+=4){ const y=Math.sin(px*0.006+t*0.002+i)*8 + Math.cos(px*0.003-t*0.003-i)*6 + c.height*0.25 + i*70; x.lineTo(px,y); } x.strokeStyle = ['#00E0A366','#5B8CFF66','#C084FC55'][i]; x.lineWidth=1.5; x.stroke(); } t++; requestAnimationFrame(L); })(); })();

async function loadNews(section, container){ 
  const feeds = {
    us: "https://news.google.com/rss/headlines/section/geo/United%20States?hl=en-US&gl=US&ceid=US:en",
    ca: "https://news.google.com/rss/headlines/section/geo/Canada?hl=en-US&gl=US&ceid=US:en",
    eu: "https://news.google.com/rss/search?q=Europe&hl=en-US&gl=US&ceid=US:en",
    world: "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    crypto: "https://news.google.com/rss/search?q=cryptocurrency%20OR%20bitcoin%20OR%20ethereum&hl=en-US&gl=US&ceid=US:en",
    tech: "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en"
  };
  const url = 'https://r.jina.ai/http/' + feeds[section].replace('https://','');
  try {
    const txt = await fetch(url).then(r=>r.text());
    const items = [...txt.matchAll(/<item>([\s\S]*?)<\/item>/g)].slice(0,12).map(m=>{ const part=m[1]; const t=(part.match(/<title>([\s\S]*?)<\/title>/)||['',''])[1]; const l=(part.match(/<link>([\s\S]*?)<\/link>/)||['',''])[1]; const p=(part.match(/<pubDate>([\s\S]*?)<\/pubDate>/)||['',''])[1]; const d=(part.match(/<description>([\s\S]*?)<\/description>/)||['',''])[1].replace(/<[^>]*>/g,''); return {t, l, p, d}; });
    container.innerHTML = items.map(it=>`<div class="news-item"><h4><a href="${it.l}" target="_blank" rel="noopener nofollow">${it.t}</a></h4><div class="news-meta">${it.p}</div><div class="small">${it.d}</div></div>`).join('');
  } catch(e) { container.innerHTML = '<div class="small">Could not load news.</div>'; }
}

document.addEventListener('DOMContentLoaded', attachAmazonLinks);
