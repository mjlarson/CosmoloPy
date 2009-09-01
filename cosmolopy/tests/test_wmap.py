"""Optical depth and cosmic age consistency check against WMAP parameters.

Take various sets of WMAP parameters and see if I derive values for
instant reionization optical depth and age of universe that agree with
them.

"""

import numpy
import numpy.testing.utils as ntest
import matplotlib.pyplot as pylab

import cosmolopy.perturbation as cp
import cosmolopy.distance as cd
import cosmolopy.density as cden
import cosmolopy.reionization as cr
import cosmolopy.constants as cc
import cosmolopy.parameters as cparam

import test_utils as tu

def test_tau_instant():
    """Check the optical depth we get using the WMAP z_reion. 
    """
    dz = 0.1
    z = numpy.arange(80., 0. - 1.5 * dz, -1. * dz)

    cosmos = [cparam.WMAP5_BAO_SN_mean(flat=True),
              cparam.WMAP5_ML(flat=True),
              cparam.WMAP5_mean(flat=True)]

    for cosmo in cosmos:
        # Fully ionized H
        x_ionH = 1.0
        
        # The WMAP numbers apparently assume He is neutral
        x_ionHe = 0.0

        zr = cosmo['z_reion']
        tau_zr = cosmo['tau']
        tau_calc = cr.optical_depth_instant(zr, 
                                            x_ionH=x_ionH, 
                                            x_ionHe=x_ionHe,
                                            **cosmo)

        print "z_r = %f, testing tau:" % zr,
        print tu.fractional_diff_string(tau_zr, tau_calc, 3)

        ntest.assert_approx_equal(tau_calc, tau_zr, significant=2, 
                                  err_msg="Optical depth doesn't match WMAP")
        

def test_t_0():
    """Check the age of the universe we get using WMAP cosmologies.

    We only find agreement to 3 sig figs, not the 4 specified in the
    WMAP paper.

    The results of test_age.py show that we're doing the integral
    correctly, so I think the problem is that we're not taking into
    account some of the higher-order effects included in the WMAP
    numbers.

    """

    dz = 0.1
    z = numpy.arange(80., 0. - 1.5 * dz, -1. * dz)

    flat = True
    cosmos = [cparam.WMAP5_BAO_SN_mean(flat),
              cparam.WMAP5_ML(flat),
              cparam.WMAP5_mean(flat)]

    for cosmo in cosmos:
        age, err_f, err_t = cd.age(0.0, **cosmo)
        age_flat = cd.age_flat(0.0, **cosmo)
        gyr = 1e9 * cc.yr_s
        age /= gyr
        age_flat /= gyr

        print "integrated age: ",
        print tu.fractional_diff_string(age, cosmo['t_0'], 4)
        ntest.assert_approx_equal(age, cosmo['t_0'], significant=3, 
                                  err_msg="Integrated age doesn't match WMAP")

        print "analytical age: ",
        print tu.fractional_diff_string(age_flat, cosmo['t_0'], 4)
        ntest.assert_approx_equal(age_flat, cosmo['t_0'], significant=3, 
                                  err_msg="Analytical age doesn't match WMAP")

if __name__ == "__main__":
    test_tau_instant()
    test_t_0()