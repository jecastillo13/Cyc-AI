class WorkoutAnalyzer:

    def __init__(self, records):
        self.records = records

    def summary(self):

        registros = [
            r for r in self.records
            if r.get("type") == "record"
        ]

        if not registros:
            raise ValueError("El archivo FIT no contiene registros de actividad.")

        distancia = 0
        timestamps = []

        potencia = []
        pulso = []
        cadencia = []
        velocidad = []

        for r in registros:

            if r.get("distance") is not None:
                distancia = max(distancia, r["distance"])

            if r.get("timestamp") is not None:
                timestamps.append(r["timestamp"])

            if r.get("power") is not None:
                potencia.append(r["power"])

            if r.get("heart_rate") is not None:
                pulso.append(r["heart_rate"])

            if r.get("cadence") is not None:
                cadencia.append(r["cadence"])

            if r.get("speed") is not None:
                velocidad.append(r["speed"])

        tiempo = 0
        if len(timestamps) >= 2:
            tiempo = max(0, int((max(timestamps) - min(timestamps)).total_seconds()))

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
