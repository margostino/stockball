from datetime import timedelta

import db
import scorer


client = db.initialize()


def get_matched_players(event, line_ups):
    matched_players_in_team_1 = [{"team": line_ups["team_1"]["key_name"], "player": item} for item in
                                 line_ups["team_1"]["line_up"] if item['key_name'].lower() in event.lower()]
    matched_players_in_team_2 = [{"team": line_ups["team_2"]["key_name"], "player": item} for item in
                                 line_ups["team_2"]["line_up"] if item['key_name'].lower() in event.lower()]
    return matched_players_in_team_1 + matched_players_in_team_2


def get_player_measurement(player, time, event):
    return scorer.calculate_player(player, event, time)


def get_team_measurement(line_up, time, event):
    team_1 = line_up['team_1']
    team_2 = line_up['team_2']
    return scorer.calculate_team(team_1, team_2, event, time)


def process(datetime, line_ups, event):
    if 'Min' in event:
        min = event['Min']
        prompt = "*"
        event_txt = event['Txt'].lower()
        # doc = nlp(txt)
        # min_stats = calculate_ner_stats(doc)

        if 'Min' in event:
            prompt = str(event['Min'])
        if 'MinEx' in event:
            prompt += "+" + str(event['MinEx'])

        time = datetime + timedelta(minutes=min)

        matched_players = get_matched_players(event_txt, line_ups)

        if len(matched_players) == 0:
            measurements = get_team_measurement(line_ups, time, event_txt)

            if measurements is not None:
                for measurement in measurements:
                    client.write_points([measurement])
        else:
            for player in matched_players:
                measurement = get_player_measurement(player, time, event_txt)
                if measurement is not None:
                    client.write_points([measurement])

        print(time.strftime("%Y-%m-%d %H:%M:%S") + " (" + prompt + ")" + " : " + event_txt)
