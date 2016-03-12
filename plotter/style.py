# plotter/style.py

import ROOT

colourdict = {
    'black':       ROOT.kBlack,
    'orange':      '#E24A33',
    'purple':      '#7A68A6',
    'blue':        '#348ABD',
    'lblue':       '#68add5',
    'turquoise':   '#188487',
    'red':         '#A60628',
    'pink':        '#CF4457',
    'green':       '#467821',
    'yellow':      '#e2a233',
    'lyellow':     '#f7fab3',
    'grey':        '#838283',
    'gray':        '#838283',
}

def get_color(c):

    if not isinstance(c, str):
        return c

    if c.startswith('#'):
        colour = ROOT.TColor.GetColor(c)
    else:
        try:
            colour = ROOT.TColor.GetColor(colourdict[c])
        except KeyError:
            if '+' in c:
                col, n = c.split('+')
                colour = getattr(ROOT, col)
                colour += int(n)
            elif '-' in c:
                col, n = c.split('-')
                colour = getattr(ROOT, col)
                colour -= int(n)
            else:
                colour = getattr(ROOT, c)

    return colour


def set_color(obj, color, fill=False, alpha=None):
    color = get_color(color)
    obj.SetLineColor(color)
    obj.SetMarkerColor(color)
    if fill:
        if alpha is not None:
            obj.SetFillColorAlpha(color, alpha)
        else:
            obj.SetFillColor(color)


def set_style(obj, color='kBlack'):

    # check if hist or graph
    is_hist = obj.InheritsFrom('TH1')

    # default
    obj.SetTitle('')
    if is_hist:
        obj.SetStats(0)

    # color
    set_color(obj, color) #, fill, alpha)

def set_palette():
    s = array('d', [0.00, 0.34, 0.61, 0.84, 1.00])
    r = array('d', [0.00, 0.00, 0.87, 1.00, 0.51])
    g = array('d', [0.00, 0.81, 1.00, 0.20, 0.00])
    b = array('d', [0.51, 1.00, 0.12, 0.00, 0.00])
    ROOT.TColor.CreateGradientColorTable(len(s), s, r, g, b, 999)
    ROOT.gStyle.SetNumberContours(999)

def set_default_style():
    set_palette()
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameBorderSize(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetTitleFillColor(0)
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetLabelFont(42,"XY")
    ROOT.gStyle.SetTitleFont(42,"XY")
    ROOT.gStyle.SetEndErrorSize(0)

# colours
default_colours = [
    'black',
    'red',
    'blue',
    'green',
    'yellow',
    'magenta',
    'orange',
]
