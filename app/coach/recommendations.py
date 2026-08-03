class RecommendationEngine:

    def recommend(self, workout_type, training_status=None):

        if training_status is not None:
            if training_status.tsb <= -20 or training_status.fatigue_score >= 80:
                return "La fatiga acumulada es alta. Prioriza descanso o recuperación muy suave."
            if training_status.tsb < -10:
                return "Tu carga reciente es elevada. Reduce la intensidad y vigila la recuperación."

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
