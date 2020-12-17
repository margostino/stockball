import config
import re

rules = config.Config().cfg["rules"]
team_rules = config.Config().cfg["rules"]["team"]
player_rules = config.Config().cfg["rules"]["player"]


def get_team_measurements_for(time, team, score):
    measurements = []

    for player in team["line_up"]:
        if player["Pon"] != "COACH":
            if "cost" in player:
                player["cost"] += score
            else:
                player["cost"] = score
            measurements.append({
                "measurement": "performance",
                "tags": {
                    "player": player["key_name"],
                    "team": team["key_name"]
                },
                "time": time,
                "fields": {
                    "value": float(player["cost"])
                }
            })
    return measurements

def get_player_measurements_for(time, actor, score):
    if "cost" in actor["player"]:
        actor["player"]["cost"] += score
    else:
        actor["player"]["cost"] = score
    return {
        "measurement": "performance",
        "tags": {
            "player": actor["player"]["key_name"],
            "team": actor["team"]
        },
        "time": time,
        "fields": {
            "value": float(actor["player"]["cost"])
        }
    }


def match_rule(rule, actor, event):
    key_name = actor["key_name"]

    if rule["pattern"] in event and actor["key_name"] in event:
        if "pos" in rule and (event.find(key_name) == rule["pos"]):
            return True
        elif "pos" in rule and rule["pos"] == -1:
            return True
        elif "pos" not in rule:
            return True

    return False


def is_ball_possession(team_1, team_2, event):
    return re.search("ball possession: " + team_1["key_name"] + ": (\d+)%, " + team_2["key_name"] + ": (\d+)%.", event, re.IGNORECASE)


def calculate_team(team_1, team_2, event, time):
    measurements = []

    for rule in team_rules:
        if match_rule(rule, team_1, event):
            score = rule["score"]
            measurements = get_team_measurements_for(time, team_1, score)
        if match_rule(rule, team_2, event):
            score = rule["score"]
            measurements = get_team_measurements_for(time, team_2, score)

    ball_possession = is_ball_possession(team_1, team_2, event)

    if ball_possession:
        team_1_ball_possession_score = (float(ball_possession.group(1)) / 100) * 2
        team_2_ball_possession_score = (float(ball_possession.group(2)) / 100) * 2
        measurements += get_team_measurements_for(time, team_1, team_1_ball_possession_score)
        measurements += get_team_measurements_for(time, team_2, team_2_ball_possession_score)


    return measurements


def calculate_player(actor, event, time):
    measurement = None
    player = actor["player"]

    for rule in player_rules:
        if match_rule(rule, player, event):
            score = rule["score"]
            measurement = get_player_measurements_for(time, actor, score)

    if measurement is None:
        print("check!: " + event)

    return measurement
