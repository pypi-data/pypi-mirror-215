# -*- coding: utf-8 -*-

"""The ``backgroundpdf`` module contains possible background PDF models for the
likelihood function.
"""

from skyllh.core.pdf import (
    IsBackgroundPDF,
    MultiDimGridPDF,
    NDPhotosplinePDF,
    TimePDF,
)

import numpy as np


class BackgroundMultiDimGridPDF(MultiDimGridPDF, IsBackgroundPDF):
    """This class provides a multi-dimensional background PDF. The PDF is
    created from pre-calculated PDF data on a grid. The grid data is
    interpolated using a :class:`scipy.interpolate.RegularGridInterpolator`
    instance.
    """

    def __init__(
            self,
            axis_binnings,
            path_to_pdf_splinetable=None,
            pdf_grid_data=None,
            norm_factor_func=None):
        """Creates a new background PDF instance for a multi-dimensional PDF
        given as PDF values on a grid. The grid data is interpolated with a
        :class:`scipy.interpolate.RegularGridInterpolator` instance. As grid
        points the bin edges of the axis binning definitions are used.

        Parameters
        ----------
        axis_binnings : sequence of BinningDefinition
            The sequence of BinningDefinition instances defining the binning of
            the PDF axes. The name of each BinningDefinition instance defines
            the event field name that should be used for querying the PDF.
        path_to_pdf_splinetable : str
            The path to the file containing the spline table.
            The spline table contains a pre-computed fit to pdf_grid_data.
        pdf_grid_data : n-dimensional numpy ndarray
            The n-dimensional numpy ndarray holding the PDF values at given grid
            points. The grid points must match the bin edges of the given
            BinningDefinition instances of the `axis_binnings` argument.
        norm_factor_func : callable | None
            The function that calculates a possible required normalization
            factor for the PDF value based on the event properties.
            The call signature of this function
            must be `__call__(pdf, events, fitparams)`, where `pdf` is this PDF
            instance, `events` is a numpy record ndarray holding the events for
            which to calculate the PDF values, and `fitparams` is a dictionary
            with the current fit parameter names and values.
        """
        super(BackgroundMultiDimGridPDF, self).__init__(
            axis_binnings, path_to_pdf_splinetable, pdf_grid_data, norm_factor_func)


class BackgroundNDPhotosplinePDF(NDPhotosplinePDF, IsBackgroundPDF):
    """This class provides a multi-dimensional background PDF created from a
    n-dimensional photospline fit. The photospline package is used to evaluate
    the PDF fit.
    """

    def __init__(
            self,
            axis_binnings,
            param_set,
            path_to_pdf_splinefit,
            norm_factor_func=None):
        """Creates a new background PDF instance for a n-dimensional photospline
        PDF fit.

        Parameters
        ----------
        axis_binnings : BinningDefinition | sequence of BinningDefinition
            The sequence of BinningDefinition instances defining the binning of
            the PDF axes. The name of each BinningDefinition instance defines
            the event field name that should be used for querying the PDF.
        param_set : Parameter | ParameterSet
            The Parameter instance or ParameterSet instance defining the
            parameters of this PDF. The ParameterSet holds the information
            which parameters are fixed and which are floating (i.e. fitted).
        path_to_pdf_splinefit : str
            The path to the file containing the photospline fit.
        norm_factor_func : callable | None
            The function that calculates a possible required normalization
            factor for the PDF value based on the event properties.
            The call signature of this function must be
            `__call__(pdf, tdm, params)`, where `pdf` is this PDF
            instance, `tdm` is an instance of TrialDataManager holding the
            event data for which to calculate the PDF values, and `params` is a
            dictionary with the current parameter names and values.
        """
        super(BackgroundNDPhotosplinePDF, self).__init__(
            axis_binnings=axis_binnings,
            param_set=param_set,
            path_to_pdf_splinefit=path_to_pdf_splinefit,
            norm_factor_func=norm_factor_func
        )


class BackgroundUniformTimePDF(TimePDF, IsBackgroundPDF):

    def __init__(self, grl):
        """Creates a new background time PDF instance as uniform background

        Parameters
        ----------
        grl : ndarray
            Array of the detector good run list

        """
        super(BackgroundUniformTimePDF, self).__init__()
        self.start = grl["start"][0]
        self.end = grl["stop"][-1]
        self.grl = grl


    def cdf(self, t):
        """Compute the cumulative density function for the box pdf. This is
        needed for normalization.

        Parameters
        ----------
        t : float, ndarray
            MJD times

        Returns
        -------
        cdf : float, ndarray
            Values of cumulative density function evaluated at t
        """
        t_start = self.grl["start"][0]
        t_end = self.grl["stop"][-1]
        t = np.atleast_1d(t)

        cdf = np.zeros(t.size, float)

        # values between start and stop times
        mask = (t_start <= t) & (t <= t_end)
        cdf[mask] = (t[mask] - t_start) / [t_end - t_start]

        # take care of values beyond stop time in sample

        return cdf

    def norm_uptime(self):
        """Compute the normalization with the dataset uptime. Distributions like 
        scipy.stats.norm are normalized (-inf, inf).
        These must be re-normalized such that the function sums to 1 over the
        finite good run list domain.

        Returns
        -------
        norm : float
            Normalization such that cdf sums to 1 over good run list domain
        """

        integral = (self.cdf(self.grl["stop"]) - self.cdf(self.grl["start"])).sum()

        if np.isclose(integral, 0):
            return 0

        return 1. / integral

    def get_prob(self, tdm, fitparams=None, tl=None):
        """Calculates the background time probability density of each event.

        tdm : TrialDataManager
            Unused interface argument.
        fitparams : None
            Unused interface argument.
        tl : instance of TimeLord | None
            The optional instance of TimeLord that should be used to collect
            timing information about this method.

        Returns
        -------
        pd : array of float
            The (N,)-shaped ndarray holding the probability density for each event.
        grads : empty array of float
            Does not depend on fit parameter, so no gradient.
        """
        livetime = self.grl["stop"][-1] - self.grl["start"][0]
        pd = 1./livetime
        grads = np.array([], dtype=np.double)

        return (pd, grads)
