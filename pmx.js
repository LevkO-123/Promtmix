
// Promtmix common JS
function fmt(n){return (Math.round((n + Number.EPSILON)*100000)/100000).toString();}

// Affiliate utils
const PMX = {
  amazonTag: 'promtmix20-20',
  sovrnKey: '2422504'
};

// Insert Sovrn Commerce (VigLink) if key present
(function(){
  if(PMX.sovrnKey && PMX.sovrnKey !== 'CHANGE_ME'){
    var s=document.createElement('script'); s.type='text/javascript'; s.async=true;
    var vglnk = { key: PMX.sovrnKey };
    window.vglnk = vglnk;
    s.src='//cdn.viglink.com/api/vglnk.js';
    var h=document.getElementsByTagName('head')[0]; h.appendChild(s);
  }
})();

// Convert data-amazon-query links into affiliate links
function attachAmazonLinks(){
  document.querySelectorAll('a[data-amazon-query]').forEach(a=>{
    const q = encodeURIComponent(a.getAttribute('data-amazon-query'));
    a.href = 'https://www.amazon.com/s?k='+q+'&tag='+PMX.amazonTag;
    a.rel = 'sponsored nofollow noopener';
  });
}
document.addEventListener('DOMContentLoaded', attachAmazonLinks);
