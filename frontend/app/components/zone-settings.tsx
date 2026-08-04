"use client";
import { useEffect,useState } from "react";
type Key="ftp"|"threshold_hr"|"max_hr"|"resting_hr";
type Draft=Record<Key,string>;
const defaults:Draft={ftp:"190",threshold_hr:"165",max_hr:"168",resting_hr:"55"};
const help:Record<Key,string>={
 ftp:"Tu potencia funcional: los vatios que aproximadamente puedes sostener durante una hora. Usa el resultado de una prueba FTP; si no lo conoces, deja 190 temporalmente.",
 threshold_hr:"Pulso medio que puedes sostener cerca de una hora. Puede obtenerse de una prueba de umbral o de los últimos 20 minutos de un esfuerzo fuerte y estable.",
 max_hr:"La frecuencia cardíaca más alta registrada de forma fiable en entrenamiento o prueba. Debe ser igual o mayor que tu pulso umbral.",
 resting_hr:"Pulso en reposo medido al despertar, antes de levantarte. Conviene usar el promedio de varios días.",
};
export function ZoneSettings(){
 const [values,setValues]=useState<Draft>(defaults),[message,setMessage]=useState(""),[saving,setSaving]=useState(false);
 useEffect(()=>{fetch("/api/settings/zones").then(response=>response.ok?response.json():null).then(body=>{if(body)setValues({ftp:String(body.ftp||190),threshold_hr:String(body.threshold_hr||165),max_hr:String(body.max_hr||168),resting_hr:String(body.resting_hr||55)})}).catch(()=>null)},[]);
 const numeric={ftp:Number(values.ftp)||0,threshold_hr:Number(values.threshold_hr)||0,max_hr:Number(values.max_hr)||0,resting_hr:Number(values.resting_hr)||0};
 const power=[.55,.75,.9,1.05,1.2].map(value=>Math.round(numeric.ftp*value)),heart=[.68,.83,.94,1.05].map(value=>Math.round(numeric.threshold_hr*value));
 const save=async()=>{setSaving(true);setMessage("");try{const response=await fetch("/api/settings/zones",{method:"PUT",headers:{"content-type":"application/json"},body:JSON.stringify(numeric)});const body=await response.json();if(!response.ok)throw new Error(body.error);setMessage("Zonas guardadas. Pulsa Sincronizar para recalcular tus actividades.")}catch(error){setMessage(error instanceof Error?error.message:"No fue posible guardar.")}finally{setSaving(false)}};
 const field=(key:Key,label:string,unit:string,placeholder:string)=><label><span className="field-title">{label}<Help text={help[key]}/></span><span className="field-input"><input type="text" inputMode="numeric" pattern="[0-9]*" placeholder={placeholder} value={values[key]} onChange={event=>setValues(current=>({...current,[key]:event.target.value.replace(/\D/g,"")}))}/>{unit}</span></label>;
 return <section className="panel zone-settings" id="zonas"><div className="panel-head"><div><p className="eyebrow">Configuración personal</p><h2>Mis zonas</h2><p className="section-copy">Introduce tus valores fisiológicos. Pulsa los signos ? si no sabes qué significa un campo.</p></div><button className="primary" disabled={saving} onClick={()=>void save()}>{saving?"Guardando…":"Guardar zonas"}</button></div><div className="thresholds">{field("ftp","FTP / potencia umbral","W","Ej. 190")}{field("threshold_hr","Pulso umbral","bpm","Ej. 165")}{field("max_hr","Pulso máximo","bpm","Ej. 185")}{field("resting_hr","Pulso en reposo","bpm","Ej. 55")}</div><div className="zone-preview"><ZoneList title="Potencia" limits={power} unit="W"/><ZoneList title="Frecuencia cardíaca" limits={heart} unit="bpm"/></div>{message&&<p className="zone-message">{message}</p>}</section>
}
function Help({text}:{text:string}){return <span className="help"><button type="button" aria-label="Mostrar ayuda">?</button><span className="help-tip" role="tooltip">{text}</span></span>}
function ZoneList({title,limits,unit}:{title:string;limits:number[];unit:string}){return <article><h3>{title}</h3>{[0,...limits].map((start,index)=><div key={index}><strong>Z{index+1}</strong><span>{index===0?0:start+1} – {index<limits.length?limits[index]:"∞"} {unit}</span></div>)}</article>}
