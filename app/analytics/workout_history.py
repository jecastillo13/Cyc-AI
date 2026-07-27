import pandas as pd


class WorkoutHistory:
    """
    Carga el historial de entrenamientos desde un archivo CSV.

    Devuelve un DataFrame para que pueda ser utilizado por los
    analizadores del sistema.
    """

    def __init__(self, filename):
        self.filename = filename

    def load(self) -> pd.DataFrame:

        return pd.read_csv(self.filename)