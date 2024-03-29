from leaguetools.Constants import lane_data, lane_aliases
from bs4 import BeautifulSoup


async def parse_lolwiki(html):
    result = []
    table = html.find("table", class_="article-table sortable")  # table with all champions

    for row in table.find_all('tr')[1:]:  # iterate over all positions in table
        champ_data = {'name': row.find('td').text.strip()}

        lanes = list(lane_data.keys())
        for idx, td in enumerate(row.find_all('td')[1:-1]):
            champ_data[lanes[idx]] = bool(td.find_all())  # or td.text.strip() != '' # to include op.gg suggestions
        result.append(champ_data)
    return result


async def parse_gg(html):
    table_class = 'Champions__TableWrapper-rli9op-0 AllChampionsTable__TableContentWrapper-cpgif4-0 dLWELV cypsLf'
    div = html.find('div', class_=table_class).find_all('div', recursive=False)[1].find().find()
    rows = div.find_all('div', recursive=False)

    buffer = {}
    for row in rows:
        name = row.find('span', class_='champion-name').text

        if name not in buffer:
            buffer[name] = {'name': name, 'TOP': False, 'JUNGLE': False, 'MIDDLE': False, 'BOTTOM': False, 'UTILITY': False}

        role_div = row.find('div', class_='champion-role').find().find()  # content looks like 'role-top'
        lane = lane_aliases[role_div.text.split('-')[1]]
        buffer[name][lane] = True
    return buffer.values()


def op_gg_get_summonerid(res) -> int:
    if res.status_code != 200:
        print(f'op.gg profile refresh for returned code {res.status_code}')
        return 0

    html = BeautifulSoup(res.text, 'html.parser')

    div = html.find('div', attrs={'data-summoner-id': True})
    return div['data-summoner-id']
