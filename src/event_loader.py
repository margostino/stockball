import json
from datetime import datetime

from pytz import utc


def load(source):
    with open(source) as json_file:
        data = json.load(json_file)

        if data["Eps"] == "FT":
            datetime_raw = str(data['Esd'])
            event_datetime = datetime(int(datetime_raw[0:4]), int(datetime_raw[4:6]), int(datetime_raw[6:8]),
                                      int(datetime_raw[8:10]), int(datetime_raw[10:12]), int(datetime_raw[12:14]),
                                      tzinfo=utc)
            line_ups = {
                "team_1": {
                    "name": data["T1"][0]["Nm"].lower(),
                    "line_up": [item['Ps'] for item in data['Lu'] if item['Tnb'] == 1][0]
                },
                "team_2": {
                    "name": data["T2"][0]["Nm"].lower(),
                    "line_up": [item['Ps'] for item in data['Lu'] if item['Tnb'] == 2][0]
                }
            }

            return {
                "comments": data['Com'],
                "datetime": event_datetime,
                "line_ups": line_ups
            }
        else:
            return {}
