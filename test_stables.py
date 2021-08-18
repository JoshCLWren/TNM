import pytest

import circuits
import wrestlers
import stables
from database import cursor, con

fake_stable = {"Stable Name": "nwo", "ids": [1, 2, 3]}


def test_stable_serializer():
    """Tests Dropping and rebuilding stables table"""

    stables.seed_stables([fake_stable])

    stables_in_db = stables.get_all_stables()

    assert len(stables_in_db) == 1


def test_stable_resource_get():
    """Tests retrieving a single stable by id"""

    stable = stables.get_by_id(1)

    assert stable
