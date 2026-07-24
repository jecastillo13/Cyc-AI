from app.coach.classifier import WorkoutClassifier
from app.coach.recommendations import RecommendationEngine


class Coach:

    def __init__(self, context):

        self.context = context

        self.classifier = WorkoutClassifier()
        self.recommendation_engine = RecommendationEngine()

    def analyze(self):

        workout = self.context.workout

        summary = {
            "distancia_km": workout.distance_km,
            "fc_media": workout.avg_hr
        }

        workout_type = self.classifier.classify(summary)

        recommendation = self.recommendation_engine.recommend(workout_type)

        return {
            "tipo_entrenamiento": workout_type,
            "recomendacion": recommendation
        }