class RecommendationEngine:

    def recommend(self, workout_type):

        recomendaciones = {
            "Fondo": "Prioriza la recuperación, hidratación y alimentación.",
            "Resistencia aeróbica": "Buen trabajo. Puedes continuar con el plan previsto.",
            "Alta intensidad": "Programa una sesión suave o de descanso al día siguiente.",
            "Entrenamiento general": "Mantén la constancia y revisa la evolución semanal."
        }

        return recomendaciones.get(
            workout_type,
            "Sin recomendaciones disponibles."
        )