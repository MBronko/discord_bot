from discord.ext.commands import command, Cog, Context
from discord import Embed

from urllib import parse
from utils.Common import GREEN_TICK, RED_X
from leaguetools.RiotAPI.tasks import get_summoner, get_champion
from leaguetools.RiotAPI.tools import match_history_most_played_champs, gather_summoner_data, refresh_op_gg_profiles
from leaguetools.Constants import lane_data

from pyot.models import lol
from pyot.core import Gatherer
from pyot.utils import PtrCache
from pyot.core.exceptions import NotFound


class RiotAPI(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def level(self, ctx: Context, *name: str):
        name = ''.join(name)

        summoner = await get_summoner(ctx, name)

        if summoner:
            return await ctx.send(f'{summoner.name} has {summoner.level}lv.')

    @command()
    async def chest(self, ctx: Context, name: str = '', *champ_name: str):
        summoner = await get_summoner(ctx, name)

        if not summoner:
            return

        champ = await get_champion(ctx, champ_name)

        if not champ:
            return

        champ_mastery = None

        try:
            champ_mastery = await lol.ChampionMastery(summoner_id=summoner.id, champion_id=champ.id).get()
        except NotFound:
            pass

        if champ_mastery and champ_mastery.chest_granted:
            inner_msg = f'unavailable {RED_X}'
        else:
            inner_msg = f'available {GREEN_TICK}'

        await ctx.send(f'Chest for {summoner.name} on {champ.name} is {inner_msg}')

    @command()
    async def clash(self, ctx: Context, *name: str):
        name = ''.join(name)

        summoner = await get_summoner(ctx, name)

        if not summoner:
            return

        buf = await summoner.clash_players.get()
        incomplete_clash_players = buf.players

        if not incomplete_clash_players:
            return await ctx.send(f'{summoner.name} doesnt belong to any clash team')

        team = await incomplete_clash_players[0].team.get()

        async with Gatherer() as gatherer:
            players_cache = PtrCache()
            match_history_cache = PtrCache()
            champions_cache = PtrCache()

            gatherer.statements = [player.summoner for player in team.players]
            players = await gatherer.gather()  # type: list[lol.Summoner]

            for player in players:
                players_cache.set(player.id, player)

            statements = [player.match_history.query(queue_ids=[700]) for player in players]
            gatherer.statements = statements
            match_histories = await gatherer.gather()  # type: list[lol.MatchHistory]

            for history in match_histories:
                match_history_cache.set(history.account_id, history)

            gatherer.statements = [player.profile_icon for player in players]
            await gatherer.gather()

            champion_set = set()
            most_played_champions = {}
            for match_history in match_histories:  # type: lol.MatchHistory
                top_champs = match_history_most_played_champs(match_history)[:5]
                most_played_champions[match_history.account_id] = top_champs
                champion_set.update([champ for champ, times in top_champs])

            statements = [lol.Champion(id=idx) for idx in champion_set]
            gatherer.statements = statements
            champions = await gatherer.gather()  # type: list[lol.Champion]

            for champion in champions:
                champions_cache.set(champion.id, champion)

            for acc_id, champs in most_played_champions.items():
                most_played_champions[acc_id] = [(champions_cache.get(champ_id).name, n) for champ_id, n in champs]

        team_embed = Embed()

        team_name = team.name if team.name else 'Team Name'
        team_tag = team.abbreviation if team.abbreviation else 'TAG'
        clash_icon = f'https://raw.communitydragon.org/latest/game/assets/clash/roster-logos/{team.icon_id}/1_64.png'

        team_embed.set_author(name=f'[{team_tag}] {team_name}', icon_url=clash_icon)
        team_embed.set_thumbnail(url=clash_icon)

        captain = players_cache.get(team.captain_summoner_id)  # type: lol.Summoner
        team_data = [
            f'Captain: {captain.name}',
            f'Tier: {team.tier}'
        ]

        team_embed.add_field(name='General info', value='\n'.join(team_data), inline=False)

        player_names: list[str] = []
        player_lanes: list[tuple[str, str]] = []
        player_embeds: list[Embed] = []
        for clash_player_data in sorted(team.players, key=lambda x: lane_data[x.position]['sort_value']):
            player = players_cache.get(clash_player_data.summoner_id)  # type: lol.Summoner

            position = clash_player_data.position
            match_history = match_history_cache.get(player.account_id)  # type: lol.MatchHistory

            champs_played = most_played_champions[player.account_id]

            embed = await gather_summoner_data(player, position, match_history, champs_played)

            player_embeds.append(embed)
            player_names.append(player.name)
            player_lanes.append((player.name, clash_player_data.position))

        player_roles = [f'{name}: {lane_data[lane]["display_name"]}' for name, lane in player_lanes]
        team_embed.add_field(name='Members', value='\n'.join(player_roles))

        url_encoded_names = ",".join([parse.quote(name) for name in player_names])

        urls = {
            'op.gg': f'https://eune.op.gg/multi/query={url_encoded_names}',
            'u.gg': f'https://u.gg/multisearch?summoners={url_encoded_names}&region=eun1',
            'porofessor.gg': f'https://porofessor.gg/pregame/eune/{url_encoded_names}'
        }

        aliased_links = [f'[{site}]({url})' for site, url in urls.items()]
        team_embed.add_field(name='Third party sites', value='\n'.join(aliased_links), inline=False)

        await ctx.send(embed=team_embed)
        for embed in player_embeds:
            await ctx.send(embed=embed)

        refresh_op_gg_profiles(player_names)


def setup(bot):
    bot.add_cog(RiotAPI(bot))
