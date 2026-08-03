from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard/ui", response_class=HTMLResponse)
def dashboard_ui():
    return """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Cyc-AI Dashboard</title><style>
body{font-family:system-ui;background:#0b1220;color:#e5e7eb;margin:0;padding:24px}main{max-width:1100px;margin:auto}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}.card{background:#172033;padding:18px;border-radius:14px}
.value{font-size:2rem;font-weight:700;color:#34d399}svg{width:100%;height:260px;background:#172033;border-radius:14px;margin-top:16px}
a{color:#60a5fa}.muted{color:#94a3b8}</style></head><body><main>
<h1>Cyc-AI</h1><p class="muted">Estado fisiológico y carga de los últimos 90 días.</p><div id="cards" class="cards"></div>
<svg id="chart" viewBox="0 0 1000 260" preserveAspectRatio="none"></svg><p><a href="/docs">Abrir API y Swagger</a></p>
</main><script>
fetch('/dashboard').then(r=>r.json()).then(d=>{const s=d.training_status;const values=[['ATL',s.atl],['CTL',s.ctl],['TSB',s.tsb],['Fatiga',s.fatigue_score],['Recuperación',s.recovery_score],['Fitness',s.fitness_score]];
document.querySelector('#cards').innerHTML=values.map(x=>`<div class="card"><div class="muted">${x[0]}</div><div class="value">${Number(x[1]).toFixed(1)}</div></div>`).join('');
const p=d.charts.daily_load,max=Math.max(...p.map(x=>x.load),1),step=1000/Math.max(p.length-1,1);const points=p.map((x,i)=>`${i*step},${245-(x.load/max)*220}`).join(' ');
document.querySelector('#chart').innerHTML=`<polyline fill="none" stroke="#34d399" stroke-width="4" points="${points}"/>`;});
</script></body></html>"""
