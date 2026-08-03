import { cookies } from "next/headers";
import { eq } from "drizzle-orm";
import { getDb } from "../../../../db";
import { sessions } from "../../../../db/schema";
import { hashToken, SESSION_COOKIE } from "../../../server/current-user";
export async function GET(request:Request){const jar=await cookies();const token=jar.get(SESSION_COOKIE)?.value;if(token)await getDb().delete(sessions).where(eq(sessions.tokenHash,await hashToken(token)));jar.delete(SESSION_COOKIE);return Response.redirect(new URL("/login",request.url))}
