import { env } from "cloudflare:workers";

const encoder = new TextEncoder();
const decoder = new TextDecoder();

function encryptionKey() {
  const secret = (env as unknown as Record<string,string>).CONNECTION_ENCRYPTION_KEY;
  if (!secret) throw new Error("CONNECTION_ENCRYPTION_KEY is not configured");
  return crypto.subtle.importKey("raw", encoder.encode(secret), "PBKDF2", false, ["deriveKey"]);
}

async function keyFor(salt: Uint8Array) {
  const base = await encryptionKey();
  return crypto.subtle.deriveKey({ name:"PBKDF2", salt, iterations:120000, hash:"SHA-256" }, base, { name:"AES-GCM", length:256 }, false, ["encrypt","decrypt"]);
}

export async function encryptSecret(value:string) {
  const salt=crypto.getRandomValues(new Uint8Array(16)); const iv=crypto.getRandomValues(new Uint8Array(12));
  const encrypted=await crypto.subtle.encrypt({name:"AES-GCM",iv},await keyFor(salt),encoder.encode(value));
  return [salt,iv,new Uint8Array(encrypted)].map(bytes=>btoa(String.fromCharCode(...bytes))).join(".");
}

export async function decryptSecret(payload:string) {
  const [saltValue,ivValue,dataValue]=payload.split(".");
  const decode=(value:string)=>Uint8Array.from(atob(value),char=>char.charCodeAt(0));
  const salt=decode(saltValue),iv=decode(ivValue),data=decode(dataValue);
  return decoder.decode(await crypto.subtle.decrypt({name:"AES-GCM",iv},await keyFor(salt),data));
}

export async function signState(userId:string) {
  const secret=(env as unknown as Record<string,string>).OAUTH_STATE_SECRET;
  if(!secret)throw new Error("OAUTH_STATE_SECRET is not configured");
  const payload=btoa(JSON.stringify({userId,expires:Date.now()+10*60_000,nonce:crypto.randomUUID()}));
  const key=await crypto.subtle.importKey("raw",encoder.encode(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);
  const signature=new Uint8Array(await crypto.subtle.sign("HMAC",key,encoder.encode(payload)));
  return `${payload}.${btoa(String.fromCharCode(...signature))}`;
}

export async function verifyState(state:string,userId:string) {
  const [payload,signature]=state.split("."); if(!payload||!signature)return false;
  const secret=(env as unknown as Record<string,string>).OAUTH_STATE_SECRET; if(!secret)return false;
  const key=await crypto.subtle.importKey("raw",encoder.encode(secret),{name:"HMAC",hash:"SHA-256"},false,["verify"]);
  const sig=Uint8Array.from(atob(signature),char=>char.charCodeAt(0));
  const valid=await crypto.subtle.verify("HMAC",key,sig,encoder.encode(payload));
  if(!valid)return false; const body=JSON.parse(atob(payload)) as {userId:string;expires:number};
  return body.userId===userId&&body.expires>Date.now();
}
