const {chromium}=require('playwright');
(async()=>{const [d,n,mode]=process.argv.slice(2);
const b=await chromium.launch();
if(mode==='reels'){const pg=await b.newPage({viewport:{width:1080,height:1920}});
 for(let i=1;i<=+n;i++){const k=String(i).padStart(2,'0');await pg.goto('file://'+d+`/_r${k}.html`);await pg.screenshot({path:`${d}/_reel_${k}.png`});}
}else{const pg=await b.newPage({viewport:{width:1080,height:1350}});
 for(let i=1;i<=+n;i++){const k=String(i).padStart(2,'0');await pg.goto('file://'+d+`/_s${k}.html`);await pg.screenshot({path:`${d}/slide_${k}.png`});}
 await pg.goto('file://'+d+'/_pdf.html');await pg.pdf({path:`${d}/${mode}`,format:'A4',printBackground:true});}
await b.close();})();
