"""in organs change  unique constraint

Revision ID: 8b34c669c41f
Revises: 74bc7ebad04c
Create Date: 2024-04-17 23:35:25.207189

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b34c669c41f"
down_revision: Union[str, None] = "74bc7ebad04c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "organs_id_name_short_name_code_external_id_key", "organs", type_="unique"
    )
    op.create_unique_constraint(None, "organs", ["id", "external_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "organs", type_="unique")
    op.create_unique_constraint(
        "organs_id_name_short_name_code_external_id_key",
        "organs",
        ["id", "name", "short_name", "code", "external_id"],
    )
    # ### end Alembic commands ###
