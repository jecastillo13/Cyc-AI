import { env } from "cloudflare:workers";
import { requireApiUser } from "../../server/current-user";

type AiBinding = { run(model: string, input: unknown): Promise<{ response?: string }> };

export async function POST(request: Request) {
  try {
    const user = await requireApiUser();
    const metrics = await request.json() as Record<string, unknown>;
    const ai = (env as unknown as { AI?: AiBinding }).AI;
    if (!ai) return Response.json({ error: "El Coach IA todavía no está habilitado." }, { status: 503 });
    const result = await ai.run("@cf/meta/llama-3.2-1b-instruct", {
      messages: [
        { role: "system", content: "Eres un entrenador de ciclismo prudente. Responde en español claro, máximo 130 palabras. Explica los datos, ofrece 3 acciones concretas y aclara que no sustituyes consejo médico. No inventes datos." },
        { role: "user", content: `Analiza para ${user.displayName} estos datos deportivos: ${JSON.stringify(metrics).slice(0, 5000)}` },
      ],
      max_tokens: 220,
    });
    return Response.json({ analysis: result.response || "No fue posible generar el análisis." });
  } catch (error) {
    if (error instanceof Response) return error;
    console.error("AI coach failed", error);
    return Response.json({ error: "No fue posible consultar el Coach IA ahora." }, { status: 502 });
  }
}
