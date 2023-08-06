class Lexicon():
    def __init__(self):
        raise NotImplementedError("Vocab is an abstract class and cannot be instantiated.")
    
    CONTINENTS = [
        'AMERICAS',
        'ASIA',
        'EUROPE'
    ]

    REGIONS = [
        'BR1',   # Brazil
        'EUN1',  # Europe Nordic & East
        'EUW1',  # Europe West
        'JP1',   # Japan
        'KR',    # Korea
        'LA1',   # Latin America North
        'LA2',   # Latin America South
        'NA1',   # North America
        'OC1',   # Oceania
        'PH2',   # Phillipines
        'RU',    # Russia
        'SG2',   # Singapore
        'TH2',   # Thailand
        'TR1',   # Turkey
        'TW2',   # Taiwan
        'VN2',   # Vietnam
    ]

    _CHAMPION_MASTERY_V4 = {
        'champion_masteries': 'lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}',  # get all champion mastery entries sorted by number of champion points descending
        'champion_mastery': 'lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{championId}', # get a champion mastery by puuid and championId
        'top_n_champion_masteries': 'lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={limit}',  #  get specified number of top champion mastery entries sorted by number of champion points descending
        'mastery_score': 'lol/champion-mastery/v4/scores/by-puuid/{puuid}',  # get a player's total champion mastery score, which is the sum of individual champion mastery levels
    }

    _CHAMPION_V3 = {
        'champion_rotation': 'lol/platform/v3/champion-rotations',  # get champion rotations, including f2p and low-level f2p rotations
    }

    # _CLASH_V1 = {}

    _LEAGUE_V4 = {
        'league_entries': 'lol/league/v4/entries/by-summoner/{summonerId}',  # get league entries in all queues for a given summonerId
    }

    # _LEAGUE_EXP_V4 = {}

    _LOL_CHALLENGES_V1 = {}

    # _LEAGUE_EXP_V4 = {}

    _MATCH_V5 = {}

    _SUMMONER_V4 = {
        'summoner': 'lol/summoner/v4/summoners/by-name/{summonerName}',  # get a summoner by summoner name
    }

    _DATA_DRAGON = {
        'dd_root': 'http://ddragon.leagueoflegends.com/cdn/{version}/',
        'all_champion_data': 'data/en_US/champion.json',  # get champion data (does not provide full champ info, will need to switch to champ_data endpoint)
        # 'champion_data': 'data/en_US/champion/{championName}.json',  # get champion data by champion name
        'items': 'data/en_US/item.json',  # get item data
        'summoner_spells': 'data/en_US/summoner.json',  # get summoner spell data
    }

    ENDPOINTS = {
        **_CHAMPION_V3,
        **_CHAMPION_MASTERY_V4,
        **_DATA_DRAGON,
        **_SUMMONER_V4,
    }