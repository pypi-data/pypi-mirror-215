"""Module for converting input figure into Econoplots style."""
# %% Imports

# Standard Library Imports

# Third Party Imports
from matplotlib import pyplot as plt  # noqa
from matplotlib.axes import Axes

# Econoplots Imports
from econoplots.params import setRCParams
from econoplots.utils import (
    loadColorMap,
    makePatchSpinesInvisible,
    nudgeBottomSpine,
    plotZeroPt,
    replaceAxesMinusGlyphs,
    setBarXAxisParams,
    setBarYAxisParams,
    setBoxColor,
    setDefaultLineColors,
    setDefaultPatchColors,
    setLegendParams,
    setLineColor,
    setLineXAxisParams,
    setLineYAxisParams,
    updateLegendEntryColors,
)

# %% Load color map and set parameters
setRCParams()

# with open("econoplots/color_map.json") as json_file:
#     color_map = json.load(json_file)

# %% Functions


def convert2Econo(
    ax: Axes,
    ax_type: str = "line",
    **kwargs,
) -> Axes:
    """Formats a Matplotlib Axes as a pseudo-Economist figure.

    Args:
        ax (Axes): A Matplotlib object.
        ax_type (str, optional): ["line" | "fill" | "hbox"] What type of plot is
            contained in ax. Defaults to "line".
        fill_area: Used for line plots.

    Returns:
        Axes: A Matplotlib object.
    """
    assert isinstance(ax, Axes)
    assert ax_type in [
        "line",
        "fill",
        "hbox",
    ], "ax_type not in recognized list."

    converter_map = {
        "line": convertLine,
        "hbox": convertHBox,
        "fill": convertLineFill,
    }

    # color_map = loadColorMap()
    ax = converter_map[ax_type](ax, **kwargs)

    return ax


def convertLine(
    ax: Axes,
    zero_dot: bool = False,
) -> Axes:
    # Set general lie plot defaults
    ax = setLineDefaults(ax)

    # Change line colors
    setDefaultLineColors(ax)

    ax = updateLegendEntryColors(ax)

    if zero_dot is True:
        ax = plotZeroPt(ax, marker_size=10)

    return ax


def setLineDefaults(ax: Axes) -> Axes:
    color_map = loadColorMap()

    # Change axis color
    ax.grid(
        which="major",
        axis="y",
        color=color_map["grid"]["grid_gray"],
        zorder=1,
        clip_on=False,
    )
    # set axis params
    # y_offset_text = ax.yaxis.get_offset_text().get_text()
    # x_offset_text = ax.xaxis.get_offset_text().get_text()
    replaceAxesMinusGlyphs(ax)
    setLineYAxisParams(ax, side="right", label_location="right")

    # Move bottom spine before setting xAxis params to avoid Xticks being regenerated
    nudgeBottomSpine(ax)
    setLineXAxisParams(ax, pad_side="right", minor_ticks_on=True)

    # delete top, right, left spines
    makePatchSpinesInvisible(ax, ["top", "right", "left"])

    # Set legend background
    setLegendParams(ax)

    return ax


def convertLineFill(ax: Axes) -> Axes:
    # Set general lie plot defaults
    ax = setLineDefaults(ax)

    ax = setDefaultPatchColors(ax)

    ax = updateLegendEntryColors(ax)

    return ax


def convertHBox(ax: Axes) -> Axes:
    assert (
        len(ax.patches) > 0
    ), "Input Axes does not have filled boxes. Remake plot by setting patch_artist=True."

    color_map = loadColorMap()
    # Set grid on and color
    ax.grid(
        which="major",
        axis="x",
        color=color_map["grid"]["grid_gray"],
        zorder=1,
        clip_on=False,
    )
    ax.grid(which="major", axis="y", visible=False)

    # make all but left spine invisible
    makePatchSpinesInvisible(ax, ["top", "right", "bottom"])

    # Set axis default params
    setBarXAxisParams(ax, side="top")
    setBarYAxisParams(ax)
    replaceAxesMinusGlyphs(ax)

    # Set color of data series
    setBoxColor(ax, color=color_map["web_all"]["blue"])
    setLineColor(ax, color=color_map["web_all"]["blue"])

    return ax
