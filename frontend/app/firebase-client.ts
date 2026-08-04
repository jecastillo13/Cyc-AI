import { getApps, initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBiy-98OybR5n6GjA-cOjmICjU2kAMtgSg",
  authDomain: "cyc-ai.firebaseapp.com",
  projectId: "cyc-ai",
  storageBucket: "cyc-ai.firebasestorage.app",
  messagingSenderId: "326786304833",
  appId: "1:326786304833:web:ebac85cb32eded8d17afc0",
};

const app=getApps()[0]??initializeApp(firebaseConfig);
export const firebaseAuth=getAuth(app);
