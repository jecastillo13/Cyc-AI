import os


class IntegrationRegistry:
    """Reporta integraciones disponibles sin exponer credenciales."""

    PROVIDERS = {
        "strava": "STRAVA_ACCESS_TOKEN",
        "garmin": "GARMIN_CONNECT_TOKEN",
        "trainingpeaks": "TRAININGPEAKS_TOKEN",
        "intervals_icu": "INTERVALS_ICU_API_KEY",
    }

    def status(self) -> dict:
        return {
            provider: {
                "configured": bool(os.getenv(variable)),
                "environment_variable": variable,
            }
            for provider, variable in self.PROVIDERS.items()
        }
