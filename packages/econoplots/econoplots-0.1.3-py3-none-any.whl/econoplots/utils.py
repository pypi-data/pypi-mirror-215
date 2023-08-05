"""Utilities."""
# Imports
from __future__ import annotations

# Standard Library Imports
import importlib.resources
import json
from itertools import cycle
from typing import Tuple

# Third Party Imports
from matplotlib import pyplot as plt  # noqa
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from matplotlib.text import Text
from matplotlib.ticker import AutoMinorLocator, FixedLocator
from numpy import (
    absolute,
    append,
    intersect1d,
    logical_and,
    max,
    min,
    nanmax,
    nanmin,
    ndarray,
    where,
)
from numpy.ma import MaskedArray, getdata

# %% Functions


def loadColorMap() -> dict:
    with importlib.resources.open_text("econoplots", "color_map.json") as file:
        color_map = json.load(file)
    return color_map


def makePatchSpinesInvisible(
    ax: Axis,
    list_of_spines: list[str] = None,
) -> None:
    """Makes spine(s) of axis invisible.

    Args:
        ax (Axis): A matplotlib Axis
        list_of_spines (list[str], optional): Entries can be any
            combination of 'top', 'bottom', 'left', or 'right'. Spines in ax
            associated with list_of_spines will be made invisible. If None,
            then all spines will be made invisible. Defaults to None.
    """
    if list_of_spines is None:
        list_of_spines = ["top", "bottom", "left", "right"]
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in list_of_spines:
        ax.spines[sp].set_visible(False)

    return


def replaceAxesMinusGlyphs(ax: Axes) -> None:
    """Replace x- and y-axes minus signs with hyphens."""
    inbound_locs, inbound_indx = getInBoundsTickPos(ax)
    x_locs_inbound = inbound_locs[0]
    y_locs_inbound = inbound_locs[1]
    x_indx_inbound = inbound_indx[0]
    y_indx_inbound = inbound_indx[1]

    # Loop through in-range x and y tick labels. Use only in-range labels so that
    # when using ax.set_[x/y]ticks() we don't expand the axes limits beyond what
    # is already set.
    x_labels = []
    tick_labels = ax.xaxis.get_ticklabels()[
        x_indx_inbound[0] : x_indx_inbound[-1] + 1
    ]
    for tl in tick_labels:
        x_labels.append(replaceMinusWithHyphen(tl))
    ax.set_xticks(x_locs_inbound, x_labels)

    y_labels = []
    tick_labels = ax.yaxis.get_ticklabels()[
        y_indx_inbound[0] : y_indx_inbound[-1] + 1
    ]
    for tl in tick_labels:
        y_labels.append(replaceMinusWithHyphen(tl))
    ax.set_yticks(y_locs_inbound, y_labels)

    return


def setLineYAxisParams(
    ax: Axes,
    side: str,
    label_location: str,
) -> None:
    """Set y-axis side, label, tick label location and style.

    Args:
        ax (Axes): _description_
        side (str): "left" or "right
    """
    color_map = loadColorMap()

    # Set axis parameters based on which side axis is on
    tick_side_params = getTickLabelSideParams(side=side)

    # set extra pad and horizontal alignment for tick labels
    if side == "right":
        ha = "right"
        left_right_pad = -2
    elif side == "left":
        ha = "left"
        left_right_pad = -2

    # Set tick parameters
    ax.yaxis.set_tick_params(
        pad=left_right_pad,  # Pad tick labels so they don't go over y-axis
        colors=color_map["grid"]["grid_gray"],  # set tick color to same as grid
        labelcolor="black",  # set tick label color
        **tick_side_params,
    )

    # ax.ticklabel_format(ScalarFormatter)

    # Set tick label parameters
    # NOTE: Move labels after moving axis.
    # set vertical alignment on y-axis tick labels to be on top of of major
    # ticks. Set horizontal alignment to right (this part not necessary)
    for label in ax.yaxis.get_ticklabels():
        label.set_verticalalignment("bottom")
        label.set_horizontalalignment(ha)

    # Move yaxis label to upper-left or -right
    relocateYAxisLabel(ax, side=label_location)

    return


def setLineXAxisParams(
    ax: Axes,
    pad_side: str,
    minor_ticks_on: bool = True,
    n_minortick_subdivisions: int = None,
):
    """Set x-axis padding, label, tick label location and style.

    Args:
        ax (Axes): _description_
        pad_side (str): Which side(s) to add padding to. Axis is always shown on
            bottom of plot.
        minor_ticks_on (bool, optional): Whether or not to plot minor tick marks.
            Defaults to True.
        n_minortick_subdivisions (int, optional): Number of minor ticks between
            major ticks. Defaults to None, which automatically determines number.
    """
    # Add empty space to x-axis to give space between y-tick labels and plotted
    # data. Do this BEFORE other operations, as resizing can mess up tick marks.
    padXAxis(ax, side=pad_side)

    # Set Major ticks. Make major ticks that are wider than span of the data invisible.
    makeOutOfRangeXTicksInvisible(ax)

    if minor_ticks_on is True:
        # Turn on minor ticks and set frequency between major ticks
        addInnerMinorTicks(ax, n_minortick_subdivisions)

    # Add minor tick(s) if outer limits of data are NOT on major ticks. Unlike
    # minor ticks that are in-between major ticks, the outer minor ticks are not
    # optional.
    addOuterMinorTicks(ax)

    return


def setBarXAxisParams(ax: Axes, side: str) -> Axes:
    """Set default x-axis params for a bar chart.

    Args:
        ax (Axes): _description_
        side (str): ["top" | "bottom"] Which side the x-axis should be on.

    Returns:
        Axes: _description_
    """
    color_map = loadColorMap()

    # Get params to set positions for ticks and tick labels
    tick_side_params = getTickLabelSideParams(side=side)

    if side == "bottom":
        axis_label_pos = "bottom"
    elif side == "top":
        axis_label_pos = "top"

    ax.xaxis.set_tick_params(
        colors=color_map["grid"]["grid_gray"],  # set tick color to same as grid
        labelcolor="black",  # set tick label color
        length=0,  # set tick lengths to 0 to align with spine
        **tick_side_params,
    )

    # Move x-axis label to top
    ax.xaxis.set_label_position(axis_label_pos)

    return ax


def setBarYAxisParams(ax: Axes) -> Axes:
    ax.yaxis.set_tick_params(length=0)

    # TODO: Move ytick label baseline to left of plot area and align to left.
    for label in ax.yaxis.get_ticklabels():
        label.set_verticalalignment("center")
        label.set_horizontalalignment("right")

    return ax


def getTickLabelSideParams(side: str) -> dict:
    """Get params to set tick label position for use in Axis.set_tick_params.

    Args:
        side (str): ["bottom" | "top" | "left" | "right"]

    Returns:
        dict: Can be used as kwarg to Axis.set_tick_params(**kwargs)
    """
    # See https://matplotlib.org/stable/api/_as_gen/matplotlib.axis.Axis.get_tick_params.html#matplotlib.axis.Axis.get_tick_params  # noqa

    # bottom, top, left, right: bool
    #   Whether to draw the respective ticks.
    # labelbottom, labeltop, labelleft, labelright: bool
    #   Whether to draw the respective tick labels

    if side == "bottom":
        tick_label_side = {
            "labelbottom": True,
            "labeltop": False,
            "bottom": True,
            "top": False,
        }
    elif side == "top":
        tick_label_side = {
            "labelbottom": False,
            "labeltop": True,
            "bottom": False,
            "top": True,
        }
    elif side == "right":
        tick_label_side = {
            "labelright": True,
            "labelleft": False,
            "right": True,
            "left": False,
        }
    elif side == "left":
        tick_label_side = {
            "labelright": False,
            "labelleft": True,
            "right": False,
            "left": True,
        }

    return tick_label_side


def addInnerMinorTicks(ax: Axes, n_minortick_subdivisions: int | None):
    """Add minor ticks to x axis within data limits."""
    ax.xaxis.set_minor_locator(AutoMinorLocator(n_minortick_subdivisions))

    # Remove minor ticks that are beyond data range.
    x_lims, _ = getDataLimits(ax)
    # min_major_tick_loc = ax.xaxis.get_majorticklocs()[1]
    # max_major_tick_loc = ax.xaxis.get_majorticklocs()[-2]
    minor_tick_locs = ax.xaxis.get_minorticklocs()
    minor_tick_locs = minor_tick_locs[minor_tick_locs > x_lims[0]]
    minor_tick_locs = minor_tick_locs[minor_tick_locs < x_lims[1]]
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))
    return


def makeOutOfRangeXTicksInvisible(ax: Axes):
    """Make major ticks that are < or > data range invisible."""
    major_tick_locs = ax.xaxis.get_majorticklocs()
    xticks = ax.xaxis.get_major_ticks()
    xlims, _ = getDataLimits(ax)
    visibility = list(major_tick_locs > xlims[0])

    for tick, vis in zip(xticks, visibility):
        tick.set_visible(vis)
    visibility = list(major_tick_locs < xlims[1])
    for tick, vis in zip(xticks, visibility):
        tick.set_visible(vis)

    return


def addOuterMinorTicks(ax: Axes):
    """Add minor ticks to data limits if major ticks don't already cover limits."""
    major_locs = [b.get_loc() for b in ax.xaxis.get_major_ticks()]
    minor_tick_locs = ax.xaxis.get_minorticklocs()

    # Get locations to add new minor ticks. Add new ticks if existing major ticks
    # don't overlap with outer limits of data.
    x_lim, _ = getDataLimits(ax)
    new_locs = []
    for x in x_lim:
        if x not in major_locs:
            new_locs.append(x)
    num_new_locs = len(new_locs)

    # Append new minor ticks to existing minor ticks.
    minor_tick_locs = append(minor_tick_locs, new_locs)
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))

    # Refresh minor tick locs because special case where adding minor tick close
    # to major tick causes minor tick to not be added. This step is needed to prevent
    # an error.
    num_minor_ticks_attempted = len(minor_tick_locs)
    minor_tick_locs = ax.xaxis.get_minorticklocs()
    ax.xaxis.set_minor_locator(FixedLocator(minor_tick_locs))

    if num_minor_ticks_attempted != len(minor_tick_locs):
        # Par down the list of new minor tick locations if matplotlib rejected
        # additions.
        print("Different number of minor ticks added than attempted.")
        new_locs = intersect1d(minor_tick_locs, new_locs)
        num_new_locs = len(new_locs)

    # Create labels for new minor ticks and set minor tick labels
    minor_labels = [item.get_text() for item in ax.get_xticklabels(minor=True)]
    num_minor_labels = len(minor_labels)
    for i, lab in enumerate(new_locs, num_minor_labels - num_new_locs):
        # new labels are at end of minor_labels list
        text = "%.0f" % lab
        minor_labels[i] = text

    # TODO: Make the format of the added minor ticks match the format of the major
    # ticks.
    ax.set_xticks(minor_tick_locs, minor_labels, minor=True)

    return


def padXAxis(
    ax: Axes,
    side: str,
) -> Axes:
    """Add extra space on both sides of the x-axis.

    Adds 15% padding on the input side, and 5% padding on the opposite side. If
    "both" sides are selected, adds 15% padding to both sides.

    Args:
        ax (Axes): _description_
        side (str): "left" | "right" | "both"

    Returns:
        Axes: _description_
    """
    # Get real bounds of x-axis data (not x-axis limits, which are wider than data)
    x_lims, _ = getDataLimits(ax)

    # get axis pad amount
    x_ax_pad = 0.15 * absolute(x_lims[1] - x_lims[0])
    x_ax_minor_pad = 0.33 * x_ax_pad

    if side == "left":
        # set x-axis max limit to tighter than default and with extra room on left
        ax.set_xlim(
            [
                x_lims[0] - x_ax_pad,
                x_lims[1] + x_ax_minor_pad,
            ]
        )

    if side == "right":
        ax.set_xlim(
            [
                x_lims[0] - x_ax_minor_pad,
                x_lims[1] + x_ax_pad,
            ]
        )

    if side == "both":
        ax.set_xlim(
            [
                x_lims[0] - x_ax_pad,
                x_lims[1] + x_ax_pad,
            ]
        )

    # NOTE: This adjustment seems to have not been necessary, but keeping here
    # in case issue crops up again.
    # Changing plot size changes tick labels in incorrect ways, so re-initialize
    # tick labels
    # ax.set_xticks(ax.xaxis.get_majorticklocs()[1:-2])

    return ax


def getDataLimits(ax: Axes) -> Tuple[list, list]:
    """Get x and y limits of data in ax (different from axis limits).

    Args:
        ax (Axes): _description_

    Returns:
        x_lims(list): x data limits [min, max]
        y_lims(list): y data limits [min, max]
    """
    x_lims = [0, 0]
    y_lims = [0, 0]
    lines = ax.get_lines()
    if len(lines) == 0:
        # If plot is a patch plot (no lines)
        patches = getAxPatches(ax)
        # TODO: Fill in this part
    else:
        for line in lines:
            xdat = line.get_xdata()
            ydat = line.get_ydata()

            # extract data from MaskedArrays
            if isinstance(xdat, MaskedArray):
                xdat = getdata(xdat)
            if isinstance(ydat, MaskedArray):
                ydat = getdata(ydat)

            # Use min/max with default values to account for 'empty' lines, which can
            # occur in box plots.
            min_x = nanmin(xdat, initial=x_lims[0])
            max_x = nanmax(xdat, initial=x_lims[1])
            min_y = nanmin(ydat, initial=y_lims[0])
            max_y = nanmax(ydat, initial=y_lims[1])

            if min_x < x_lims[0]:
                x_lims[0] = min_x
            if max_x > x_lims[1]:
                x_lims[1] = max_x

            if min_y < y_lims[0]:
                y_lims[0] = min_y
            if max_y > y_lims[1]:
                y_lims[1] = max_y

    return x_lims, y_lims


def getAxPatches(ax: Axes) -> list[PolyCollection]:
    children = ax.get_children()
    patches = [child for child in children if isinstance(child, PolyCollection)]
    return patches


def getInBoundsTickPos(ax: Axes) -> Tuple[list[ndarray], list[ndarray]]:
    """Get major tick locations that are within axis limits.

    Args:
        ax (Axes): _description_

    Returns:
        locs (list[ndarray]): A two-entry list with x and y in-bounds major tick
            locations.
        indices (list[ndarray]): A two-entry list with the indices of the in-bounds
            major ticks.

    """
    # get axis limits
    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()

    xtick_locs = ax.xaxis.get_majorticklocs()
    ytick_locs = ax.yaxis.get_majorticklocs()

    # Get the indices and corresponding locs that are within the axis limits.
    x_inbounds_indx = where(
        logical_and(
            xtick_locs >= x_lim[0],
            xtick_locs <= x_lim[1],
        )
    )[0]
    y_inbounds_indx = where(
        logical_and(
            ytick_locs >= y_lim[0],
            ytick_locs <= y_lim[1],
        )
    )[0]

    xtick_locs_inbound = xtick_locs[
        x_inbounds_indx[0] : x_inbounds_indx[-1] + 1
    ]
    ytick_locs_inbound = ytick_locs[
        y_inbounds_indx[0] : y_inbounds_indx[-1] + 1
    ]

    return (
        [xtick_locs_inbound, ytick_locs_inbound],
        [x_inbounds_indx, y_inbounds_indx],
    )


def setDefaultLineColors(ax: Axes) -> Axes:
    """Sets colors of all lines in ax to default line chart colors.

    Args:
        ax (Axes): _description_

    Returns:
        Axes: _description_
    """
    color_map = loadColorMap()
    color_cycler = cycle(color_map["line_chart"])
    for line in ax.lines:
        line.set_color(next(color_cycler))

    return ax


def setDefaultPatchColors(ax: Axes) -> Axes:
    color_map = loadColorMap()
    color_cycler = cycle(color_map["line_chart"])

    children = ax.get_children()
    patches = [child for child in children if isinstance(child, PolyCollection)]
    for p in patches:
        col = next(color_cycler)
        p.set_facecolor(col)
        p.set_edgecolor(col)
    return ax


def relocateYAxisLabel(ax: Axes, side: str) -> Axes:
    """Move y-axis label to top of plot.

    Args:
        ax (Axes): _description_
        side (str): "left" or "right"

    Returns:
        Axes: _description_
    """
    ax.yaxis.label.set(rotation="horizontal")

    # Set label vertical alignment
    ax.yaxis.label.set_va("bottom")

    # TODO: Get max value of yticklabel, then place yaxis label above that. Will
    # be smarter than simply placing the yaxis label at an arbitrary location.
    # ytick_labels = ax.yaxis.get_majorticklabels()
    # ytick_label_locs = [label.get_position()[1] for label in ytick_labels]
    # get max visible ytick label location
    # top_label_loc = ytick_label_locs[-2]

    # Add a bit of white space between the bottom of the label and the top of the
    # axis.
    # y_label_pad = 0
    y_label_pad = 0.01
    # y_label_pad = 0.05

    if side == "left":
        # move label to upper-left and set horizontal alignment
        ax.yaxis.set_label_coords(0, 1 + y_label_pad)
        ax.yaxis.label.set_ha("left")
    elif side == "right":
        # move label to upper-right and set horizontal alignment
        ax.yaxis.set_label_coords(1, 1 + y_label_pad)
        ax.yaxis.label.set_ha("right")

    return ax


def setLegendParams(ax: Axes) -> Axes:
    """Set legend background and edge to white."""
    # Only change if a legend is already populated.
    leg = ax.get_legend()
    if leg is not None:
        # Set Alpha to fully opaque, set background to white, set edge to white
        leg.get_frame().set_alpha(1)
        leg.get_frame().set_facecolor("white")
        leg.get_frame().set_edgecolor("white")
    return ax


def changeLegendLines2Patches(ax: Axes) -> Axes:
    """Regenerates legend with lines to legend with patches."""
    leg = ax.get_legend()
    lines = leg.get_lines()
    colors = [line.get_color() for line in lines]
    labels = [line.get_label() for line in lines]
    patches = [
        Patch(facecolor=col, edgecolor=col, label=lab)
        for col, lab in zip(colors, labels)
    ]
    # get legend location and transform from pixel to data coords
    # plt.draw()
    # bbox = leg.get_window_extent()
    # leg_loc = ax.transData.inverted().transform([bbox.xmin, bbox.ymin])
    # recreate legend
    ax.legend(patches, labels)

    return ax


def updateLegendEntryColors(ax: Axes) -> Axes:
    """Change legend entry colors to match line/patch colors in plot."""
    leg = ax.get_legend()
    if leg is None:
        # Return early if ax doesn't have legend
        return ax

    # Change line colors
    leg_lines = leg.get_lines()
    plot_lines = ax.get_lines()
    for pline, lline in zip(plot_lines, leg_lines):
        new_color = pline.get_color()
        lline.set_color(new_color)

    # Change patch colors
    leg_patches = leg.get_patches()
    # Patches are not stored separately in ax (like lines are), so need to get
    # all children, then filter out from there.
    all_children = ax.get_children()
    patch_indices = where([isinstance(c, PolyCollection) for c in all_children])
    patch_children = [all_children[indx] for indx in list(*patch_indices)]
    for ppatch, lpatch in zip(patch_children, leg_patches):
        new_color = ppatch.get_facecolor()
        lpatch.set_facecolor(new_color)
        lpatch.set_edgecolor(new_color)

    return ax


def replaceMinusWithHyphen(text: Text) -> Text:
    """Replace all minus signs chr(8722) with hyphens chr(45)."""
    t = text._text
    text._text = t.replace(chr(8722), "-")
    return text


def setBoxColor(ax: Axes, color) -> Axes:
    """Set colors of patches in ax."""
    patches = ax.patches
    for p in patches:
        p.set_facecolor(color)
        p.set_edgecolor(color)

    return ax


def setLineColor(ax: Axes, color) -> Axes:
    """Set colors of lines in ax."""
    # Number of lines per data series varies depending on if flyers are present.
    # Need to know where median lines are, so we need to know number of lines per
    # series.
    lines = ax.get_lines()
    num_lines = len(lines)
    num_series = len(ax.yaxis.get_majorticklabels())
    lines_per_series = int(num_lines / num_series)

    # Change all line colors
    for _, line in enumerate(lines):
        line.set_color(color)

    # Change median lines color
    for i in range(num_series):
        line = lines[i * lines_per_series + 4]
        line.set_color("black")

    return ax


def fillArea(ax: Axes) -> Axes:
    """Replaces lines in ax with filled areas between y-values and 0."""
    lines = ax.get_lines()
    for line in lines:
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        color = line.get_color()
        poly = ax.fill_between(x_data, y_data, color=color)
        # By default the fill area is zorder=1, which puts it behind grid lines.
        # Move to zorder=2, which is same as default lines.
        poly.set_zorder(2)
        # Set line to invisible.
        line.set_linestyle("")

    return ax


def plotZeroPt(ax: Axes, marker_size: float) -> Axes:
    """Add a black dot marker at 0,0 on a plot."""
    ax.plot(
        0,
        0,
        marker=".",
        markersize=marker_size,
        markerfacecolor="black",
        markeredgecolor="black",
    )
    return ax


def nudgeBottomSpine(ax: Axes) -> Axes:
    """Align bottom spine with bottom major tick."""
    # only move spine if there is no data beneath bottom major tick
    major_tick_locs = ax.yaxis.get_majorticklocs()
    _, y_lims = getDataLimits(ax)
    if min(y_lims) >= min(major_tick_locs):
        ax.spines["bottom"].set_position(("data", min(major_tick_locs)))

    return ax
