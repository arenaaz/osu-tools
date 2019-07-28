#!/usr/bin/env python
# coding: utf-8

import sys
from pathlib import Path
from db import *

sys.path.append("projects/osu!tools/")

user_home = str(Path.home())

osu_osu_file = user_home + '\\AppData\\Local\\osu!\\osu!.db'
osu_collection_file = user_home + '\\AppData\\Local\\osu!\\collection.db'

with open(osu_collection_file, "rb") as f:
    coll_db = CollectionDB(f)

OSU_GAME_TYPES = ['standard', 'taiko', 'ctb', 'mania']
OSU_BEATMAP_RANKED_STATUS = ['unknown', 'unsubmitted', 'pending/wip/graveyard', 'unused','ranked', 'approved', 'qualified', 'loved']

beatmap_list = []

with open(osu_osu_file, "rb") as f:

    osu_version, folder_count = read_int(f), read_int(f)
    print('osu! version:', osu_version)
    print('Folder Count:', folder_count)

    account_unlocked, date_account_unlocked = read_bool(f), read_datetime(f)
    print('AccountUnlocked:', account_unlocked)
    print('Date the account will be unlocked:', date_account_unlocked)

    player_name = read_string(f)
    print('Player name:', player_name)

    beatmap_count = read_int(f)
    print('Number of beatmaps:', beatmap_count)

    for c in range(beatmap_count):

        entry_size = read_int(f)
        artist_name, artist_name_u = read_string(f), read_string(f)
        song_title, song_title_u = read_string(f), read_string(f)
        creator_name = read_string(f)
        difficulty = read_string(f)
        audio_file_name = read_string(f)
        beatmap_hash = read_string(f)
        osu_filename = read_string(f)
        ranked_status = read_byte(f)
        hitcircle_count, slider_count, spinner_count = read_short(f), read_short(f), read_short(f)
        last_mod_time = read_datetime(f)
        approach_rate, circle_size, hp_drain = read_single(f), read_single(f), read_single(f)
        overall_difficulty = read_single(f)
        slider_velocity = read_double(f)
        star_ratings = {}
        for game_type in OSU_GAME_TYPES:
            pair_count = read_int(f)

            mod_stars = []
            for _ in range(pair_count):
                read_byte(f)  # 0x08
                mod_comb = read_int(f)
                read_byte(f)  # 0x0d
                stars = read_double(f)
                mod_stars.append((mod_comb, stars))

            star_ratings[game_type] = mod_stars

        drain_time, total_time, preview_time = read_int(f), read_int(f), read_int(f)
        timing_point_count = read_int(f)
        timing_points = []
        for _ in range(timing_point_count):
            bpm, offset, inherited = read_double(f), read_double(f), not read_bool(f)
            timing_points.append((bpm, offset, inherited))

        beatmap_id, beatmap_set_id, thread_id = read_int(f), read_int(f), read_int(f)
        grades = {game_type: read_byte(f) for game_type in OSU_GAME_TYPES}
        local_beatmap_offset = read_short(f)
        stack_leniency = read_single(f)
        gameplay_mode = read_byte(f)
        song_source, song_tags = read_string(f), read_string(f)
        online_offset = read_short(f)
        song_font = read_string(f)
        beatmap_unplayed = read_bool(f)
        beatmap_last_played = read_datetime(f)
        beatmap_osz2 = read_bool(f)
        beatmap_folder = read_string(f)
        beatmap_last_checked = read_datetime(f)
        ignore_sound, ignore_skin, disable_storyboard, disable_video, visual_override =\
            read_bool(f), read_bool(f), read_bool(f), read_bool(f), read_bool(f)
        last_modified = read_int(f)
        mania_scroll_speed = read_byte(f)

        beatmap_list.append((beatmap_hash, song_title, difficulty, artist_name))

    print('Length of beatmap_list:', len(beatmap_list))

# collect hashs from all beatmaps
beatmap_hashs = [x[0] for x in beatmap_list]

# collect hashs from all collections
coll_hashs = []
for name, coll in coll_db.collections.items():
    print('collection name:', name, '[', len(coll.beatmap_md5s), ']')
    coll_hashs.extend(coll.beatmap_md5s)
print('total number of hashes in collections:', len(coll_hashs))

# find beatmap hashs not in any collections
hashs_not_in_coll = set(beatmap_hashs) - set(coll_hashs)
print('number of beatmap hashs not in any collections:', len(hashs_not_in_coll))

# reveal name of beatmap not in any collections
beatmaps_not_in_coll = [bm for bm in beatmap_list if bm[0] in hashs_not_in_coll]
print('number of beatmaps not in any collections:', len(beatmaps_not_in_coll))

# write beatmap info to file
beatmaps_not_in_coll_file = user_home + '\\Desktop\\beatmapss_not_in_coll.txt'
with open(beatmaps_not_in_coll_file, "w") as f:
    f.write(f'number of beatmap hashs not in any collections: {len(beatmaps_not_in_coll)}\n')
    f.write('\n'.join([f'{bm[1]} ({bm[2]}) - {bm[3]}' for bm in beatmaps_not_in_coll]))
