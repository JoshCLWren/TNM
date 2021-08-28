import pytest

import circuits
import wrestlers
import tag_teams
from database import cursor, con
import seed_db


def test_tag_serializer():
    """Tests Dropping and rebuilding tag table"""

    fake = seed_db.fake_tag()

    tag_teams.seed_tags([fake])

    tags_in_db = tag_teams.get_all_tags()

    assert len(tags_in_db) == 1


def test_post_tag():
    """Test adding a tag"""

    fake = seed_db.fake_tag()

    tag_teams.post_tag_team(**fake)
    tags_in_db = tag_teams.get_all_tags()

    assert len(tags_in_db) == 2
