(async()=>{const wait=ms=>new Promise(r=>setTimeout(r,ms)), out=[]; const ae=()=>document.activeElement.tagName+(document.activeElement.dataset.fk?'['+document.activeElement.dataset.fk+']':'');
location.hash='#/vi/coroutines/a1/1'; await wait(300);
let b=document.querySelector('.side-body [data-fk=nav-next]'); b.focus(); b.click(); out.push('nav-next -> '+ae());
b=document.querySelector('.side-body [data-fk=nav-next]'); b.click(); b.click(); out.push('nav-next x2 -> '+ae());
let t=[...document.querySelectorAll('.side .tab')][1]; t.focus(); t.click(); out.push('side tab click -> '+ae());
t=document.querySelector('.side .tab[aria-selected=true]'); t.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true})); out.push('tab ArrowLeft -> '+ae());
let r=document.querySelector('[data-fk=row-1]'); r.focus(); r.click(); out.push('log row -> '+ae());
let s=document.querySelector('.sandbox [data-fk=sb-block]'); s.focus(); s.click(); out.push('sandbox toggle -> '+ae());
let l=document.querySelector('[data-fk=lang-en]'); l.focus(); l.click(); out.push('lang switch -> '+ae());
l=document.querySelector('[data-fk=theme]'); l.focus(); l.click(); out.push('theme -> '+ae());
l=document.querySelector('[data-fk=motion]'); l.focus(); l.click(); out.push('motion -> '+ae());
l=document.querySelector('[data-fk=sans]'); l.focus(); l.click(); out.push('sans -> '+ae());
out.push('aria-live="'+document.getElementById('ade-live').textContent+'"');
location.hash='#/en/'; await wait(300); out.push('home title="'+document.title+'"');
return out.join('\n');})()
