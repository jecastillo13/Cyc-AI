class WorkoutAnalyzer:

    def __init__(self, records):
        self.records = records

    def summary(self):

        registros = [
            r for r in self.records
            if r.get("type") == "record"
        ]

        if not registros:
            return {
                "error": "No hay registros de actividad"
            }

        distancia = 0
        tiempo = 0

        potencia = []
        pulso = []
        cadencia = []
        velocidad = []

        for r in registros:

            if "distance" in r:
                distancia = max(distancia, r["distance"])

            if "timestamp" in r:
                tiempo += 1

            if "power" in r:
                potencia.append(r["power"])

            if "heart_rate" in r:
                pulso.append(r["heart_rate"])

            if "cadence" in r:
                cadencia.append(r["cadence"])

            if "speed" in r:
                velocidad.append(r["speed"])

        return {

            "registros": len(registros),

            "distancia_km": round(distancia / 1000, 2),

            "duracion_segundos": tiempo,

            "potencia_media":
                round(sum(potencia) / len(potencia), 1)
                if potencia else None,

            "potencia_max":
                max(potencia)
                if potencia else None,

            "fc_media":
                round(sum(pulso) / len(pulso), 1)
                if pulso else None,

            "fc_max":
                max(pulso)
                if pulso else None,

            "cadencia_media":
                round(sum(cadencia) / len(cadencia), 1)
                if cadencia else None,

            "velocidad_media":
                round(sum(velocidad) / len(velocidad) * 3.6, 2)
                if velocidad else None
        }