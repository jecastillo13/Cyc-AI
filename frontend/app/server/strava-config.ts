import { env } from "cloudflare:workers";

export function stravaConfig(){const config=env as unknown as Record<string,string>;return {clientId:config.STRAVA_CLIENT_ID||"269720",clientSecret:config.STRAVA_CLIENT_SECRET||""}}
