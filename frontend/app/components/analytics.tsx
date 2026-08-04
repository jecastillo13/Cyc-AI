"use client";
import { useEffect,useState } from "react";
type Analytics={source:string;totals:{activities:number;duration_hours:number;distance_km:number;tss:number};peaks:{heart_rate:number;power:number};weekly:{week:string;tss:number}[];sports:{sport:string;duration_hours:number;distance_km:number;activities:number}[];zones:{heart_rate:number[];power:number[]};power_curve:Record<string,number>};
const curveLabels:Record<string,string>={"5":"5 s","60":"1 min","300":"5 min","1200":"20 min","3600":"60 min"};
export function AnalyticsPanel(){
 const [days,setDays]=useState(90),[data,setData]=useState<Analytics|null>(null),[error,setError]=useState("");
 useEffect(()=>{fetch(`/api/analytics?days=${days}`,{cache:"no-store"}).then(async response=>{const body=await response.json();if(!response.ok)throw new Error(body.error);setData(body)}).catch(reason=>setError(reason instanceof Error?reason.message:"No fue posible cargar la analítica."))},[days]);
 const changeDays=(value:number)=>{setDays(value);setData(null);setError("")};
 if(error)return <section className="panel analytics" id="analitica"><p className="empty">{error}</p></section>;
 return <section className="panel analytics" id="analitica">
  <div className="panel-head"><div><p className="eyebrow">Rendimiento en profundidad</p><h2>Analítica</h2><p className="section-copy">Carga, volumen, zonas y curvas. Fuente: {data?.source||"—"}.</p></div><select value={days} onChange={event=>changeDays(Number(event.target.value))}><option value="7">7 días</option><option value="28">4 semanas</option><option value="90">3 meses</option><option value="365">1 año</option></select></div>
  {!data?<p className="empty">Calculando…</p>:<AnalyticsContent data={data}/>}
 </section>
}
function AnalyticsContent({data}:{data:Analytics}){const maxTss=Math.max(1,...data.weekly.map(item=>item.tss));return <>
 <div className="analytics-kpis"><Kpi label="Actividades" value={String(data.totals.activities)}/><Kpi label="Duración" value={`${data.totals.duration_hours} h`}/><Kpi label="Distancia" value={`${data.totals.distance_km} km`}/><Kpi label="Carga estimada" value={`${data.totals.tss} pts`}/><Kpi label="Potencia máxima" value={`${data.peaks.power||"—"} W`}/><Kpi label="Pulso máximo" value={`${data.peaks.heart_rate||"—"} bpm`}/></div>
 <div className="analytics-grid"><article><h3>Carga semanal Cyc-AI</h3><div className="weekly-bars">{data.weekly.map(item=><div key={item.week}><span style={{height:`${Math.max(3,item.tss/maxTss*100)}%`}}/><small>{item.week.slice(5)}<br/>{item.tss} pts</small></div>)}</div></article><article><h3>Resumen por deporte</h3>{data.sports.map(item=><div className="sport-row" key={item.sport}><strong>{item.sport}</strong><span>{item.activities} sesiones</span><span>{item.duration_hours} h</span><span>{item.distance_km} km</span></div>)}</article></div>
 <div className="analytics-grid"><ZoneChart title="Tiempo en zonas de pulso" values={data.zones.heart_rate}/><ZoneChart title="Tiempo en zonas de potencia" values={data.zones.power}/></div>
 <article className="power-curve"><h3>Curva de potencia desde Strava</h3><div>{Object.entries(data.power_curve).map(([duration,power])=><span key={duration}><small>{curveLabels[duration]}</small><strong>{power?`${power} W`:"Sin datos"}</strong></span>)}</div></article>
 <p className="analytics-note">La carga Cyc-AI se calcula con potencia normalizada, duración, factor de intensidad y tu FTP. Es una estimación propia, no el TSS oficial de TrainingPeaks. Las zonas usan los valores que guardaste en tu perfil.</p>
 </>}
function Kpi({label,value}:{label:string;value:string}){return <article><small>{label}</small><strong>{value}</strong></article>}
function ZoneChart({title,values}:{title:string;values:number[]}){const shown=values.slice(0,7),max=Math.max(1,...shown);return <article><h3>{title}</h3><div className="zone-bars">{shown.map((value,index)=><div key={index}><span style={{height:`${Math.max(2,value/max*100)}%`}}/><small>Z{index+1}<br/>{value}m</small></div>)}</div></article>}
