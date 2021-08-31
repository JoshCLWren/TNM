# Objects:
# Circuits.
# Circuits have brands
# Brands have shows
# Shows have matches
# Circuits also have super shows
# Shows have regular matches and main events.
# Matches have Wrestlers
# Wrestlers have a Circuit/Brand/Gender/Name/Tag Teams/Stables
# Tag Teams have two Wrestlers
# Stables have more than two Wrestlers
# Regular matches are single/tag/multi-man/battle royal/ and are 1v1/triangle/4way
# Main Events are single/tag/multi-man/ with #1 contender spot or title shot and are 1v1/triangle/4way
# Feuds are a wrestler/tag-team/stable vs wrestler/tag-team/stable
# Super shows have multiple main events and gimmick matches
# Royal Rumbles/war games/elimination chambers have wrestlers and are only on Super Shows
from circuit_assets import circuit_assets
import migrations
import circuit_assets
import time
from datetime import datetime
from roster_builder import roster_builder
from Match_Maker import matches
import database
import Shows


def Show(tv_show, match_total=3):
    print(f"Welcome to {tv_show}!")
    database.shows_table()
    show = Shows.create_show(tv_show, match_total)
    matches(show)


cont = "yes"
while cont == "yes" or cont == "y":
    print("Build/Update Databases?")
    build_db = input()
    build_db = "y"
    if build_db == "y":
        migrations.db_builder()
        circuit_assets.circuit_assets()
    else:
        "Please Proceed"
    print("Which show are you making?")
    print("1. Raw")
    print("2. Smackdown")
    print("3. 205")
    print("4. IMPACT")
    print("5. CMLL")
    print("6. ROH")
    tv_input = input()
    try:
        tv_input = int(tv_input)
    except Exception:
        cont = "no"
        continue
    if tv_input == 1:
        tv_show = "Raw"
    elif tv_input == 2:
        tv_show = "Smackdown"
    elif tv_input == 3:
        tv_show = "205"
    elif tv_input == 4:
        tv_show = "IMPACT"
    elif tv_input == 5:
        tv_show = "CMLL"
    elif tv_input == 6:
        tv_show = "ROH"
    else:
        cont = "no"

    print(f"How many matches will {tv_show} have?")
    match_total = int(input())

    Show(tv_show=tv_show, match_total=match_total)
    print("Again?")
    cont = input()
