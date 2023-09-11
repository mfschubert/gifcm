"""gifcm - Easy gif animation of matplotlib figures."""

from importlib import metadata

try:
    __version__ = metadata.version("gifcm")
except metadata.PackageNotFoundError:
    pass

__author__ = "Martin Schubert <mfschubert@gmail.com>"
__all__ = ["AnimatedFigure", "Frame"]

from gifcm.animated_figure import AnimatedFigure, Frame
