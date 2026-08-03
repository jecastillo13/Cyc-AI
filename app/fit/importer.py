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

            try:
                with gzip.open(str(ruta), "rb") as origen:
                    shutil.copyfileobj(origen, temporal)
            except (gzip.BadGzipFile, EOFError, OSError) as exc:
                temporal.close()
                Path(temporal.name).unlink(missing_ok=True)
                raise ValueError("El archivo .fit.gz no contiene datos GZIP válidos.") from exc

            temporal.close()

            return temporal.name

        return str(ruta)
