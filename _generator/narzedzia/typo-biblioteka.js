(function(g){
var A='\xA0',T='\u2009',M='\u202f',U='A-ZĄĆĘŁŃÓŚŹŻ',W='A-Za-zÀ-ɏ',
P=/(https?:\/\/\S+|www\.\S+|[\w.+-]+@[\w-]+\.[\w.-]+|\x60{3}[\s\S]*?\x60{3}|\x60[^\x60\n]*\x60)/;
function f(s,st,n){
s=s.replace(/[ \t]{2,}/g,' ')
.replace(/\.{3}/g,'…').replace(/([!?])\1+/g,'$1')
.replace(/(\d)[ \t]-[ \t](?=\d)/g,'$1 − ')
.replace(/(\S)[ \t](?:-{1,2}|—)[ \t](?=\S)/g,'$1'+A+'– ')
.replace(new RegExp('(^|[^\\d-])(\\d+)[-–—](\\d+)(?![\\d-])','g'),function(m,p,a,b){return/^\d\d$/.test(a)&&/^\d{3}$/.test(b)?m:p+a+'–'+b})
.replace(/(^|[^\w])(\d+)([ \t]?)[x×]([ \t]?)(\d+)/g,function(m,p,a,s1,s2,b){return a==='0'&&!s1&&!s2?m:p+a+'×'+b})
.replace(/\+-/g,'±').replace(/!=/g,'≠').replace(/(^|\s)-(?=\d)/g,'$1−')
.replace(/(^|[\s(])([13])\/([24])(?![\d\/])/g,function(m,p,a,b){var r={'12':'½','14':'¼','34':'¾'}[a+b];return r?p+r:m})
.replace(/\(c\)/gi,'©').replace(/\(tm\)/gi,'™').replace(/\(r\)/gi,'®')
.replace(new RegExp('(\\d)(?:\\s?°\\s?|\\s)([CF])(?![A-Za-z\\dÀ-ɏ])','g'),'$1'+T+'°$2')
.replace(/(\d)'(?=\d)/g,'$1′').replace(/(\d)"/g,'$1″');
if(n)return s;
s=s.replace(/ +([,.;:!?)\]])/g,'$1').replace(/([(\[]) +/g,'$1').replace(new RegExp(',(?=['+W+'])','g'),', ')
.replace(new RegExp('(['+W+'])\'(?=['+W+'])','g'),'$1’')
.replace(/"/g,function(m,i,t){var c=i?t.charAt(i-1):(st.p||' '),o=/[\s(\[{„«–—-]/.test(c);
if(o){st.d++;return st.d>1?'«':'„'}var r=st.d>1?'»':'”';if(st.d>0)st.d--;return r})
.replace(/([aiouwzAIOUWZ])\s(?=\S)/g,function(m,c,i,t){return/[\s(„«]/.test(i?t.charAt(i-1):' ')?c+A:m})
.replace(new RegExp('(^|[^'+W+'.])((?:['+U+']\\.\\s?)+)(?=['+U+'][a-ząćęłńóśźż]{2,})','g'),function(m,p,i){return p+i.replace(/\.\s?/g,'.'+M).replace(new RegExp(M+'$'),A)})
.replace(/(^|[^\d.,\/:-])(\d{5,})(?![\d\/:-])/g,function(m,p,d){return/^(10|11|13|16)$/.test(d.length)?m:p+d.replace(/\B(?=(\d{3})+$)/g,M)});
return s}
function tp(s,st,n){st=st||{d:0};var r=s.split(P).map(function(c,i){return i%2?c:f(c,st,n)}).join('');st.p=r.slice(-1);return r}
g.tp=tp;
if(typeof document==='undefined'){
if(typeof module!=='undefined'){module.exports={tp:tp};
if(require.main===module){var d='';process.stdin.on('data',function(c){d+=c}).on('end',function(){process.stdout.write(tp(d))})}}
return}
if(g.TYPO_OFF)return;
var X='[data-notp],script,style,code,pre,kbd,samp,textarea,input,select,option,title,noscript,[contenteditable=true]',
B='p,li,h1,h2,h3,h4,h5,h6,td,th,dd,dt,figcaption,blockquote,div',
pl=function(e){return/^pl/i.test((e.closest('[lang]')||document.documentElement).lang||'pl')};
function run(r){
var x=[],w,n,S=new Map;
if(r.nodeType===3)x=[r];else if(r.nodeType===1){w=document.createTreeWalker(r,4);while(n=w.nextNode())x.push(n)}
x.forEach(function(n){var e=n.parentNode;if(!e||!e.closest||e.closest(X))return;
var b=e.closest(B)||document.body,st=S.get(b);if(!st)S.set(b,st={d:0});
var v=tp(n.nodeValue,st,!pl(e));if(v!==n.nodeValue)n.nodeValue=v});
if(r.querySelectorAll)r.querySelectorAll('p,li,dd,figcaption,blockquote').forEach(function(p){
var t=p.lastChild;if(t&&t.nodeType===3&&!p.closest(X)&&pl(p))t.nodeValue=t.nodeValue.replace(/\s(\S{1,4})\s*$/,A+'$1')})}
function toc(){var t=document.querySelector('[data-toc]');if(!t)return;
var h=document.querySelectorAll('main h2,main h3,article h2,article h3');if(!h.length)h=document.querySelectorAll('h2,h3');
var o=document.createElement('ol');h.forEach(function(e,i){if(!e.id)e.id='r'+i;var li=document.createElement('li'),a=document.createElement('a');
a.href='#'+e.id;a.textContent=e.textContent;li.append(a);if(e.tagName==='H3')li.style.marginInlineStart='1.5em';o.append(li)});
t.classList.add('toc');t.setAttribute('aria-label','Spis treści');t.append(o)}
function rh(){var r=document.querySelector('[data-rh]'),h=[].slice.call(document.querySelectorAll('h2'));if(!r||!h.length)return;
r.classList.add('rh');r.setAttribute('aria-hidden','true');var q=0,u=function(){q=0;var i=0;h.forEach(function(x,k){if(x.getBoundingClientRect().top<=96)i=k});r.textContent='§ '+(i+1)+' · '+h[i].textContent};
u();addEventListener('scroll',function(){q=q||requestAnimationFrame(u)},{passive:true})}
function mm(){if(!document.documentElement.hasAttribute('data-miernik')&&!/[?&]miernik/.test(location.search))return;
var L=document.createElement('div'),d=function(){L.textContent='';var a=[];document.querySelectorAll('main p,article p,.t p').forEach(function(p){
var l=[],w=document.createTreeWalker(p,4),r=document.createRange(),t,i,b,m,o;
while(t=w.nextNode())for(i=0;i<t.length;i++){r.setStart(t,i);r.setEnd(t,i+1);b=r.getClientRects()[0];if(!b)continue;m=b.top+b.height/2;o=l[l.length-1];
if(o&&Math.abs(o.m-m)<10)o.n++;else l.push({m:m,y:b.top,x:b.left,n:1})}
l.forEach(function(o,k){var s=document.createElement('span');s.className='mm';s.textContent=o.n;s.style.cssText='top:'+(o.y+scrollY)+'px;left:'+Math.max(0,o.x+scrollX-34)+'px';L.append(s);if(k<l.length-1)a.push(o.n)})});
L.title=a.length?'znaków w wierszu: średnio '+Math.round(a.reduce(function(x,y){return x+y},0)/a.length):''};
document.body.append(L);(document.fonts?document.fonts.ready:Promise.resolve()).then(d);addEventListener('resize',function(){setTimeout(d,150)})}
function init(){run(document.body);toc();rh();mm();var q=[],p=0;
new MutationObserver(function(m){m.forEach(function(x){x.addedNodes.forEach(function(n){q.push(n)});if(x.type==='characterData')q.push(x.target)});
if(!p){p=1;requestAnimationFrame(function(){p=0;q.splice(0).forEach(run)})}}).observe(document.body,{childList:true,subtree:true,characterData:true})}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()
})(typeof window!=='undefined'?window:globalThis);
