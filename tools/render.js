const {chromium}=require('playwright');
(async()=>{const [d,n,pdf]=process.argv.slice(2);
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=1;i<=+n;i++){const k=String(i).padStart(2,'0');await pg.goto('file://'+d+`/_s${k}.html`);await pg.screenshot({path:`${d}/slide_${k}.png`});}
await pg.goto('file://'+d+'/_pdf.html');await pg.pdf({path:`${d}/${pdf}`,format:'A4',printBackground:true});
await b.close();})();
