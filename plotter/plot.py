# plotter
# plot.py

import ROOT

# colours for the dict
colors = [
    '#E24A33',
    '#E24A33',
    '#32b45d',
    '#f7fab3',
    '#7A68A6',
    '#a4cee6',
    '#348ABD',
    '#348ABD',
    '#BCBC93',
    '#36BDBD',
    '#a4cee6',
    '#32b45d',
    ]

# plots configuration
class PlotConf(object):
    def __init__(self, xtitle, ytitle, legpos, xmin=None, xmax=None):
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.legpos = legpos
        self.xmin = xmin
        self.xmax = xmax

plots_conf = dict()
plots_conf['cuts']            = PlotConf('', 'Events', 'right')
plots_conf['ph_n']            = PlotConf('Number of photons', 'Events', 'right')
plots_conf['el_n']            = PlotConf('Number of electrons', 'Events', 'right')
plots_conf['jet_n']           = PlotConf('Number of jets', 'Events', 'right')
plots_conf['ph_pt']           = PlotConf('p_{T}^{#gamma} [GeV]', 'Events / (BIN GeV)', 'right')
plots_conf['ph_eta']          = PlotConf('Photon #eta', 'Events / (BIN GeV)', 'right')
plots_conf['ph_phi']          = PlotConf('Photon #phi', 'Events / (BIN GeV)', 'right')
plots_conf['ph_iso']          = PlotConf('Isolation (Etcone20) [GeV]', 'Events (1/BIN GeV)', 'right')
plots_conf['met_et']          = PlotConf('E_{T}^{miss} [GeV]', 'Events / (BIN GeV)', 'right', 0, 500)
plots_conf['met_phi']         = PlotConf('#phi^{miss}', 'Events', 'right')
plots_conf['ht']              = PlotConf('H_{T} [GeV]', 'Events / (BIN GeV)', 'right')
plots_conf['jet_pt']          = PlotConf('Jet p_{T} [GeV]', 'Events / (BIN GeV)', 'right')
plots_conf['jet_pt[0]']       = PlotConf('Jet1 p_{T} [GeV]', 'Events / (BIN GeV)', 'right')
plots_conf['jet_pt[1]']       = PlotConf('Jet2 p_{T} [GeV]', 'Events / (BIN GeV)', 'right')
plots_conf['jet_eta']         = PlotConf('Jet #eta', 'Events', 'right')
plots_conf['rt2']             = PlotConf('R_{T}^{2}', 'Events', 'left', 0.3, 1.1)
plots_conf['rt4']             = PlotConf('R_{T}^{4}', 'Events / BIN', 'left', 0.3, 1.05)
plots_conf['dphi_jetmet']     = PlotConf('#Delta#phi(jet^{1,2}, E_{T}^{miss})', 'Events', 'right')
plots_conf['dphi_jetmet_alt'] = PlotConf('#Delta#phi(jet^{1..4}, E_{T}^{miss})', 'Events', 'right')
plots_conf['dphi_jet1met']    = PlotConf('#Delta#phi(j^{1}, E_{T}^{miss})', 'Events', 'right')
plots_conf['dphi_jet2met']    = PlotConf('#Delta#phi(j^{2}, E_{T}^{miss})', 'Events', 'right')
plots_conf['dphi_jet3met']    = PlotConf('#Delta#phi(j^{3}, E_{T}^{miss})', 'Events', 'right')
plots_conf['dphi_gamjet']     = PlotConf('#Delta#phi(#gamma, jet)', 'Events', 'right')
plots_conf['dphi_gammet']     = PlotConf('#Delta#phi(#gamma, E_{T}^{miss})', 'Events', 'right')

plots_conf['default'] = PlotConf('','', 'right')


def draw_significance(canvas, h_obs, h_exp):

        ratio = histogram_equal_to(h_obs)

        canvas.cd()
        ratio.SetTitle('')
        ratio.SetStats(0)
        ratio.SetMarkerStyle(20)
        ratio.SetMarkerSize(1)
        ratio.SetLineWidth(2)
        ratio.SetLineColor(ROOT.kBlack)
        ratio.SetMarkerColor(ROOT.kBlack)
        ratio.SetFillColor(ROOT.kGray)

        # x axis
        ratio.GetXaxis().SetTitle(xtitle)
        if xmin is not None and xmax is not None:
            ratio.GetXaxis().SetRangeUser(xmin, xmax)
        ratio.GetXaxis().SetLabelSize(ratio_xlabel_size)
        ratio.GetXaxis().SetTitleSize(ratio_xtitle_size)
        ratio.GetXaxis().SetTitleOffset(1.2)
        ratio.GetXaxis().SetLabelOffset(0.03)
        ratio.GetXaxis().SetTickLength(0.06)

        if ratio.GetXaxis().GetXmax() < 5.:
            ratio.GetXaxis().SetNdivisions(512)
        else:
            ratio.GetXaxis().SetNdivisions(508)

        # y axis
        ratio.GetYaxis().SetTitle('Significance')
        ratio.GetYaxis().SetLabelSize(ratio_ylabel_size)
        ratio.GetYaxis().SetTitleSize(ratio_ytitle_size)
        ratio.GetYaxis().SetRangeUser(-5, 5)
        ratio.GetYaxis().SetNdivisions(504)
        ratio.GetYaxis().SetTitleOffset(0.4)
        ratio.GetYaxis().SetLabelOffset(0.01)

        for bx in xrange(ratio.GetNbinsX()):

            obs = h_obs.GetBinContent(bx+1)
            exp = h_exp.GetBinContent(bx+1)

            z = poisson_significance(obs, exp)

            ratio.SetBinContent(bx+1, z)

        ratio.Draw('e0')

        firstbin = ratio.GetXaxis().GetFirst()
        lastbin  = ratio.GetXaxis().GetLast()
        xmax     = ratio.GetXaxis().GetBinUpEdge(lastbin)
        xmin     = ratio.GetXaxis().GetBinLowEdge(firstbin)

        lines = [
            ROOT.TLine(xmin,  0., xmax,  0.),
            ROOT.TLine(xmin, -3., xmax, -3.),
            ROOT.TLine(xmin,  3., xmax,  3.),
        ]

        lines[0].SetLineWidth(1)
        lines[0].SetLineStyle(2)
        lines[1].SetLineStyle(3)
        lines[2].SetLineStyle(3)

        lines[0].Draw()
        lines[1].Draw()
        lines[2].Draw()
        ratio.Draw('e0 same')

        ratio.GetYaxis().SetLabelSize(0.)

        x = xmin - ratio.GetBinWidth(1) * 0.5  #ROOT.gPad.GetUxmin()

        t = ROOT.TLatex()
        t.SetTextSize(0.15)
        t.SetTextAlign(32)
        t.SetTextAngle(0);

        y = ratio.GetYaxis().GetBinCenter(3)
        t.DrawLatex(x, y+0.5, '3')

        y = ratio.GetYaxis().GetBinCenter(-3)
        t.DrawLatex(x, y+0.5, '-3')


def draw_ratio(canvas, h_deno, h_nume):

        ratio = h_nume.Clone()
        ratio.Divide(h_deno)

        # remove the point from the plot if zero
        for b in xrange(ratio.GetNbinsX()):
            if ratio.GetBinContent(b+1) < 0.00001:
                ratio.SetBinContent(b+1, -1)

        canvas.cd()
        ratio.SetTitle('')
        ratio.SetStats(0)
        ratio.SetMarkerStyle(20)
        ratio.SetMarkerSize(1)
        ratio.SetLineWidth(2)
        ratio.SetLineColor(ROOT.kBlack)
        ratio.SetMarkerColor(ROOT.kBlack)

        # x axis
        ratio.GetXaxis().SetTitle(xtitle)
        if xmin is not None and xmax is not None:
            ratio.GetXaxis().SetRangeUser(xmin, xmax)
        ratio.GetXaxis().SetLabelSize(ratio_xlabel_size)
        ratio.GetXaxis().SetTitleSize(ratio_xtitle_size)
        ratio.GetXaxis().SetTitleOffset(1.1)
        ratio.GetXaxis().SetLabelOffset(0.03)
        ratio.GetXaxis().SetTickLength(0.06)

        if ratio.GetXaxis().GetXmax() < 5.:
            ratio.GetXaxis().SetNdivisions(512)
        else:
            ratio.GetXaxis().SetNdivisions(508)

        # y axis
        ratio.GetYaxis().SetTitle('Data / SM')
        ratio.GetYaxis().SetLabelSize(ratio_ylabel_size)
        ratio.GetYaxis().SetTitleSize(ratio_ytitle_size)
        ratio.GetYaxis().SetRangeUser(0, 2.2)
        ratio.GetYaxis().SetNdivisions(504)
        ratio.GetYaxis().SetTitleOffset(0.4)
        ratio.GetYaxis().SetLabelOffset(0.01)
        ratio.GetYaxis().CenterTitle()

        err_band_stat = ROOT.TGraphAsymmErrors(ratio.GetNbinsX())
        err_band_all  = ROOT.TGraphAsymmErrors(ratio.GetNbinsX())

        for bin_ in xrange(ratio.GetNbinsX()):

            x    = h_deno.GetBinCenter(bin_+1)
            xerr = h_deno.GetBinWidth(bin_+1)/2

            sm_y     = h_deno.GetBinContent(bin_+1)

            sm_all_high = h_deno_all.GetBinError(bin_+1)
            sm_all_low  = h_deno_all.GetBinError(bin_+1)

            try:
                all_low  = sm_all_low/sm_y
            except ZeroDivisionError:
                all_low = 0.0

            try:
                all_high = sm_all_high/sm_y
            except ZeroDivisionError:
                all_high = 0.0

            err_band_all.SetPoint(bin_, x, 1.)
            err_band_all.SetPointError(bin_, xerr, xerr, all_low, all_high)


        err_band_all.SetMarkerSize(0)
        err_band_all.SetFillStyle(sm_total_style)
        err_band_all.SetLineColor(sm_syst_color)
        err_band_all.SetFillColor(sm_syst_color)
        err_band_all.SetLineWidth(2)

        ratio.Draw()
        err_band_all.Draw('P2same')
        ratio.Draw('same e0')

        firstbin = ratio.GetXaxis().GetFirst()
        lastbin  = ratio.GetXaxis().GetLast()
        xmax     = ratio.GetXaxis().GetBinUpEdge(lastbin)
        xmin     = ratio.GetXaxis().GetBinLowEdge(firstbin)

        lines = [
            ROOT.TLine(xmin, 1., xmax, 1.),
            ROOT.TLine(xmin, 0.5,xmax, 0.5),
            ROOT.TLine(xmin, 1.5,xmax, 1.5),
        ]

        lines[0].SetLineWidth(1)
        lines[0].SetLineStyle(2)
        lines[1].SetLineStyle(3)
        lines[2].SetLineStyle(3)

        for line in lines:
            line.Draw()



class Plot:

    number_of_plot = 0

    def __init__(self):

        self.name = 'plot_%d' % Plot.number_of_plot

        self.canvas = None
        self.legend = None

        self.objects = []
        self.labels = []

        self.logx = False
        self.logy = False

        Plot.number_of_plot = Plot.number_of_plot + 1

    # @classmethod
    # def get_number_of_plots(cls):
    #     return cls.number_of_plot

    def __del__(self):
        del self.canvas
        del self.legend

    def add(self, obj, colour, opts='', label=''):
        # set_style(obj, colour)

        # obj.SetOption(drawopts)

        self.objects.append(obj.Clone(obj.GetName()))

        if not label:
            label = obj.GetName()
        self.labels.append(label)

    def save(self):
        if self.canvas or not self.canvas.IsOnHeap():
            return
        self.canvas.Print(self.name + '.pdf')

    def dump(self):
        # (items_sel[k]->GetFile(), items_sel[k]->GetName(), items_sel[k]->GetText())
        # temp->SetDrawOptions(lnk->GetOption())
        # temp->SetColour(colours[k])
        # Int_t rebin = nentryRebin->GetIntNumber()
        # if(rebin > 1) temp->SetRebinNumber(nentryRebin->GetIntNumber())
        # if(checkNormalise->GetState() ) temp->SetScaleFactor(1/h->Integral())
        # if(checkNormalise2->GetState()) temp->SetScaleFactor(((TH1*)plot_list->At(0))->Integral()/h->Integral())
        # //        macro->AddHisto(temp)
        pass


    def create(self):

        do_ratio = False
        logy = False

        # try to guess variable
        names = [ obj.GetName() for obj in self.objects ]

        variable = names[0]

        if variable not in plots_conf:
            vartmp = variable[:variable.find('[')]
            conf = plots_conf.get(vartmp, plots_conf['default'])
        else:
            conf = plots_conf.get(variable, plots_conf['default'])

        xtitle = conf.xtitle
        ytitle = conf.ytitle
        xmin   = conf.xmin
        xmax   = conf.xmax
        legpos = conf.legpos


        self.canvas = ROOT.TCanvas(self.name, self.name, 600, 600)
        ROOT.SetOwnership(self.canvas, False)

        self.canvas.cd()

        if do_ratio:

            cup   = ROOT.TPad("u", "u", 0., 0.305, 0.99, 1)
            cdown = ROOT.TPad("d", "d", 0., 0.01, 0.99, 0.295)

            cup.SetRightMargin(0.03)
            cup.SetBottomMargin(0.005)
            cup.SetLeftMargin(0.15)

            cdown.SetLeftMargin(0.15)
            cdown.SetRightMargin(0.03)
            cdown.SetBottomMargin(0.37)
            cdown.SetTopMargin(0.0054)


            cup.SetTickx()
            cup.SetTicky()
            cdown.SetTickx()
            cdown.SetTicky()
            cdown.SetFillColor(ROOT.kWhite)
            cup.Draw()
            cdown.Draw()


            if logy:
                cup.SetLogy()

        else:
            if logy:
                can.SetLogy()


        # configure histograms
        # for name, hist in bkg.iteritems():
        #     set_style(hist, color=colors_dict[name], fill=True)
        #     hist.SetLineColor(ROOT.kBlack)


        # stack
        #         # create SM stack
        # sm_stack = ROOT.THStack()

        # def _compare(a, b):
        #     amax = a.GetMaximum()
        #     bmax = b.GetMaximum()
        #     return cmp(int(amax), int(bmax))

        # for hist in sorted(bkg.itervalues(), _compare):
        #     sm_stack.Add(hist)

        # add entries to legend
        if do_ratio:
            legymin = 0.60
            legymax = 0.88

            if legpos == 'left':
                legxmin = 0.20
                legxmax = 0.53
            elif legpos == 'right':
                legxmin = 0.55
                legxmax = 0.91
        else:
            legymin = 0.80
            legymax = 0.94

            if legpos == 'left':
                legxmin = 0.20
                legxmax = 0.53
            elif legpos == 'right':
                legxmin = 0.65
                legxmax = 0.92

        legend1 = ROOT.TLegend(legxmin, legymin, legxmax, legymax)
        legend2 = ROOT.TLegend(legxmin, legymin-.15, legxmax-0.035, legymin -.01)

        for obj in self.objects:
            legend1.AddEntry(obj, obj.GetName(), 'f')


        if do_ratio:
            cup.cd()

        # first histogram to configure (ROOT de mierda)
        chist = self.objects[0]

        if xmin is not None and xmax is not None:
            chist.GetXaxis().SetRangeUser(xmin, xmax)

        if chist.GetXaxis().GetXmax() < 5.:
            chist.GetXaxis().SetNdivisions(512)
        else:
            chist.GetXaxis().SetNdivisions(508)


        if do_ratio:
            cup.RedrawAxis()
        else:
            self.canvas.RedrawAxis()

        chist.SetMinimum(0.01)

        if logy:
            chist.SetMaximum(chist.GetMaximum()*1000)

        # Titles and labels
        chist.GetXaxis().SetTitle(xtitle)
        chist.GetXaxis().SetTitleOffset(1.40)
        chist.GetXaxis().SetLabelSize(0.)

        # chist.GetXaxis().SetLabelSize(up_size*1.17)
        # chist.GetXaxis().SetTitleSize(up_size*1.17)

        # chist.GetYaxis().SetLabelSize(up_size*1.17)
        # chist.GetYaxis().SetTitleSize(up_size*1.17)

        if 'BIN' in ytitle:
            width = chist.GetBinWidth(1)

            if width > 10:
                ytitle = ytitle.replace('BIN', '{:.0f}'.format(width))
            else:
                ytitle = ytitle.replace('BIN', '{:.2f}'.format(width))

        chist.GetYaxis().SetTitle(ytitle)
        chist.GetYaxis().SetTitleOffset(1.1)

        # if data:
        # data_graph = make_poisson_cl_errors(data)

        # set_style(data_graph, msize=1, lwidth=2, color=ROOT.kBlack)

        #data_graph.Draw('P0Z')
        #data.Draw("P same")


        chist.Draw()

        for obj in self.objects[1:]:
            obj.Draw('same')

        if do_ratio:
            cup.RedrawAxis()
        else:
            self.canvas.RedrawAxis()

        legend1.Draw()
        legend2.Draw()


        pass
