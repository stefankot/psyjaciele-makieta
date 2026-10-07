const t=document.querySelector('.menu-toggle');const m=document.querySelector('#menu');function close(){t.setAttribute('aria-expanded','false');m.classList.remove('is-open');t.setAttribute('aria-label','Otwórz menu');header?.classList.remove('menu-open');}t.addEventListener('click',()=>{const open=t.getAttribute('aria-expanded')!=='true';t.setAttribute('aria-expanded',String(open));m.classList.toggle('is-open',open);header.classList.toggle('menu-open',open);t.setAttribute('aria-label',open?'Zamknij menu':'Otwórz menu');});m.addEventListener('click',event=>{if(event.target.closest('a'))close();});document.addEventListener('keydown',event=>{if(event.key==='Escape' && t.getAttribute('aria-expanded')==='true'){close();t.focus();}}); const s=document.querySelector('.about');const h=document.querySelector('.portrait-halo');const rm=window.matchMedia('(prefers-reduced-motion: reduce)');const ds=[];  const basePetSize=0.1;const D=basePetSize*1.3;const G=0.035*1.3;const P=D+G;const R=0.5+0.012+D/2;const rs=[0,1,2,3].map(i=>{const radius=R+i*P;const step=2*Math.asin(P/(2*radius));let count=Math.floor(Math.PI/step)+1;if(count % 2===0)count--;return{radius,step,count};});let q=731;function rand(){q=(q*16807)% 2147483647;return(q - 1)/2147483646;}const petNames=['Luna','Fafik','Burek','Maja','Reksio','Kluska','Mruczek','Tofik','Kulka','Figa','Azor','Pieróg','Pusia','Max','Łatek','Stefan','Roki','Misia','Karmel','Gucio','Pestka','Tosia','Bąbel','Filemon','Nela','Bigos','Bela','Dżeki','Pączek','Kicia','Czarek','Pixel','Dusia','Rysiek','Frodo','Nugget','Koko','Żurek','Leo','Sonia','Chrupka','Kapsel','Mila','Maniek','Trufel','Ziutek','Ciapek','Frytka','Dyzio','Łobuz','Bunia','Precel','Borys','Szczypiorek','Miki','Gofr','Zuzia','Kajtek','Hultaj','Chałka','Mango','Pimpek','Klops','Szarlotka'];
h.removeAttribute('aria-hidden');h.setAttribute('role','group');h.setAttribute('aria-label','Zwierzęta naszych psyjaciół');
const petTooltip=document.createElement('div');petTooltip.className='pet-name-tooltip';petTooltip.id='pet-name-tooltip';petTooltip.setAttribute('role','tooltip');petTooltip.hidden=true;document.body.append(petTooltip);
function hidePetTooltip(){petTooltip.hidden=true;}
function showPetTooltip(dot){petTooltip.textContent=dot.dataset.petName;petTooltip.hidden=false;const rect=dot.getBoundingClientRect(),tip=petTooltip.getBoundingClientRect();petTooltip.style.left=Math.max(8,Math.min(innerWidth-tip.width-8,rect.left+rect.width/2-tip.width/2))+'px';petTooltip.style.top=Math.max(8,rect.top-tip.height-8)+'px';}
window.addEventListener('scroll',hidePetTooltip,{passive:true});document.addEventListener('keydown',e=>{if(e.key==='Escape')hidePetTooltip();});
rs.forEach((v,k)=>{for(let i=0;i<v.count;i++){const A=Math.PI/2+(i -(v.count - 1)/2)*v.step;const d=document.createElement('button');d.type='button';d.className='halo-dot';const pet=window.psyPetPhotos.assign(d,'founders');d.dataset.petName=petNames[pet];d.setAttribute('aria-label',petNames[pet]);d.setAttribute('aria-describedby','pet-name-tooltip');d.addEventListener('pointerenter',()=>showPetTooltip(d));d.addEventListener('focus',()=>showPetTooltip(d));d.addEventListener('pointerleave',hidePetTooltip);d.addEventListener('blur',hidePetTooltip);d.addEventListener('click',()=>showPetTooltip(d));d.style.setProperty('--pet-x',`${pet%8*100/7}%`);d.style.setProperty('--pet-y',`${Math.floor(pet/8)*100/7}%`);d.style.left=`${(0.5 - v.radius * Math.cos(A)) * 100 - D * 50}%`;d.style.top=`${(0.5 - v.radius * Math.sin(A)) * 100 - D * 50}%`;h.append(d);ds.push({d,k,i});}});// Each pet has its own scroll interval, cubic route and easing. All finish at portrait center.
function pathTangent(p,t){const u=1-t;return Math.atan2(3*u*u*(p.c1y-p.y)+6*u*t*(p.c2y-p.c1y)-3*t*t*p.c2y,3*u*u*(p.c1x-p.x)+6*u*t*(p.c2x-p.c1x)-3*t*t*p.c2x);}
const petPaths=ds.map(({d})=>{const side=rand()>.5?1:-1,p={d,side,x:side*(1.1+rand()*1.1),y:(rand()-.5)*1.8,c1x:side*(.2+rand()*1.4),c1y:(rand()-.5)*2.2,c2x:(rand()-.5)*.7,c2y:-.08-rand()*.55,start:rand()*.38,end:.7+rand()*.3,ease:.65+rand()*1.9,mode:Math.floor(rand()*3),turn:(rand()-.5)*50};p.angles=[];for(let i=0;i<=64;i++){let angle=pathTangent(p,i/64);if(i){const previous=p.angles[i-1];while(angle-previous>Math.PI)angle-=2*Math.PI;while(angle-previous<-Math.PI)angle+=2*Math.PI;}p.angles.push(angle);}return p;});let petsScheduled=false;
function movePets(){petsScheduled=false;const section=s.getBoundingClientRect(),portrait=h.getBoundingClientRect(),photo=document.querySelector('.portrait-circle').getBoundingClientRect(),center=photo.top+photo.height/2,travel=section.height/2+innerHeight/2,progress=Math.max(0,Math.min(1,1-(center-innerHeight/2)/travel));petPaths.forEach(p=>{const raw=rm.matches?1:Math.max(0,Math.min(1,(progress-p.start)/(p.end-p.start))),eased=raw*raw*raw*(raw*(raw*6-15)+10),t=p.mode===0?1-Math.pow(1-eased,p.ease):p.mode===1?Math.pow(eased,p.ease):Math.pow(eased,p.ease)/(Math.pow(eased,p.ease)+Math.pow(1-eased,p.ease)),u=1-t,scale=portrait.width,x=(u*u*u*p.x+3*u*u*t*p.c1x+3*u*t*t*p.c2x)*scale,y=(u*u*u*p.y+3*u*u*t*p.c1y+3*u*t*t*p.c2y)*scale,index=Math.min(63,Math.floor(t*64)),angle=(p.angles[index]+(p.angles[index+1]-p.angles[index])*(t*64-index)-p.angles[64])*180/Math.PI;
p.d.style.transform=`translate(${x}px,${y}px) rotate(${angle+p.turn*u}deg) scale(${.55+.45*t})`;p.d.style.opacity=rm.matches?1:Math.min(1,raw*6);});}
function schedulePets(){if(!petsScheduled){petsScheduled=true;requestAnimationFrame(movePets);}}
window.addEventListener('scroll',schedulePets,{passive:true});window.addEventListener('resize',schedulePets);rm.addEventListener('change',schedulePets);movePets();
const header=document.querySelector('.site-header'),headerBackdrop=document.querySelector('.header-backdrop');const headerColorSections=[...document.querySelectorAll('main>section,body>footer')],headerHero=document.querySelector('.hero');let scheduled=false,headerLastY=window.scrollY;function updateHeaderColor(y){const info=header.querySelector('.header-info').getBoundingClientRect(),probe=info.top+Math.min(info.height,44)/2;const section=y<=16?headerHero:headerColorSections.find(section=>{const rect=section.getBoundingClientRect();return rect.top<=probe&&rect.bottom>probe;})||headerHero;const palette=getComputedStyle(section),color=palette.getPropertyValue(section===headerHero?'--ink':'--small-ink').trim()||palette.getPropertyValue('--ink').trim();header.style.setProperty('--nav-ink',color);}function updateHeader(){scheduled=false;const y=Math.max(0,window.scrollY),delta=y-headerLastY;header.classList.toggle('is-compact',y>16);headerBackdrop?.classList.toggle('is-active',y>16);updateHeaderColor(y);if(y<=16){header.classList.remove('is-scrolling-down');headerLastY=y;}else if(Math.abs(delta)>3){header.classList.toggle('is-scrolling-down',delta>0);headerLastY=y;}}window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateHeader);}},{passive:true});window.addEventListener('resize',()=>updateHeaderColor(Math.max(0,window.scrollY)),{passive:true});updateHeader();const animatedImages=document.querySelectorAll('img[data-animated-src]');if(!rm.matches){function loadAnimation(img){const still=img.src;img.addEventListener('error',()=>{img.src=still;},{once:true});img.loading='lazy';img.fetchPriority='low';img.src=img.dataset.animatedSrc;}if('IntersectionObserver'in window){const animations=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){animations.unobserve(entry.target);loadAnimation(entry.target);}});},{threshold:.12});animatedImages.forEach(img=>animations.observe(img));}else animatedImages.forEach(loadAnimation);}
// Both logo rings combine a slow continuous turn with the current scroll offset.
const logoRings=[...document.querySelectorAll('.social-promo-ring,.footer-logo-ring')];
const visibleLogoRings=new Set(logoRings);
let logoRingFrame=0,logoRingLastTime=0,logoRingAngle=0;
function drawLogoRings(){
 const angle=logoRingAngle+window.scrollY*.12;
 logoRings.forEach(ring=>{ring.style.transform=rm.matches?'none':`rotate(${angle}deg)`;});
}
function animateLogoRings(time){
 logoRingFrame=0;
 if(rm.matches||document.hidden||!visibleLogoRings.size){logoRingLastTime=0;return;}
 if(logoRingLastTime)logoRingAngle=(logoRingAngle+Math.min(time-logoRingLastTime,64)*.002)%360;
 logoRingLastTime=time;
 drawLogoRings();
 logoRingFrame=requestAnimationFrame(animateLogoRings);
}
function updateLogoRingMotion(){
 drawLogoRings();
 if(rm.matches||document.hidden||!visibleLogoRings.size){
  cancelAnimationFrame(logoRingFrame);logoRingFrame=0;logoRingLastTime=0;
 }else if(!logoRingFrame){logoRingFrame=requestAnimationFrame(animateLogoRings);}
}
if('IntersectionObserver' in window){
 const logoRingObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{entry.isIntersecting?visibleLogoRings.add(entry.target):visibleLogoRings.delete(entry.target);});
  updateLogoRingMotion();
 });
 logoRings.forEach(ring=>logoRingObserver.observe(ring));
}
window.addEventListener('scroll',updateLogoRingMotion,{passive:true});
document.addEventListener('visibilitychange',updateLogoRingMotion);
rm.addEventListener('change',updateLogoRingMotion);
updateLogoRingMotion();

const portraitBlobs=[...document.querySelectorAll('.portrait-blob')];let blobsScheduled=false;function rotatePortraitBlobs(){blobsScheduled=false;portraitBlobs.forEach((blob,i)=>{const b=blob.parentElement.getBoundingClientRect();const progress=Math.max(-1,Math.min(1,(innerHeight/2-b.top-b.height/2)/(innerHeight/2+b.height/2)));blob.style.setProperty('--blob-angle',`${rm.matches?0:progress*6*(i%2?-1:1)}deg`);});}window.addEventListener('scroll',()=>{if(!blobsScheduled){blobsScheduled=true;requestAnimationFrame(rotatePortraitBlobs);}},{passive:true});window.addEventListener('resize',rotatePortraitBlobs);rm.addEventListener('change',rotatePortraitBlobs);rotatePortraitBlobs();

// Seven-column titles; measured line length controls compact heading leading.
const titles=[...document.querySelectorAll('main h1,main h2')],titleMeasure=document.createElement('canvas').getContext('2d');let titleFrame;
function fitTitles(){cancelAnimationFrame(titleFrame);titleFrame=requestAnimationFrame(()=>{titles.forEach(title=>{const wrap=title.closest('.wrap');if(!wrap)return;const grid=getComputedStyle(wrap),gap=parseFloat(grid.columnGap)||parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap'))||0,column=(wrap.clientWidth-11*gap)/12;title.style.setProperty('--title-width',`${innerWidth>700?7*column+6*gap:wrap.clientWidth}px`);const parts=[...title.querySelectorAll('.heading-roman,em')];(parts.length?parts:[title]).forEach(part=>{if(title.querySelector('.heading-roman')&&title.querySelector('em')){part.style.lineHeight=part.matches('em')?'1.02':'1.12';return}const style=getComputedStyle(part),font=parseFloat(style.fontSize),text=part.textContent.trim();titleMeasure.font=`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;const width=titleMeasure.measureText(style.textTransform==='uppercase'?text.toUpperCase():text).width+Math.max(0,text.length-1)*(parseFloat(style.letterSpacing)||0);part.style.lineHeight=width/font<=12?'1.02':'1.12';});title.style.lineHeight='1.08';});});}
window.addEventListener('resize',fitTitles,{passive:true});document.fonts.ready.then(fitTitles);fitTitles();

// Independent wandering paths across each half; text and photo centre stay clear.
(()=>{
 const section=document.querySelector('.booking-composition'),dots=[...section.querySelectorAll('.booking-pet')];
 let width=0,height=0,top=0,bottom=0,size=0,visible=false,frame=0,elapsed=0,last=0;
 function measure(){
  const box=section.getBoundingClientRect(),title=section.querySelector('h2').getBoundingClientRect(),copy=section.querySelector('.booking-bottom').getBoundingClientRect();
  width=box.width;height=box.height;size=Math.min(80,Math.max(24,width*.06),(copy.top-title.bottom)/3);
  top=title.bottom-box.top+size*.65;bottom=copy.top-box.top-size*.65;
  dots.forEach(dot=>{dot.style.width=size+'px';dot.style.left='0';dot.style.top='0'});render();
 }
 function render(){
  dots.forEach((dot,i)=>{
   const right=dot.classList.contains('solid'),n=right?i-20:i,count=right?12:20;
   const angle=n*Math.PI*2/count+elapsed*(.065+(i*7%13)*.009)*(i%3===0?-1:1);
   let x,y;
   const inset=size*.65,travel=(a,b,t)=>a+(b-a)*(.5+.5*Math.sin(t));
   if(right){
    const t=angle+n*.7;
    x=travel(width/2+inset,width-inset,t);y=travel(inset,height-inset,t*.71+i);
   }else{x=travel(inset,width/2-inset,angle);y=travel(top,bottom,angle*.73+i*1.9);}
   dot.style.transform=`translate(${x-size/2}px,${y-size/2}px) rotate(${Math.sin(angle)*12}deg)`;
  });
 }
 function tick(now){frame=0;if(!visible||rm.matches||document.hidden){last=0;return}if(last)elapsed+=Math.min(.05,(now-last)/1000);last=now;render();frame=requestAnimationFrame(tick)}
 function start(){if(visible&&!rm.matches&&!document.hidden&&!frame)frame=requestAnimationFrame(tick)}
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;start()}).observe(section);
 new ResizeObserver(measure).observe(section);document.fonts.ready.then(measure);
 document.addEventListener('visibilitychange',start);rm.addEventListener('change',()=>{if(rm.matches){cancelAnimationFrame(frame);frame=0;last=0}else start()});
 measure();
})();
