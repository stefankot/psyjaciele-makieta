(()=>{
 if(!window.gsap||!window.ScrollTrigger)return;
 gsap.registerPlugin(ScrollTrigger);
 const mm=gsap.matchMedia();
 mm.add({all:'(min-width:0px)',desktop:'(min-width:701px)',reduce:'(prefers-reduced-motion:reduce)'},ctx=>{
  const root=document.documentElement;
  if(ctx.conditions.reduce){root.dataset.motion='reduced';root.dataset.motionTriggers='0';return;}
  const amplitude=ctx.conditions.desktop?1:.5;
  root.dataset.motion='gsap';
  const enter=(trigger,run)=>ScrollTrigger.create({trigger,start:'top 90%',once:true,onEnter:run});
  // An excited pair of pets leans into the scroll, then lands back on the grid.
  gsap.timeline({scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1.1}})
   .to('.hero-art img',{rotation:-7*amplitude,y:-28*amplitude,scale:1.05,transformOrigin:'70% 75%',duration:.35,ease:'sine.inOut'})
   .to('.hero-art img',{rotation:8*amplitude,y:12*amplitude,scale:1.09,duration:.35,ease:'sine.inOut'})
   .to('.hero-art img',{rotation:0,y:0,scale:1,duration:.3,ease:'back.out(2)'});
  gsap.to('.hero-title',{y:-34*amplitude,rotation:-1.5*amplitude,transformOrigin:'left bottom',ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1}});
  document.querySelectorAll('.heading>h2,.section-heading h2,.booking-copy h2,.contact-copy h2,.about-copy h2,.arrival-copy h2').forEach((title,i)=>{
   enter(title,()=>gsap.fromTo(title,{y:55*amplitude,rotation:(i%2?4:-4)*amplitude,opacity:.3},{y:0,rotation:0,opacity:1,duration:1.3,ease:'elastic.out(1,.65)',clearProps:'transform,opacity'}));
  });
  document.querySelectorAll('.drawing,.booking-art,.contact-art,.about-illustration,.clinic-illustration').forEach((figure,i)=>{
   const art=figure.querySelector('.art');
   gsap.timeline({scrollTrigger:{trigger:figure,start:'top 95%',end:'bottom 20%',scrub:1.15}})
    .fromTo(art,{y:70*amplitude,rotation:(i%2?-9:9)*amplitude,scale:1},{y:-18*amplitude,rotation:(i%2?4:-4)*amplitude,scale:1.03,duration:.6,ease:'back.out(2.5)'})
    .to(art,{y:0,rotation:0,scale:1,duration:.4,ease:'elastic.out(1,.6)'});
  });
  // Whole portrait moves together so the halo keeps its equal spacing.
  gsap.timeline({scrollTrigger:{trigger:'.about-photo',start:'top 90%',end:'bottom 20%',scrub:1.2}})
   .fromTo('.about-photo',{rotation:-3*amplitude,y:28*amplitude},{rotation:3*amplitude,y:-12*amplitude,duration:.5,ease:'sine.inOut'})
   .to('.about-photo',{rotation:0,y:0,duration:.5,ease:'back.out(2)'});
  document.querySelectorAll('.bento .tile').forEach((tile,i)=>{
   enter(tile,()=>gsap.fromTo(tile,{y:90*amplitude,rotation:(i%2?8:-8)*amplitude,scale:.86},{y:0,rotation:0,scale:1,delay:(i%2)*.09,duration:1.2,ease:'elastic.out(1,.65)',clearProps:'transform'}));
  });
  document.querySelectorAll('.person figure,.quote,.clinic-gallery .placeholder').forEach((item,i)=>{
   enter(item,()=>gsap.fromTo(item,{y:45*amplitude,rotation:(i%2?3:-3)*amplitude,opacity:.4},{y:0,rotation:0,opacity:1,duration:1.05,ease:'back.out(1.8)',clearProps:'transform,opacity'}));
  });
  document.querySelectorAll('.travel-art,.urgent-art').forEach(item=>{
   enter(item,()=>gsap.fromTo(item,{y:24,opacity:.5},{y:0,opacity:1,duration:.8,ease:'power2.out',clearProps:'transform,opacity'}));
  });
  root.dataset.motionTriggers=String(ScrollTrigger.getAll().length);
 });
 document.fonts.ready.then(()=>ScrollTrigger.refresh());
 window.addEventListener('load',()=>ScrollTrigger.refresh(),{once:true});
})();
