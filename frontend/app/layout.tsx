import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import "./auth.css";

const sans=Geist({variable:"--font-sans",subsets:["latin"]});
const mono=Geist_Mono({variable:"--font-mono",subsets:["latin"]});

export const metadata:Metadata={title:"Cyc—AI | Tu estado, en movimiento",description:"Dashboard inteligente para analizar carga, recuperación y planificación de ciclismo.",icons:{icon:"/favicon.svg"}};

export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="es"><body className={`${sans.variable} ${mono.variable}`}>{children}</body></html>}
