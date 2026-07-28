import pandas as pd

from app.physiology.models.training_load_series import (
    TrainingLoadPoint,
    TrainingLoadSeries,
)


class TrainingLoadSeriesBuilder:
    """
    Construye una serie temporal de carga de entrenamiento a partir
    del historial exportado desde TrainingPeaks.

    Actualmente utiliza el TSS cuando está disponible.

    En futuras versiones podrá utilizar:
        - TRIMP
        - HRTSS
        - otras métricas de carga
    """

    DATE_COLUMN = "WorkoutDay"
    LOAD_COLUMN = "TSS"

    def build(self, history: pd.DataFrame) -> TrainingLoadSeries:

        points = []

        if history.empty:
            return TrainingLoadSeries(points=[])

        if self.DATE_COLUMN not in history.columns:
            return TrainingLoadSeries(points=[])

        if self.LOAD_COLUMN not in history.columns:
            return TrainingLoadSeries(points=[])

        dataframe = history.copy()

        dataframe[self.DATE_COLUMN] = pd.to_datetime(
            dataframe[self.DATE_COLUMN]
        )

        dataframe = dataframe.sort_values(self.DATE_COLUMN)

        dataframe = dataframe.dropna(subset=[self.LOAD_COLUMN])

        for _, row in dataframe.iterrows():

            points.append(
                TrainingLoadPoint(
                    date=row[self.DATE_COLUMN],
                    load=float(row[self.LOAD_COLUMN]),
                )
            )

        return TrainingLoadSeries(points=points)