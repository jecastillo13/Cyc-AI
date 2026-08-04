import { and, asc, eq, gte } from "drizzle-orm";
import { getDb } from "../../../db";
import { activities } from "../../../db/schema";
import { requireApiUser } from "../../server/current-user";

const DAY=86_400_000;
const safeZones=(value:string|null)=>{try{return JSON.parse(value||"[]") as number[]}catch{return []}};
const monday=(date:Date)=>{const copy=new Date(Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate()));copy.setUTCDate(copy.getUTCDate()-((copy.getUTCDay()+6)%7));return copy.toISOString().slice(0,10)};

export async function GET(request:Request){
  try{
    const user=await requireApiUser();
    const requested=Number(new URL(request.url).searchParams.get("days")||90);
    const days=[7,28,90,365].includes(requested)?requested:90;
    const start=new Date(Date.now()-(days-1)*DAY);
    const raw=await getDb().select().from(activities).where(and(eq(activities.userId,user.userId),gte(activities.startedAt,start))).orderBy(asc(activities.startedAt));
    const rows=raw.filter(row=>row.provider==="strava"&&(row.durationSeconds>0||row.distanceMeters>0));
    const weeks=new Map<string,{duration:number;distance:number;tss:number;energy:number;count:number}>();
    const sports=new Map<string,{duration:number;distance:number;count:number}>();
    const hrZones=Array(10).fill(0) as number[],powerZones=Array(10).fill(0) as number[];
    for(const row of rows){
      const key=monday(row.startedAt),week=weeks.get(key)||{duration:0,distance:0,tss:0,energy:0,count:0};
      week.duration+=row.durationSeconds;week.distance+=row.distanceMeters;week.tss+=(row.trainingStressScore||0)/10;week.energy+=row.energyKj||0;week.count++;weeks.set(key,week);
      const sport=sports.get(row.sportType)||{duration:0,distance:0,count:0};sport.duration+=row.durationSeconds;sport.distance+=row.distanceMeters;sport.count++;sports.set(row.sportType,sport);
      safeZones(row.heartRateZones).forEach((value,index)=>hrZones[index]+=(value||0)/10);
      safeZones(row.powerZones).forEach((value,index)=>powerZones[index]+=(value||0)/10);
    }
    const powerCurve=Object.fromEntries(["5","60","300","1200","3600"].map(duration=>[duration,Math.max(0,...raw.map(row=>{try{return (JSON.parse(row.powerCurve||"{}") as Record<string,number>)[duration]||0}catch{return 0}}))]));
    return Response.json({
      period_days:days,source:"Strava",
      totals:{activities:rows.length,duration_hours:+(rows.reduce((sum,row)=>sum+row.durationSeconds,0)/3600).toFixed(1),distance_km:+(rows.reduce((sum,row)=>sum+row.distanceMeters,0)/1000).toFixed(1),tss:+rows.reduce((sum,row)=>sum+(row.trainingStressScore||0)/10,0).toFixed(0),energy_kj:rows.reduce((sum,row)=>sum+(row.energyKj||0),0)},
      peaks:{heart_rate:Math.max(0,...rows.map(row=>row.maxHeartRate||0)),power:Math.max(0,...rows.map(row=>row.maxPower||0)),longest_minutes:Math.round(Math.max(0,...rows.map(row=>row.durationSeconds))/60),longest_km:+(Math.max(0,...rows.map(row=>row.distanceMeters))/1000).toFixed(1)},
      weekly:Array.from(weeks,([week,value])=>({week,duration_hours:+(value.duration/3600).toFixed(1),distance_km:+(value.distance/1000).toFixed(1),tss:Math.round(value.tss),energy_kj:value.energy,activities:value.count})),
      sports:Array.from(sports,([sport,value])=>({sport,duration_hours:+(value.duration/3600).toFixed(1),distance_km:+(value.distance/1000).toFixed(1),activities:value.count})),
      zones:{heart_rate:hrZones.map(Math.round),power:powerZones.map(Math.round)},
      power_curve:powerCurve,
    });
  }catch(error){if(error instanceof Response)return error;console.error("Analytics failed",error);return Response.json({error:"No fue posible calcular la analítica."},{status:500})}
}
