import gzip
import shutil
import tempfile
from pathlib import Path


class FitImporter:

    @staticmethod
    def preparar(ruta_archivo: str) -> str:

        ruta = Path(ruta_archivo)

        # ¿Es un archivo .gz?
        if ruta.suffix.lower() == ".gz":

            temporal = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".fit"
            )

            with gzip.open(str(ruta), "rb") as origen:
                shutil.copyfileobj(origen, temporal)

            temporal.close()

            return temporal.name

        return str(ruta)