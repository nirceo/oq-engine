#!/usr/bin/env/python
# LICENSE
#
# Copyright (c) 2010-2013, GEM Foundation, G. Weatherill, M. Pagani, D. Monelli
#
# The Hazard Modeller's Toolkit (hmtk) is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>
#
# DISCLAIMER
#
# The software Hazard Modeller's Toolkit (hmtk) provided herein is released as
# a prototype implementation on behalf of scientists and engineers working
# within the GEM Foundation (Global Earthquake Model).
#
# It is distributed for the purpose of open collaboration and in the hope that
# it will be useful to the scientific, engineering, disaster risk and software
# design communities.
#
# The software is NOT distributed as part of GEM's OpenQuake suite
# (http://www.globalquakemodel.org/openquake) and must be considered as a
# separate entity. The software provided herein is designed and implemented
# by scientific staff. It is not developed to the design standards, nor
# subject to same level of critical review by professional software developers,
# as GEM's OpenQuake software suite.
#
# Feedback and contribution to the software is welcome, and can be directed to
# the hazard scientific staff of the GEM Model Facility
# (hazard@globalquakemodel.org).
#
# The Hazard Modeller's Toolkit (hmtk) is therefore distributed WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# The GEM Foundation, and the authors of the software, assume no liability for
# use of the software.

'''
Module to produce cumulative moment plot
'''


import numpy as np
import matplotlib.pyplot as plt


def plot_cumulative_moment(year, mag):
    '''Calculation of Mmax using aCumulative Moment approach, adapted from
    the cumulative strain energy method of Makropoulos & Burton (1983)
    :param year: Year of Earthquake
    :type year: numpy.ndarray
    :param mag: Magnitude of Earthquake
    :type mag: numpy.ndarray
    :keyword iplot: Include cumulative moment plot
    :type iplot: Boolean
    :return mmax: Returns Maximum Magnitude
    :rtype mmax: Float
    '''
    # Calculate seismic moment
    m_o = 10. ** (9.05 + 1.5 * mag)
    year_range = np.arange(np.min(year), np.max(year) + 1, 1)
    nyr = np.float(np.shape(year_range)[0])
    morate = np.zeros(nyr, dtype=float)
    # Get moment release per year
    for loc, tyr in enumerate(year_range):
        idx = np.abs(year - tyr) < 1E-5
        if np.sum(idx) > 0:
            # Some moment release in that year
            morate[loc] = np.sum(m_o[idx])
    ave_morate = np.sum(morate) / nyr

    # Average moment rate vector
    exp_morate = np.cumsum(ave_morate * np.ones(nyr))

    plt.step(year_range, np.cumsum(morate), 'b-', linewidth=2)
    plt.plot(year_range, exp_morate, 'r-', linewidth=2)
    # Get offsets
    upper_morate = exp_morate + (np.max(np.cumsum(morate) - exp_morate))
    lower_morate = exp_morate + (np.min(np.cumsum(morate) - exp_morate))
    plt.plot(year_range, upper_morate, 'r--', linewidth=1)
    plt.plot(year_range, lower_morate, 'r--', linewidth=1)
    plt.axis([np.min(year), np.max(year), 0.0, np.sum(morate)])
