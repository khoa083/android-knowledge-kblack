(async()=>{const routes=['#/vi/','#/en/','#/vi/live','#/vi/misconceptions','#/en/glossary','#/vi/sources','#/vi/about','#/en/search?q=flow','#/vi/search?q=coroutine','#/vi/nonexistent'];
// sinh route từ registry: trang track, mọi chương (bước 1), preset, mục glossary đầu tiên của track
ADE.tracks.forEach((t,i)=>{const L=i%2?'en':'vi';routes.push('#/'+L+'/'+t.id);t.chapters.forEach((c,j)=>routes.push('#/'+(j%2?'en':'vi')+'/'+t.id+'/'+c.id+'/'+(j%3)));t.presets.forEach(p=>routes.push('#/'+L+'/live?preset='+p.id+'&step=2'));});
ADE.glossaryIds.slice(0,3).forEach(g=>routes.push('#/vi/glossary/'+g));
ADE.sourceList.slice(0,3).forEach(s=>routes.push('#/en/sources/'+s.id));
const out=[];let bad=0;for(const r of routes){location.hash=r;await new Promise(x=>setTimeout(x,220));const d=document.documentElement;const o=d.scrollWidth>d.clientWidth+1;const leak=(document.getElementById('main').innerText.match(/\btrack\.[a-z0-9]+\.[\w.]+|\bapp\.[a-z]+\.[\w.]+/)||[''])[0];if(o||leak)bad++;out.push(r+' => '+(document.querySelector('#main h1, #main .page-h h1')?.textContent||'?').slice(0,40)+' | lang='+d.lang+' | overflowX='+(o?'YES '+d.scrollWidth+'>'+d.clientWidth:'no')+(leak?' | LEAK '+leak:''));}
return routes.length+' routes, problems='+bad+'\n'+out.join('\n');})()
