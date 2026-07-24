import pandas as pd


class WorkoutHistory:

    def __init__(self, filename):
        self.filename = filename

    def load(self):

        df = pd.read_csv(self.filename)

        return {
            "total_entrenamientos": len(df),
            "columnas": list(df.columns)
        }