
const PMX = {
  amazonTag: 'promtmix20-20',
  sovrnKey: '2422504'
};
(function(){
  if(PMX.sovrnKey && PMX.sovrnKey !== 'CHANGE_ME'){
    var s=document.createElement('script'); s.type='text/javascript'; s.async=true;
    window.vglnk = { key: PMX.sovrnKey };
    s.src='//cdn.viglink.com/api/vglnk.js';
    document.head.appendChild(s);
  }
})();
function attachAmazonLinks(){
  document.querySelectorAll('a[data-amazon-query]').forEach(a=>{
    const q = encodeURIComponent(a.getAttribute('data-amazon-query'));
    a.href = 'https://www.amazon.com/s?k='+q+'&tag='+PMX.amazonTag;
    a.rel = 'sponsored nofollow noopener';
  });
}
document.addEventListener('DOMContentLoaded', attachAmazonLinks);
