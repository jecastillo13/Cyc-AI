class RecommendationEngine:

    def recommend(self, workout_type, training_status=None, training_load=0.0):

        if training_load >= 200:
            return "La sesión tuvo una carga muy alta. Programa recuperación y evita otra sesión exigente mañana."

        if training_status is not None:
            if training_status.tsb <= -20 or training_status.fatigue_score >= 80:
                return "La fatiga acumulada es alta. Prioriza descanso o recuperación muy suave."
            if training_status.tsb < -10:
                return "Tu carga reciente es elevada. Reduce la intensidad y vigila la recuperación."
            if training_status.ctl < 20 and training_status.recovery_score >= 60:
                return "Hay margen para construir base. Aumenta el volumen semanal de forma gradual, entre 5 % y 10 %."
            if training_status.recovery_score >= 75 and training_status.tsb >= -5:
                return "Estás bien recuperado. Es un buen momento para una sesión de calidad controlada."

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
