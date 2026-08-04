"use client";

import { useEffect, useMemo, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Status = { atl:number; ctl:number; tsb:number; fatigue_score:number; recovery_score:number; fitness_score:number; readiness:string; injury_risk:string };
type RecentActivity = { name:string;sport_type:string;date:string;duration_minutes:number;distance_km:number;elevation_meters:number };
type Dashboard = { athlete:{name:string}; history:{workouts_last_7_days:number;distance_last_7_days:number;duration_hours_last_7_days?:number;elevation_last_7_days?:number;load_trend_percent:number}; training_status:Status; charts:{daily_load:{date:string;load:number}[]};recent_activities?:RecentActivity[] };
type Plan = { weeks:{week:number;target_load:number;sessions:{day:string;session:string;target_load:number}[]}[] };
type Provider = { id:string;name:string;status:string;description:string;connection:{displayName:string|null;lastSyncAt:string|null}|null };

async function fetchDashboard() {
  const response = await fetch("/api/dashboard", { cache: "no-store" });
  if (!response.ok) throw new Error("No fue posible actualizar el panel.");
  return response.json() as Promise<Dashboard>;
}

const fallback: Dashboard = {
  athlete:{name:"Ciclista"},
  history:{workouts_last_7_days:8,distance_last_7_days:156.3,load_trend_percent:-7.8},
  training_status:{atl:50.4,ctl:61.2,tsb:10.8,fatigue_score:41.2,recovery_score:69.6,fitness_score:61.2,readiness:"moderate",injury_risk:"low"},
  charts:{daily_load:Array.from({length:28},(_,i)=>({date:`Día ${i+1}`,load:[0,42,71,0,35,118,24][i%7]}))},
};

const labels: Record<string,string> = { high:"Alta", moderate:"Moderada", low:"Baja" };

export default function Home() {
  const [data,setData]=useState<Dashboard>(fallback);
  const [connected,setConnected]=useState(false);
  const [message,setMessage]=useState("");
  const [plan,setPlan]=useState<Plan|null>(null);
  const [providers,setProviders]=useState<Provider[]>([]);
  const [syncing,setSyncing]=useState("");
  const [aiAnalysis,setAiAnalysis]=useState("");
  const [askingAi,setAskingAi]=useState(false);

  useEffect(()=>{
    fetchDashboard()
      .then(payload=>{setData(payload);setConnected(true)})
      .catch(()=>setConnected(false));
    fetch("/api/me").then(response=>{if(response.status===401){window.location.href="/login";return null}return response.ok?response.json():null}).then(payload=>{if(payload?.user?.displayName)setData(current=>({...current,athlete:{name:payload.user.displayName}}))}).catch(()=>null);
    fetch("/api/integrations").then(response=>response.ok?response.json():null).then(payload=>{if(payload?.providers)setProviders(payload.providers)}).catch(()=>null);
    if(new URLSearchParams(window.location.search).get("connected")==="strava"){
      fetch("/api/integrations/strava/sync",{method:"POST"})
        .then(async response=>{const payload=await response.json();if(!response.ok)throw new Error(payload.error);setData(await fetchDashboard());setConnected(true);setMessage(`${payload.synced} actividades sincronizadas automáticamente desde Strava.`)})
        .catch(error=>setMessage(error instanceof Error?error.message:"Strava quedó conectado, pero no fue posible sincronizar ahora."))
        .finally(()=>{setSyncing("");window.history.replaceState({},"",window.location.pathname)});
    }
  },[]);
  const generate=async()=>{try{const r=await fetch(`${API}/plan/generate?weeks=1&goal=base`,{method:"POST"});if(!r.ok)throw new Error();setPlan(await r.json())}catch{setMessage("Inicia la API para generar un plan personalizado.")}};
  const syncStrava=async()=>{setSyncing("strava");try{const response=await fetch("/api/integrations/strava/sync",{method:"POST"});const payload=await response.json();if(!response.ok)throw new Error(payload.error);setData(await fetchDashboard());setConnected(true);setMessage(`${payload.synced} actividades sincronizadas desde Strava.`)}catch(error){setMessage(error instanceof Error?error.message:"No fue posible sincronizar Strava")}finally{setSyncing("")}};
  const disconnect=async(provider:string)=>{if(!confirm(`¿Desconectar ${provider}?`))return;const response=await fetch(`/api/integrations?provider=${encodeURIComponent(provider)}`,{method:"DELETE"});if(response.ok)setProviders(current=>current.map(item=>item.id===provider?{...item,connection:null}:item));else setMessage("No fue posible desconectar la aplicación.")};
  const askCoach=async()=>{setAskingAi(true);try{const response=await fetch("/api/coach",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({history:data.history,training_status:data.training_status,recent_activities:data.recent_activities})});const payload=await response.json();if(!response.ok)throw new Error(payload.error);setAiAnalysis(payload.analysis)}catch(error){setAiAnalysis(error instanceof Error?error.message:"No fue posible consultar el Coach IA.")}finally{setAskingAi(false)}};
  const chart=useMemo(()=>data.charts.daily_load.slice(-28),[data]);
  const max=Math.max(...chart.map(x=>x.load),1); const s=data.training_status;

  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="#inicio"><span className="brand-mark">C</span><span>Cyc—AI</span></a>
      <nav><a className="active" href="#inicio">Resumen</a><a href="#carga">Carga</a><a href="#coach">Coach</a><a href="#plan">Plan semanal</a><a href="#conexiones">Conexiones</a></nav>
      <div className="athlete"><span className="avatar">{data.athlete.name.charAt(0)}</span><div><strong>{data.athlete.name}</strong><small>{connected?"Datos sincronizados":"Modo demostración"}</small></div></div>
    </aside>

    <main id="inicio">
      <header><div><p className="eyebrow">Estado de hoy</p><h1>Buen ritmo, {data.athlete.name.split(" ")[0]}.</h1><p className="sub">Tu carga está controlada y tienes margen para seguir construyendo.</p></div><a className="primary connect-cta" href="#conexiones">Conectar aplicación</a></header>
      {message&&<div className="notice" role="status">{message}</div>}

      <section className="metrics" aria-label="Indicadores fisiológicos">
        <Metric label="Disponibilidad" value={labels[s.readiness]||s.readiness} note={`Qué tan preparado estás hoy · riesgo ${labels[s.injury_risk]?.toLowerCase()||s.injury_risk}`} accent />
        <Metric label="Fitness (CTL)" value={s.fitness_score.toFixed(0)} note="Promedio ponderado de tu carga de las últimas 6 semanas" />
        <Metric label="Fatiga (ATL)" value={s.fatigue_score.toFixed(0)} note="Impacto de la carga reciente; alto significa más cansancio" />
        <Metric label="Recuperación" value={`${s.recovery_score.toFixed(0)}%`} note="Estimación de frescura según fitness, fatiga y balance" />
      </section>

      <section className="grid" id="carga">
        <article className="panel chart-panel"><div className="panel-head"><div><p className="eyebrow">Últimos 28 días</p><h2>Carga de entrenamiento</h2></div><div className="legend"><span>ATL {s.atl.toFixed(1)}</span><span>CTL {s.ctl.toFixed(1)}</span></div></div>
          <div className="bars" aria-label="Gráfica diaria de carga">{chart.map((x,i)=><div key={`${x.date}-${i}`} className="bar-wrap" title={`${x.date}: ${x.load}`}><span className="bar" style={{height:`${Math.max(3,(x.load/max)*100)}%`}}/></div>)}</div>
          <div className="chart-foot"><span>Hace 28 días</span><span>Hoy</span></div>
        </article>
        <article className="panel week"><p className="eyebrow">Últimos 7 días</p><div className="week-number">{data.history.workouts_last_7_days}</div><p>actividades · {data.history.distance_last_7_days.toFixed(0)} km</p><div className="week-details"><span>{(data.history.duration_hours_last_7_days||0).toFixed(1)} h entrenadas</span><span>{data.history.elevation_last_7_days||0} m ascendidos</span></div><div className={`trend ${data.history.load_trend_percent<=0?"good":""}`}>{data.history.load_trend_percent>0?"↑":"↓"} {Math.abs(data.history.load_trend_percent).toFixed(1)}% frente a los 7 días anteriores</div></article>
      </section>

      <section className="grid lower" id="coach">
        <article className="panel coach"><div className="coach-icon">IA</div><div><p className="eyebrow">Coach IA · Cloudflare Workers AI</p><h2>{s.recovery_score>=70?"Buen momento para calidad":"Mantén una carga estable"}</h2><p>{aiAnalysis||"Pide un análisis personalizado de tu carga, recuperación y últimas actividades. La IA usará únicamente los datos visibles de este panel."}</p><button onClick={()=>void askCoach()} disabled={askingAi}>{askingAi?"Analizando tus datos…":"Analizar mis datos con IA →"}</button></div></article>
        <article className="panel balance"><p className="eyebrow">Balance de forma</p><div className="balance-value">{s.tsb>0?"+":""}{s.tsb.toFixed(1)}</div><h3>TSB favorable</h3><p>Valores positivos suelen indicar mayor frescura.</p></article>
      </section>
      <section className="panel recent"><div className="panel-head"><div><p className="eyebrow">Detalle sincronizado</p><h2>Actividades recientes</h2></div><small>Datos obtenidos de Strava</small></div><div className="activity-list">{data.recent_activities?.length?data.recent_activities.map((activity,index)=><article className="activity-row" key={`${activity.date}-${index}`}><div><strong>{activity.name}</strong><small>{new Date(activity.date).toLocaleDateString("es-CO",{day:"numeric",month:"short"})} · {activity.sport_type}</small></div><span>{activity.distance_km.toFixed(1)} km</span><span>{activity.duration_minutes} min</span><span>{activity.elevation_meters} m ↑</span></article>):<p className="empty">Sincroniza Strava para ver aquí tus entrenamientos.</p>}</div></section>

      <section className="panel plan" id="plan"><div className="panel-head"><div><p className="eyebrow">Siguiente paso</p><h2>Plan semanal adaptable</h2></div><button className="primary" onClick={()=>void generate()}>Generar mi semana</button></div>
        {plan?<div className="sessions">{plan.weeks[0].sessions.map(x=><div className="session" key={x.day}><strong>{x.day.slice(0,3)}</strong><span>{x.session}</span><em>{x.target_load||"—"}</em></div>)}</div>:<p className="empty">Genera una semana según tu recuperación, riesgo y carga actuales.</p>}
      </section>
      <section className="panel integrations" id="conexiones"><div className="panel-head"><div><p className="eyebrow">Tus datos, bajo tu control</p><h2>Aplicaciones conectadas</h2><p className="section-copy">Conecta tu cuenta una sola vez. Cyc-AI obtiene tus actividades desde el servicio autorizado; no necesitas subir archivos.</p></div><a className="signout" href="/api/auth/logout">Cerrar sesión</a></div>
        <div className="provider-grid">{(providers.length?providers:[{id:"strava",name:"Strava",status:"available",description:"Ciclismo, carrera y actividades GPS",connection:null},{id:"garmin",name:"Garmin Connect",status:"planned",description:"Actividad, sueño, HRV y recuperación",connection:null},{id:"trainingpeaks",name:"TrainingPeaks",status:"planned",description:"Planes, TSS y entrenamientos",connection:null},{id:"intervals",name:"Intervals.icu",status:"planned",description:"Carga, fitness y calendario",connection:null}]).map(provider=><article className="provider" key={provider.id}><div className={`provider-mark ${provider.id}`}>{provider.name.slice(0,2).toUpperCase()}</div><div className="provider-body"><h3>{provider.name}</h3><p>{provider.description}</p>{provider.connection&&<small>Conectado como {provider.connection.displayName||"atleta"}</small>}</div>{provider.connection?<div className="connection-actions"><button className="secondary" onClick={()=>provider.id==="strava"&&void syncStrava()}>{syncing===provider.id?"Sincronizando…":"Sincronizar"}</button><button className="disconnect" onClick={()=>void disconnect(provider.id)}>Quitar</button></div>:provider.status==="available"?<a className="secondary" href="/api/oauth/strava/start">Conectar</a>:<span className="soon">{provider.status==="configuration_required"?"Falta configurar":"Próximamente"}</span>}</article>)}</div>
      </section>
      <footer>Cyc—AI interpreta datos deportivos; no sustituye orientación médica o profesional.</footer>
    </main>
  </div>
}

function Metric({label,value,note,accent=false}:{label:string;value:string;note:string;accent?:boolean}){return <article className={`metric ${accent?"accent":""}`}><p>{label}</p><strong>{value}</strong><small>{note}</small></article>}
