import json
from pathlib import Path


class UserManager:

    def __init__(self, username="default"):

        self.username = username

        self.user_path = Path("users") / username
        self.profile_path = self.user_path / "profile.json"
        self.fits_path = self.user_path / "fits"

    def create_user(self):

        self.user_path.mkdir(parents=True, exist_ok=True)
        self.fits_path.mkdir(parents=True, exist_ok=True)

        if not self.profile_path.exists():

            profile = {
                "name": self.username,
                "weight": None,
                "height": None,
                "ftp": None,
                "birth_date": None
            }

            self.save_profile(profile)

    def get_profile(self):

        with open(self.profile_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_profile(self, profile):

        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4)

    def get_fits_path(self):
        return self.fits_path