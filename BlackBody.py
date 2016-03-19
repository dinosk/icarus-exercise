from astropy.constants import h, c, k_B, sigma_sb, R_sun
from astropy import units as u
from scipy.integrate import quad
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
parser.add_argument("--no-gui", action="store_true", help="Disable the GUI")

np.seterr(over='ignore')


class BlackBody(object):
    """BlackBody(object)
    Main Class representing a black body of a certain temperature. 
    It can create a plot of flux vs wavelength using matplotlib, 
    and calculate the U, B, V, R, I magnitudes using as a reference a 0 magnitude star.

    In this case: alpha Lyr star with the values taken from Bessell et al. (1998) Johnson-Cousins-Glass System
    The F0 values are read from the config file "reference_data.cfg"
    """
    def __init__(self, T):
        """
        Create a black body by setting its temperature.
        If no units are passed, it defaults to Kelvin.
        """
        if not isinstance(T, u.Quantity):
            T_in_K = u.Quantity(T, u.K)
        self.T = T_in_K
        self.ref_data = {}
        self.read_config()


    def readReferenceData(self, section):
        """
        Utility function for the ConfigParser to parse the reference_data.cfg
        """
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
        """
        Parses the reference values for the 0 magnitude star.
        """
        Config = ConfigParser.ConfigParser()
        Config.read("reference_data.cfg")
        for section in Config.sections():
            self.ref_data[section] = self.readReferenceData(section)

    def radiation(self, wavelength, T=None):
        """
        Calculates the black body radiation for a given wavelength or wavelength range.
        """
        if T:
            if not isinstance(T, u.Quantity):
                T = u.Quantity(T, u.K)
            self.T = T
        numerator = ((2 * np.pi * h * c**2) / (wavelength * u.m)**5)
        exponent = (h.value * c.value) / (wavelength * k_B.value * self.T.value)
        denominator = np.exp(exponent) - 1
        return (numerator / denominator).value

    def obs_flux(self, wavelength, T=None):
        """
        Calculates the observed flux for a certain wavelength or wavelength range.
        """
        return self.radiation(wavelength, T) * (R_sun / (10 * u.parsec).to(u.m))**2

    def magnitude(self, band):
        """
        Calculates the magnitude of a given band passed as a letter argument.
        For example m_u = magnitude("u")

        Integrates with the quad method from scipy.
        """
        # m_x = -2.5 * np.log10( quad(self.obs_flux,
		# 						 	self.ref_data["lambda_eff"][band] - self.ref_data["delta_lambda"][band]/2,
		#			 			    self.ref_data["lambda_eff"][band] + self.ref_data["delta_lambda"][band]/2)[0]
		#							/ self.ref_data["f_lambda_0"][band] )
        m_x = -2.5 * np.log10( self.obs_flux(self.ref_data["lambda_eff"][band]) / self.ref_data["f_lambda_0"][band] )
        return m_x

    def show_plot(self, output_file=None):
        """
        Creates a plot of Flux vs Wavelength using matplotlib.
        Wavelength range is set from 1nm to 1um.
        If an output file is passed it will save it in the current working
        directory under the given name.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
        fig.subplots_adjust(**adjustprops)

        ax.set_xlabel(r'$Wavelength \, [nm]$', size=15, labelpad=20)
        ax.set_ylabel(r'$Flux \, [\mathrm{erg\, m^{-2}\, nm^{-1}\, s^{-1}}]$', size=15)

        ax.minorticks_on()
        ax.grid()

        # We will create the plot for wavelengths of 1nm up to 1um
        wavelength = np.arange(1e-9, 1e-6, 1e-9)

        spectrum = self.radiation(wavelength)

        ax.plot(wavelength*10**9, spectrum, color="red", linewidth=3, linestyle="-")
        plt.title('Flux vs Wavelength of BlackBody at %d K' % self.T.value)
        fig.show()
        if output_file:
            plt.savefig("plots/"+output_file)


if __name__ == "__main__":
    """
    Sample main function.
    Spawns the GUI or if the --no-gui flag is passed
    creates a black body with the given temperature and either
    prints the magnitudes or creates a plot.

    For example:
        python BlackBody.py -t 4000 -o fig.png
        # will create a plot of Flux vs Wavelength of a black body with 4000K.

        python BlackBody.py --mag-only
        # will print out the U, B, V, R, I magnitudes of the sun. (default temp = 5778K)
    """
    args = parser.parse_args()
    if args.temperature:
        bb = BlackBody(args.temperature)
    else:
        # print "Temperature was not set, using default value 5778K"
        bb = BlackBody(5778)

    if args.no_gui:
    	if args.mag_only:
    	    print "U:", bb.magnitude("u")
    	    print "B:", bb.magnitude("b")
    	    print "V:", bb.magnitude("v")
    	    print "R:", bb.magnitude("r")
    	    print "I:", bb.magnitude("i")
    	    sys.exit()

    	if args.output_file:
    	    bb.show_plot(args.output_file)
    	else:
    	    bb.show_plot()
    	sys.exit()
    app = Gui.Gui(None)
    app.title("Icarus Exercise")
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)
    app.mainloop()

    
