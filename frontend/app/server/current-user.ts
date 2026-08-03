import { cookies } from "next/headers";
import { and, eq, gt } from "drizzle-orm";
import { getDb } from "../../db";
import { sessions, users } from "../../db/schema";

export const SESSION_COOKIE = "cyc_session";

export async function requireApiUser() {
  const token = (await cookies()).get(SESSION_COOKIE)?.value;
  if (!token) throw new Response("Unauthorized", { status: 401 });
  const [row] = await getDb().select({userId:users.id,email:users.email,displayName:users.displayName})
    .from(sessions).innerJoin(users,eq(sessions.userId,users.id))
    .where(and(eq(sessions.tokenHash,await hashToken(token)),gt(sessions.expiresAt,new Date()))).limit(1);
  if (!row) throw new Response("Unauthorized", { status: 401 });
  return { userId:row.userId, email:row.email, displayName:row.displayName, fullName:row.displayName };
}

export async function hashToken(value:string){const bytes=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value));return toBase64(new Uint8Array(bytes))}
export function toBase64(bytes:Uint8Array){let value="";for(const byte of bytes)value+=String.fromCharCode(byte);return btoa(value)}
