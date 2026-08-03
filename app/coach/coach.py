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
        )

        return {
            "tipo_entrenamiento": workout_type,
            "recomendacion": recommendation,
            "training_load": {
                "method": training_load.method,
                "value": training_load.value,
                "confidence": training_load.confidence,
                "notes": training_load.notes
            }
        }
