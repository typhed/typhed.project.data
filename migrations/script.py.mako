# -*- encoding: utf-8 -*-

"""
${message}

Revision ID: ${up_revision}
Revise Info: ${down_revision | comma,n}
Create Date: ${create_date}
"""

import sqlalchemy as sa

from alembic import op
from typing import Optional, Sequence, Union

${imports if imports else ""}

revision : str = ${repr(up_revision)}
down_revision : Optional[str] = ${repr(down_revision)}

# set the up-branch labels for auditing
branch_labels : Union[str, Sequence[str], None] = ${repr(branch_labels)}

# set dependency tree checks
depends_on : Union[str, Sequence[str], None] = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "PASS"}


def downgrade() -> None:
    ${downgrades if downgrades else "PASS"}
