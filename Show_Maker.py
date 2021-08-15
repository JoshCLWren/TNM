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
import logging
from datetime import datetime
from roster_builder import roster_builder
from Match_Maker import matches

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="applog.txt",
    filemode="w",
    format="%(message)s",
)

logging.warning("Start of session")
logging.warning(datetime.today().strftime("%Y-%m-%d-%H:%M:%S"))


def Show(tv_show, match_total=3):
    print(f"Welcome to {tv_show}!")
    matches(tv_show=tv_show, match_total=match_total)


cont = "yes"
while cont == "yes" or cont == "y":
    print("Build/Update Databases?")
    # build_db = input()
    build_db = "y"
    if build_db == "y":
        logging.warning("Building Migrations")
        migrations.db_builder()
        logging.warning("Sleeping 5 seconds")
        # time.sleep(5)
        logging.warning("Building Circuit Assets")
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
    tv_input = int(input())

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

    print(f"How many matches will {tv_show} have?")
    match_total = int(input())
    logging.warning(f"Matches = {match_total}")
    logging.warning("Building Show")

    Show(tv_show=tv_show, match_total=match_total)
    print("Again?")
    cont = input()
