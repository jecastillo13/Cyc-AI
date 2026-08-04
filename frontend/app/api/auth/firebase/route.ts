import { eq } from "drizzle-orm";
import { getDb } from "../../../../db";
import { users } from "../../../../db/schema";
import { createSession } from "../../../server/current-user";

const FIREBASE_API_KEY="AIzaSyBiy-98OybR5n6GjA-cOjmICjU2kAMtgSg";
type FirebaseAccount={localId:string;email:string;emailVerified:boolean;displayName?:string};

export async function POST(request:Request){
  const {idToken}=await request.json() as {idToken?:string};
  if(!idToken)return Response.json({error:"Falta la credencial de Firebase."},{status:400});
  const response=await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${FIREBASE_API_KEY}`,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({idToken})});
  if(!response.ok)return Response.json({error:"La sesión de Google no es válida."},{status:401});
  const payload=await response.json() as {users?:FirebaseAccount[]};const account=payload.users?.[0];
  if(!account?.email||!account.emailVerified)return Response.json({error:"Debes verificar tu correo antes de entrar."},{status:403});
  const db=getDb();const email=account.email.toLowerCase();const [existing]=await db.select({id:users.id}).from(users).where(eq(users.email,email)).limit(1);const userId=existing?.id??account.localId;const now=new Date();
  if(existing)await db.update(users).set({displayName:account.displayName||email,email,updatedAt:now}).where(eq(users.id,userId));
  else await db.insert(users).values({id:userId,email,displayName:account.displayName||email,passwordHash:"firebase-managed",createdAt:now,updatedAt:now});
  await createSession(userId);return Response.json({ok:true});
}
