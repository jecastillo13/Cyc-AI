import { requireApiUser } from "../../../../server/current-user";
import { signState } from "../../../../server/secrets";
import { stravaConfig } from "../../../../server/strava-config";

export async function GET(request:Request){try{const user=await requireApiUser();const config=stravaConfig();if(!config.clientSecret)return Response.json({error:"Strava is not configured"},{status:503});const callback=new URL("/api/oauth/strava/callback",request.url).toString();const url=new URL("https://www.strava.com/oauth/authorize");url.search=new URLSearchParams({client_id:config.clientId,redirect_uri:callback,response_type:"code",approval_prompt:"auto",scope:"read,activity:read_all",state:await signState(user.userId)}).toString();return Response.redirect(url)}catch(error){if(error instanceof Response)return error;return Response.json({error:"Unable to start Strava connection"},{status:500})}}
