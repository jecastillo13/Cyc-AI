class WorkoutClassifier:

    def classify(self, summary):

        distancia = summary.get("distancia_km", 0)
        fc = summary.get("fc_media", 0)

        if distancia >= 100:
            return "Fondo"

        if distancia >= 60 and fc <= 145:
            return "Resistencia aeróbica"

        if fc >= 160:
            return "Alta intensidad"

        return "Entrenamiento general"