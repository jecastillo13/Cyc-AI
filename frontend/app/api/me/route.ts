import { requireApiUser } from "../../server/current-user";

export async function GET(){try{const user=await requireApiUser();return Response.json({user})}catch(error){if(error instanceof Response)return error;return Response.json({error:"Unable to load account"},{status:500})}}
