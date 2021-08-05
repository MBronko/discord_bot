from utils.Models import Leaguechamps

lane_icon_url_prefix = 'https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-parties/global/default/icon-position-'
team_icon_url = 'https://static.wikia.nocookie.net/leagueoflegends/images/8/80/Summoner%27s_Rift_icon.png'

lane_data: dict[str, dict[str]] = {
    'TOP':     {'display_name': 'Top',     'db_field': Leaguechamps.top},
    'JUNGLE':  {'display_name': 'Jungle',  'db_field': Leaguechamps.jungle},
    'MIDDLE':  {'display_name': 'Mid',     'db_field': Leaguechamps.mid},
    'BOTTOM':  {'display_name': 'Adc',     'db_field': Leaguechamps.adc},
    'UTILITY': {'display_name': 'Support', 'db_field': Leaguechamps.support},
    'FILL':    {'display_name': 'Fill',    'db_field': None},
    'UNSELECTED': {'display_name': ' Unselected', 'db_field': None}
}

for idx, key in enumerate(lane_data):
    lane = lane_data[key]
    lane['icon_url'] = f'{lane_icon_url_prefix}{key.lower()}.png'
    lane['sort_value'] = idx
