from leaguetools.ChampRollTools import parse_champion_name
from utils.Models import Session, Leaguechamps, LeaguechampsKeyCache


def parse_possible_champion_keys(name: tuple[str]) -> tuple[list[str], str]:
    parsed = [x.capitalize() for segment in name if segment != '\'' for x in segment.split('\'')]

    if not parsed:
        return [], ''

    capitalized_segments = ''.join(parsed)
    capitalized = capitalized_segments.capitalize()

    res = [capitalized, capitalized_segments]

    with Session() as session:
        parsedname = parse_champion_name(capitalized)

        champ = session.query(LeaguechampsKeyCache).where(LeaguechampsKeyCache.parsedname == parsedname).first()
        if champ:
            res.insert(0, champ.key)

        champ = session.query(Leaguechamps).where(Leaguechamps.parsedname == parsedname).first()
        if champ:
            res.append(champ.name)

    return res, parsedname
