from astropy.constants import h, c, k_B, sigma_sb, R_sun
from astropy import units as u
from scipy.integrate import quad, trapz, cumtrapz, simps
import numpy as np
import matplotlib.pyplot as plt
import argparse
import Tkinter
import IPython
import sys, os
import ConfigParser
import Gui

parser = argparse.ArgumentParser()
parser.add_argument("--output-file", "-o", help="Specify an output file for plots")
parser.add_argument("--temperature", "-t", help="Sets the temperature of the black body", type=int)
parser.add_argument("--mag-only", action="store_true", help="Print the U, B, V, R, I magnitudes only")

np.seterr(over='ignore')


class BlackBody(object):
    """
    Class
    """
    def __init__(self, T):
        if not isinstance(T, u.Quantity):
            T_in_K = u.Quantity(T, u.K)
        self.T = T_in_K
        self.ref_data = {}
        self.read_config()


    def readReferenceData(self, section):
        dict1 = {}
        Config = ConfigParser.ConfigParser()
        Config.read("reference_data.cfg")
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = float(Config.get(section, option))
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1


    def read_config(self):
        Config = ConfigParser.ConfigParser()
        Config.read("reference_data.cfg")
        for section in Config.sections():
            self.ref_data[section] = self.readReferenceData(section)

    def radiation(self, wavelength, T=None):
        if T:
            if not isinstance(T, u.Quantity):
                T = u.Quantity(T, u.K)
            self.T = T
        numerator = ((2 * np.pi * h * c**2) / (wavelength * u.m)**5)
        exponent = (h.value * c.value) / (wavelength * k_B.value * self.T.value)
        denominator = np.exp(exponent) - 1
        return (numerator / denominator).value

    def obs_flux(self, wavelength, T=None):
        return self.radiation(wavelength, T) * (R_sun / (10 * u.parsec).to(u.m))**2

    def magnitude(self, band):
        m_x = -2.5 * np.log10( quad(self.obs_flux,
								 	self.ref_data["lambda_eff"][band] - self.ref_data["delta_lambda"][band]/2,
					 			    self.ref_data["lambda_eff"][band] + self.ref_data["delta_lambda"][band]/2)[0]
									/ self.ref_data["f_lambda_0"][band] )
        return m_x

    def show_plot(self, output_file=None):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
        fig.subplots_adjust(**adjustprops)
        # Setting the labels for the X and Y axis
        ax.set_xlabel(r'$Wavelength \, [nm]$', size=15, labelpad=20)
        ax.set_ylabel(r'$Flux \, [\mathrm{erg\, m^{-2}\, nm^{-1}\, s^{-1}}]$', size=15)
        # plt.ticklabel_format(style="sci",scilimits=(2,2),axis="y")

        ax.minorticks_on()
        ax.grid()

        # We will create the plot for wavelengths of 1nm up to 1um
        wavelength = np.arange(1e-9, 1e-6, 1e-9)
        # print wavelength
        spectrum = self.radiation(wavelength)

        ax.plot(wavelength*10**9, spectrum, color="red", linewidth=3, linestyle="-", label=r"$T_2=4000 \, \mathrm{K}$")
        plt.title('Flux vs Wavelength of BlackBody at %d K' % self.T.value)
        fig.show()
        if output_file:
            plt.savefig(output_file)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.temperature:
        bb = BlackBody(args.temperature)
    else:
        print "Temperature was not set, using default value 5778K"
        bb = BlackBody(5778)

    app = Gui.Gui(None)
    app.title("Icarus Exercise")
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)
    app.mainloop()

    # print ref_data
    if args.mag_only:
        print "U:", bb.magnitude("u")
        print "B:", bb.magnitude("b")
        print "V:", bb.magnitude("v")
        print "R:", bb.magnitude("r")
        print "I:", bb.magnitude("i")
        sys.exit()
    # print "Writing to file:", args.output_file
    if args.output_file:
        bb.show_plot(args.output_file)
    else:
        bb.show_plot()
