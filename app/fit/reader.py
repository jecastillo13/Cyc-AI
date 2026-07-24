import fitdecode


class FitReader:

    def __init__(self, filename):
        self.filename = filename

    def read(self):

        registros = []

        with fitdecode.FitReader(self.filename) as fit:

            for frame in fit:

                if isinstance(frame, fitdecode.FitDataMessage):

                    registro = {
                        "type": frame.name
                    }

                    for campo in frame.fields:
                        registro[campo.name] = campo.value

                    registros.append(registro)

        return registros