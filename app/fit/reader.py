import fitdecode


class FitReader:

    def __init__(self, filename):
        self.filename = filename

    def read(self):

        registros = []

        try:
            return self._read_frames()
        except fitdecode.FitError as exc:
            raise ValueError("El archivo FIT está corrupto o no tiene un formato válido.") from exc

    def _read_frames(self):
        registros = []

        with fitdecode.FitReader(self.filename) as fit:

            for frame in fit:

                if not isinstance(frame, fitdecode.FitDataMessage):
                    continue

                registro = {
                    "type": frame.name
                }

                for campo in frame.fields:

                    nombre = campo.name
                    valor = campo.value

                    if nombre in [
                        "timestamp",
                        "distance",
                        "speed",
                        "heart_rate",
                        "cadence",
                        "power",
                        "altitude",
                        "position_lat",
                        "position_long",
                        "total_timer_time",
                        "total_elapsed_time",
                        "total_distance",
                        "avg_speed",
                        "max_speed",
                        "avg_power",
                        "max_power",
                        "avg_heart_rate",
                        "max_heart_rate",
                        "avg_cadence",
                        "max_cadence",
                        "total_ascent",
                        "total_descent",
                        "total_calories",
                        "sport",
                        "sub_sport"
                    ]:
                        registro[nombre] = valor

                registros.append(registro)

        return registros
