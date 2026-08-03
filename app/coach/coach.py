from app.coach.classifier import WorkoutClassifier
from app.coach.recommendations import RecommendationEngine


class Coach:

    def __init__(self, context):

        self.context = context

        self.classifier = WorkoutClassifier()
        self.recommendation_engine = RecommendationEngine()

    def analyze(self):

        # Información del entrenamiento
        workout = self.context.workout

        # Información fisiológica
        training_load = self.context.training_load

        # Por ahora el clasificador sigue utilizando un diccionario.
        # Más adelante lo modificaremos para que trabaje directamente
        # con el objeto Workout.
        summary = {
            "distancia_km": workout.distance_km,
            "fc_media": workout.avg_hr
        }

        workout_type = self.classifier.classify(summary)

        recommendation = self.recommendation_engine.recommend(
            workout_type,
            self.context.training_status,
            training_load.value,
        )

        status = self.context.training_status
        fatigue_prediction = min(100.0, status.fatigue_score + training_load.value * 0.08)
        performance_prediction = max(0.0, min(100.0, status.fitness_score + status.tsb * 0.4))
        explanation = (
            f"Carga {training_load.value:.1f} por {training_load.method}; "
            f"ATL {status.atl:.1f}, CTL {status.ctl:.1f} y TSB {status.tsb:.1f}. "
            f"La disponibilidad es {status.readiness} y el riesgo estimado es {status.injury_risk}."
        )

        return {
            "tipo_entrenamiento": workout_type,
            "recomendacion": recommendation,
            "explicacion": explanation,
            "predicciones": {
                "fatiga_proxima_sesion": round(fatigue_prediction, 2),
                "rendimiento_actual": round(performance_prediction, 2),
            },
            "training_load": {
                "method": training_load.method,
                "value": training_load.value,
                "confidence": training_load.confidence,
                "notes": training_load.notes
            }
        }
