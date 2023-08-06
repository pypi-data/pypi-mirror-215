"""logger-color
Different logging levels for stram (terminal) and file. Color the log messages.
Has additional levels for diagnostics: DIAG_INFO, DIAG_WARNING.

============== ===== ===========
Level		   Int   Color
============== ===== ===========
DEBUG          10    gray
INFO           20    green
WARNING		   30    yellow
ERROR		   40    red
CRITICAL	   50    bold red
DIAG_INFO      21    blue
DIAG_WARNING   31    blue bold
============== ===== ===========
"""

from logger_color.clogger import CLogger
from logger_color.functions import debug, info, warning, error, critical
from logger_color.functions import start_logging, diag_info, diag_warning

__all__ = [
    "CLogger",
    "critical",
    "debug",
    "diag_info",
    "diag_warning",
    "error",
    "info",
    "start_logging",
    "warning",
]

__title__ = "logger_color"
__version__ = "0.0.8"
__date__ = "2023-06-21"

__summary__ = "Different logging levels for stram (terminal) and file. Color the log messages. " \
              "Has additional levels for diagnostics: DIAG_INFO, DIAG_WARNING."
__author__ = "Vladimir Prusakov"
__email__ = "vladimir.prusakovs@gmail.com"
__url__ = "https://github.com/vladimirs-git/logger-color"
__download_url__ = f"{__url__}/archive/refs/tags/{__version__}.tar.gz"
__license__ = "MIT"
