from importlib_metadata import version

from plastik import colors
from plastik.axes import *  # noqa:F401,F403
from plastik.legends import *  # noqa:F401,F403
from plastik.ridge import *  # noqa:F401,F403

__version__ = version(__package__)
__all__ = ["colors"]
