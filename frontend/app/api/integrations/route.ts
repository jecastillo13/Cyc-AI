import { and, eq } from "drizzle-orm";
import { getDb } from "../../../db";
import { connections } from "../../../db/schema";
import { requireApiUser } from "../../server/current-user";
import { decryptSecret } from "../../server/secrets";
import { stravaConfig } from "../../server/strava-config";

const providers=[
  {id:"strava",name:"Strava",status:"available",description:"Ciclismo, carrera y actividades GPS"},
  {id:"garmin",name:"Garmin Connect",status:"planned",description:"Actividad, sueño, HRV y recuperación"},
  {id:"intervals",name:"Intervals.icu",status:"planned",description:"Carga, fitness y calendario"},
  {id:"fitbit",name:"Fitbit",status:"planned",description:"Actividad, sueño y estado físico"},
];

export async function GET(){try{const user=await requireApiUser();const rows=await getDb().select({provider:connections.provider,displayName:connections.displayName,lastSyncAt:connections.lastSyncAt}).from(connections).where(eq(connections.userId,user.userId));return Response.json({providers:providers.map(provider=>({...provider,status:provider.id==="strava"&&!stravaConfig().clientSecret?"configuration_required":provider.status,connection:rows.find(row=>row.provider===provider.id)||null}))})}catch(error){if(error instanceof Response)return error;return Response.json({error:"Unable to load integrations"},{status:500})}}

export async function DELETE(request:Request){try{const user=await requireApiUser();const provider=new URL(request.url).searchParams.get("provider");if(!provider)return Response.json({error:"provider is required"},{status:400});const db=getDb();const [connection]=await db.select().from(connections).where(and(eq(connections.userId,user.userId),eq(connections.provider,provider))).limit(1);if(connection&&provider==="strava"){const config=stravaConfig();const basic=btoa(`${config.clientId}:${config.clientSecret}`);await fetch("https://www.strava.com/oauth/revoke",{method:"POST",headers:{authorization:`Basic ${basic}`,"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({token:await decryptSecret(connection.accessTokenEncrypted),token_type_hint:"access_token"})})}await db.delete(connections).where(and(eq(connections.userId,user.userId),eq(connections.provider,provider)));return new Response(null,{status:204})}catch(error){if(error instanceof Response)return error;return Response.json({error:"Unable to disconnect"},{status:500})}}
