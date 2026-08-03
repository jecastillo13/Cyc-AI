import { cookies } from "next/headers";
import { eq } from "drizzle-orm";
import { getDb } from "../../../../db";
import { sessions, users } from "../../../../db/schema";
import { verifyPassword } from "../../../server/passwords";
import { hashToken, SESSION_COOKIE } from "../../../server/current-user";
export async function POST(request:Request){const body=await request.json() as {email?:string;password?:string};const email=body.email?.trim().toLowerCase()||"";const [user]=await getDb().select().from(users).where(eq(users.email,email)).limit(1);if(!user||!await verifyPassword(body.password||"",user.passwordHash))return Response.json({error:"Correo o contraseña incorrectos."},{status:401});const token=crypto.randomUUID()+crypto.randomUUID();const now=new Date();const expiresAt=new Date(now.getTime()+30*24*3600_000);await getDb().insert(sessions).values({id:crypto.randomUUID(),userId:user.id,tokenHash:await hashToken(token),expiresAt,createdAt:now});(await cookies()).set(SESSION_COOKIE,token,{httpOnly:true,secure:true,sameSite:"lax",path:"/",expires:expiresAt});return Response.json({ok:true})}
