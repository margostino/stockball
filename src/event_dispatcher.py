import config
import db
import event_loader
import event_processor
import sanitizer
import json
import requests
from os import walk

sources_path = config.Config().cfg["sources_path"]
fantasy_url = config.Config().cfg["fantasy_url"]
client = db.initialize()

response = requests.get(fantasy_url)
fantasy_data = json.loads(response.text)

sources = []

# max_clean_sheets = -1
# max_clean_sheets_player = ""
#
# for player in fantasy_data["elements"]:
#     if player["clean_sheets"] > max_clean_sheets:
#         max_clean_sheets = player["clean_sheets"]
#         max_clean_sheets_player = player

# TODO: sanitize fantasy data
for player in fantasy_data["elements"]:
    player["second_name"] = player["second_name"].replace("é", "e")

for (dirpath, dirnames, filenames) in walk(sources_path):
    for event_path_id in dirnames:
        event_file = "{}/{}/0/index.html".format(dirpath, event_path_id)
        sources.append(event_file)

for source in sources:
    raw = event_loader.load(source)
    if len(raw) > 0:
        events = sanitizer.sanitize(raw)
        datetime = events["datetime"]
        line_ups = events["line_ups"]

        for player in line_ups["team_1"]["line_up"]:
            # TODO: patch properly
            if "Fn" not in player:
                player["Fn"] = player["Ln"]

            fantasy_player = [item for item in fantasy_data["elements"] if player["Fn"] in item["first_name"] and player["Ln"] in item["second_name"]]

            if len(fantasy_player) == 1:
                now_cost = fantasy_player[0]["now_cost"]  # TODO: evaluate initial season cost
                player["cost"] = now_cost

            if len(fantasy_player) > 1:
                print("check players match!")

        for player in line_ups["team_2"]["line_up"]:
            # TODO: patch properly
            if "Fn" not in player:
                player["Fn"] = player["Ln"]

            fantasy_player = [item for item in fantasy_data["elements"] if player["Fn"] in item["first_name"] and player["Ln"] in item["second_name"]]

            if len(fantasy_player) == 1:
                now_cost = fantasy_player[0]["now_cost"]  # TODO: evaluate initial season cost
                player["cost"] = now_cost

            if len(fantasy_player) > 1:
                print("check players match!")

        for event in reversed(events["comments"]):
            event_processor.process(datetime, line_ups, event)

print("end")
