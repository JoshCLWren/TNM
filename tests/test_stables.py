import pytest

import circuits
import wrestlers
import stables
from database import cursor, con
import seed_db


def test_stable_serializer():
    """Tests Dropping and rebuilding stables table"""

    fake = seed_db.fake_stable()

    nwo = [{}]
    nwo[0]["Stable Name"] = fake["name"]
    nwo[0]["ids"] = fake["members"]

    stables.seed_stables(nwo)

    stables_in_db = stables.get_all_stables()

    assert len(stables_in_db) == 1


def test_stable_resource_get():
    """Tests retrieving a single stable by id"""

    stable = stables.get_by_id(1)

    assert stable
