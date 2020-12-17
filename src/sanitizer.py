import json
from datetime import datetime

from pytz import utc


def sanitize(events):
    comments = events["comments"]
    team_1 = events["line_ups"]["team_1"]
    team_2 = events["line_ups"]["team_2"]

    team_1["name"] = team_1["name"].lower()
    team_2["name"] = team_2["name"].lower()


    if len(team_1['name'].split()) > 2:
        key_team_1 = team_1['name'].split()[0] + " " + team_1['name'].split()[1]
    else:
        key_team_1 = team_1['name']
    if len(team_2['name'].split()) > 2:
        key_team_2 = team_2['name'].split()[0] + " " + team_2['name'].split()[1]
    else:
        key_team_2 = team_2['name']

    team_1["key_name"] = key_team_1.replace(" ", "_")
    team_2["key_name"] = key_team_2.replace(" ", "_")

    for player in team_1["line_up"]:
        key_name = player["Snm"].replace(" ", "_").lower()
        player["key_name"] = key_name
        lookup_name = player["Snm"].lower()
        for comment in comments:
            comment['Txt'] = comment['Txt'].lower()
            comment['Txt'] = comment['Txt'].replace(lookup_name, key_name).lower()
            comment['Txt'] = comment['Txt'].replace(key_team_1, key_team_1.replace(" ", "_")).lower()


    for player in team_2["line_up"]:
        key_name = player["Snm"].replace(" ", "_").lower()
        player["key_name"] = key_name
        lookup_name = player["Snm"].lower()
        for comment in comments:
            comment['Txt'] = comment['Txt'].lower()
            comment['Txt'] = comment['Txt'].replace(lookup_name, key_name).lower()
            comment['Txt'] = comment['Txt'].replace(key_team_2, key_team_2.replace(" ", "_")).lower()

    return events