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

    La serie resultante es diaria y continua. Los días sin
    entrenamiento se rellenan con una carga de 0 para que los
    cálculos de ATL y CTL reproduzcan correctamente el modelo
    exponencial de Bannister.

    En futuras versiones podrá utilizar:
        - TRIMP
        - HRTSS
        - otras métricas de carga
    """

    DATE_COLUMN = "WorkoutDay"
    LOAD_COLUMN = "TSS"

    def build(self, history: pd.DataFrame) -> TrainingLoadSeries:

        if history.empty:
            return TrainingLoadSeries(points=[])

        if self.DATE_COLUMN not in history.columns:
            return TrainingLoadSeries(points=[])

        if self.LOAD_COLUMN not in history.columns:
            return TrainingLoadSeries(points=[])

        dataframe = history.copy()

        # Convertir la columna de fecha y eliminar la parte horaria.
        dataframe[self.DATE_COLUMN] = (
            pd.to_datetime(dataframe[self.DATE_COLUMN])
            .dt.normalize()
        )

        # Ordenar cronológicamente.
        dataframe = dataframe.sort_values(self.DATE_COLUMN)

        # Sustituir cargas nulas por 0.
        dataframe[self.LOAD_COLUMN] = (
            dataframe[self.LOAD_COLUMN]
            .fillna(0.0)
            .astype(float)
        )

        # Si existen varios entrenamientos el mismo día,
        # se suman sus cargas.
        dataframe = (
            dataframe
            .groupby(self.DATE_COLUMN, as_index=False)[self.LOAD_COLUMN]
            .sum()
        )

        # Crear un calendario diario completo.
        full_range = pd.date_range(
            start=dataframe[self.DATE_COLUMN].min(),
            end=dataframe[self.DATE_COLUMN].max(),
            freq="D",
        )

        # Añadir los días sin entrenamiento con carga 0.
        dataframe = (
            dataframe
            .set_index(self.DATE_COLUMN)
            .reindex(full_range, fill_value=0.0)
            .rename_axis(self.DATE_COLUMN)
            .reset_index()
        )

        points = []

        for _, row in dataframe.iterrows():

            points.append(
                TrainingLoadPoint(
                    date=row[self.DATE_COLUMN],
                    load=float(row[self.LOAD_COLUMN]),
                )
            )

        return TrainingLoadSeries(points=points)