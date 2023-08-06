# Copyright 2018-2020 Coop IT Easy SCRLfs (<http://coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Constant shared across the module"""

import os
from pathlib import Path

from prgconfig import PrgConfig

__productname__ = "ociedoo"
__version__ = "0.8.0-alpha.2"
__license__ = "GPL-3.0-or-later"

# Path for default value for config file
PGRNAME = "ociedoo"
DEFAULTSPATH = str(Path(__file__).parent / Path("defaults"))
DEFAULT_CONF = str(Path(DEFAULTSPATH) / "config")

config = PrgConfig(prg_name=PGRNAME, defaults_file=Path(DEFAULT_CONF))

# DB rules
REDBNAME = "^([a-zA-Z0-9-._]+)$"

# Default temporary directory
DEFAULT_TMP_DIR = os.getenv("TMPDIR", "~/.cache/ociedoo")

# odoo internal value
FILESTORE_DIR = "filestore"

# default config values
DEFAULT_DATA_DIR = "~/.local/share/Odoo"

# own conventions
# name of the top-level directory that a filestore backup must contain
FILESTORE_BACKUP_DIR = "filestore"
# prefix of the temporary directory to use when restoring a filestore backup
FILESTORE_TMP_DIR_PREFIX = "{0}-filestore".format(PGRNAME)
