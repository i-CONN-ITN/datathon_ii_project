##################################################################################################################
# Helper function to plot panels.
# Author: Viktor Sip (https://github.com/sipv)
# Repository: https://github.com/sipv/MultipanelFigures
##################################################################################################################
import itertools

import matplotlib
import matplotlib.pyplot as plt
import numpy             as np

from   matplotlib import lines

def set_plot_config():
    # Set font sizes
    # https://stackoverflow.com/a/39566040/13392466

    SMALL_SIZE  = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12

    plt.rc('font',   size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes',   titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes',   labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick',  labelsize=SMALL_SIZE)     # fontsize of the tick labels
    plt.rc('ytick',  labelsize=SMALL_SIZE)     # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)      # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)    # fontsize of the figure title

    return SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE

"Function from https://gist.github.com/salotz/8b4542d7fe9ea3e2eacc1a2eef2532c5"
def move_axes(ax, fig, subplot_spec=111):
  """Move an Axes object from a figure to a new pyplot managed Figure in
  the specified subplot."""

  # get a reference to the old figure context so we can release it
  old_fig = ax.figure

  # remove the Axes from it's original Figure context
  ax.remove()

  # set the pointer from the Axes to the new figure
  ax.figure = fig

  # add the Axes to the registry of axes for the figure
  fig.axes.append(ax)
  # twice, I don't know why...
  fig.add_axes(ax)

  # then to actually show the Axes in the new figure we have to make
  # a subplot with the positions etc for the Axes to go, so make a
  # subplot which will have a dummy Axes
  dummy_ax = fig.add_subplot(subplot_spec)

  # then copy the relevant data from the dummy to the ax
  ax.set_position(dummy_ax.get_position())

  # then remove the dummy
  dummy_ax.remove()

  # close the figure the original axis was bound to
  plt.close(old_fig)

class Background():
    def __init__(self, fig=None, visible=False, spacing=0.1, linecolor='0.5', linewidth=1):
        if fig is not None:
            plt.scf(fig)
        ax = plt.axes([0,0,1,1], facecolor=None, zorder=-1000)
        plt.xticks(np.arange(0, 1 + spacing/2., spacing))
        plt.yticks(np.arange(0, 1 + spacing/2., spacing))
        plt.grid()
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        ax.autoscale(False)
        if not visible:
            plt.axis('off')
        self.axes = ax
        self.linecolor = linecolor
        self.linewidth = linewidth

    def vline(self, x, y0=0, y1=1, **args):
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x, x], [y0, y1], **defargs))

    def hline(self, y, x0=0, x1=1, **args):
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x0, x1], [y, y], **defargs))
        
    def labels(self, xs, ys, fontsize=18):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        assert len(xs) == len(ys)
        for x, y, letter in zip(xs, ys, letters):
            self.axes.text(x, y, letter, transform=self.axes.transAxes, size=fontsize, 
                           weight='bold', ha='left', va='bottom')

    def box(self, pos, title=None, titlestyle=None, pad=0.0, **args):
        """Draw a box with optional title.

        Args:
            pos:         (left, right, bottom, top) axes coordinates.
            title:       Optional box title.
            titlestyle:  Dict with arguments passed to plt.text().
            pad:         Padding size in axes coordinates.
        """

        plt.sca(self.axes)
        width = pos[1] - pos[0]
        height = pos[3] - pos[2]

        defargs = dict(ec=self.linecolor, linewidth=self.linewidth, fc='none')
        defargs.update(args)

        fancy = matplotlib.patches.FancyBboxPatch((pos[0], pos[2]), width, height,
                                                  boxstyle=f"round,pad={pad}", **defargs)
        self.axes.add_patch(fancy)

        if title:
            titleargs = dict(ha='left', va='center', backgroundcolor='w',
                             color=self.linecolor, fontsize=12)
            if titlestyle is not None:
                titleargs.update(titlestyle)

            plt.text(pos[0]+0.02, pos[3]+pad, title, **titleargs)

def add_panel_letters(fig, axes=None, fontsize=18, xpos=-0.04, ypos=1.05):
    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if axes is None:
        axes = fig.get_axes()

    if type(xpos) == float:
        xpos = itertools.repeat(xpos)
    if type(ypos) == float:
        ypos = itertools.repeat(ypos)

    for i, (ax, x, y) in enumerate(zip(axes, xpos, ypos)):
        ax.text(x, y, labels[i],
                transform=ax.transAxes, size=fontsize, weight='bold')


def axtext(ax, text, **args):
    defargs = {'fontsize': 14, 'ha': 'center', 'va': 'center'}
    defargs.update(args)
    plt.text(0.5, 0.5, text, **defargs)
    plt.xlim([0, 1]); plt.ylim([0, 1])
    plt.axis('off')


def box_rounded(ax, pos, title=None, pad=0.0):
    """Draw a box with rounded corner around a gridspec
    pos: (left, right, bottom, top)
    """

    plt.sca(ax)
    width = pos[1]-pos[0]
    height = pos[3]-pos[2]
    fancy = matplotlib.patches.FancyBboxPatch((pos[0], pos[2]), width, height,
                                              fc='none', ec='0.4', boxstyle=f"round,pad={pad}")
    ax.add_patch(fancy)

    if title:
        plt.text(pos[0]+0.02, pos[3]+pad, title, ha='left', va='center', backgroundcolor='w',
                 color='0.4', fontsize=8)

def axbottomleft(ax):
    """Hide the right and top spines
    
    https://stackoverflow.com/a/27361819/13392466
    """
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
