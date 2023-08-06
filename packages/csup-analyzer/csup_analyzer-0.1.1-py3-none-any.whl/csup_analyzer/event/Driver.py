import pandas as pd

CAR_NAMES_BY_REPLAY_NAME = {
    "4x4-agitator": "Agitator",
    "50s-gt-brusso": "Brusso",
    "60s-gp-osprey": "Osprey",
    "80s-gp-generic": "Mantra",
    "bambino-cup-bambino": "Piccino",
    "eurotruck-geiger": "Bonk",
    "gp-spectre": "Storm",
    "gt-panther": "Panther",
    "prototype-conquest": "Conquest",
    "rally-vost": "Vost",
    "sprint-car-tubular": "Tubular",
    "stock-car": "Impact",
    "superlights-feather": "Feather",
    "touring-road-rebel": "Road Rebel",
    "trans-am-generic": "Loose Cannon",
    "top-gear-vehicle-nugget": "Rocket",
    "top-gear-vehicle-pickup": "Indestructible",
}


class Driver:
    def __init__(self, driver_id: str, driver_replay_dict: dict) -> None:
        self.assign_properties(driver_id, driver_replay_dict)
        self.series = None

    def assign_properties(self, did: str, d: dict) -> None:
        self.id = did

        self.name = d["racerName"]
        self.platform = d["platform"]
        self.is_ai = d["isAITeam"]

        self.colors = d["driverSkinLivery"][1]
        self.vehicle_colors = d["vehicleLivery"][1]

        self.car = CAR_NAMES_BY_REPLAY_NAME[d["vehicle"]]

    def as_series(self) -> pd.Series:
        if self.series is None:
            property_attributes = [
                attr
                for attr in dir(self)
                if not attr.startswith("__")
                and not callable(getattr(self, attr))
                and attr not in ["series", "id"]
            ]

            indices = property_attributes

            data = [getattr(self, attr) for attr in property_attributes]

            self.series = pd.Series(data=data, index=indices, name=self.id)

        return self.series

    def __str__(self) -> str:
        return self.name
