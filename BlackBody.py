from astropy.constants import h, c, k_B, sigma_sb, R_sun
from astropy import units as u
from scipy.integrate import quad, trapz, cumtrapz, simps
import numpy as np
import matplotlib.pyplot as plt
import argparse
import warnings
import IPython
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--output-file", "-o", help="Specify an output file for plots")
parser.add_argument("--temperature", "-t", help="Sets the temperature of the star", type=int)
parser.add_argument("--mag-only", action="store_true", help="Print the U, B, V, R, I magnitudes only")

U = 365.6*1e-9
U_band = 66*1e-9
B = 445.3*1e-9
B_band = 94*1e-9
V = 551.7*1e-9
V_band = 88*1e-9
R = 658.9*1e-9
R_band = 138*1e-9
I = 806.7*1e-9
I_band = 149*1e-9

np.seterr(over='ignore')

class BlackBody(object):
	"""
	Class
	"""
	def __init__(self, T):
		if not isinstance(T, u.Quantity):
			T_in_K = u.Quantity(T, u.K)
		self.T = T_in_K

	def radiation(self, wavelength, T=None):
		if T:
			if not isinstance(T, u.Quantity):
				T = u.Quantity(T, u.K)
			self.T = T
		numerator = ((2 * np.pi * h * c**2) / (wavelength)**5)
		# IPython.embed()
		exponent = (h.value * c.value) / (wavelength * k_B.value * self.T.value)
		denominator = np.exp(exponent) - 1
		return (numerator / denominator).value

	def obs_flux(self, wavelength, T=None):
		return self.radiation(wavelength, T) * (R_sun / (10 * u.parsec).to(u.m))**2

	# 3.14522e-09
	# 2.9926e-09
	def magnitude_U(self):
		wavelength = np.arange(U - U_band/2, U + U_band/2, 1e-9)
		spectrum = self.obs_flux(wavelength)
		m_x = -2.5 * np.log10( simps(spectrum, None, 1e-9) / 3.980e-9 )
		# m_x = -2.5 * np.log10( cumtrapz(self.obs_flux, U - U_band/2, U + U_band/2)[0] / 3.208e-9 )
		# m_x = -2.5 * np.log10( self.obs_flux(U).value / 3980*1e-4 )
		return m_x

	# 6.59271e-09
	# 4.15143e-09
	def magnitude_B(self):
		wavelength = np.arange(B - B_band/2, B + B_band/2, 1e-9)
		spectrum = self.obs_flux(wavelength)
		m_x = -2.5 * np.log10( simps(spectrum, None, 1e-9) / 6.55e-9 )
		# m_x = -2.5 * np.log10( quad(self.obs_flux, B - B_band/2, B + B_band/2)[0] / 6.55e-9 )
		# m_x = -2.5 * np.log10( self.obs_flux(B).value / 6950*1e-4 )
		return m_x

	# 3.52475e-09
	# 3.60047e-09
	def magnitude_V(self):
		wavelength = np.arange(V - V_band/2, V + V_band/2, 1e-9)
		spectrum = self.obs_flux(wavelength)
		m_x = -2.5 * np.log10( simps(spectrum, None, 1e-9) / 3.3992e-9 )
		# bandwidth = np.arange(V - V_band/2, V + V_band/2, 1e-9)
		# m_x = -2.5 * np.log10( quad(self.obs_flux, V - V_band/2, V + V_band/2)[0] / 3.3992e-9 )
		return m_x

	# 1.89348e-09
	# 2.27736e-09
	def magnitude_R(self):
		wavelength = np.arange(R - R_band/2, R + R_band/2, 1e-9)
		spectrum = self.obs_flux(wavelength)
		m_x = -2.5 * np.log10( simps(spectrum, None, 1e-9) / 2.177e-9 )
		# bandwidth = np.arange(R - R_band/2, R + R_band/2, 1e-9)
		# m_x = -2.5 * np.log10( quad(self.obs_flux, R - R_band/2, R + R_band/2)[0] / 2.177e-9 )
		return m_x

	# 1.18279e-09
	# 9.43402e-10
	def magnitude_I(self):
		wavelength = np.arange(I - I_band/2, I + I_band/2, 1e-9)
		spectrum = self.obs_flux(wavelength)
		m_x = -2.5 * np.log10( simps(spectrum, None, 1e-9) / 1.126e-9 )
		# bandwidth = np.arange(I - I_band/2, I + I_band/2, 1e-9)
		# m_x = -2.5 * np.log10( quad(self.obs_flux, I - I_band/2, I + I_band/2)[0] / 1.126e-9 )
		return m_x

	def show_plot(self, output_file=None):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
		fig.subplots_adjust(**adjustprops)

		# Setting the labels for the X and Y axis
		ax.set_xlabel(r'$Wavelength \, [nm]$', size=15, labelpad=20)
		ax.set_ylabel(r'$Flux \, [\mathrm{W sr^{-1} m^{-2} nm^{-1}}]$', size=15)
		plt.ticklabel_format(style="sci",scilimits=(2,2),axis="y")

		ax.minorticks_on()
		ax.grid()

		# We will create the plot for wavelengths of 1nm up to 1um
		wavelength = np.arange(1e-9, 1e-6, 1e-9)
		# print wavelength
		spectrum = self.radiation(wavelength)

		ax.plot(wavelength*10**9, spectrum.value, color="red", linewidth=3, linestyle="-", label=r"$T_2=4000 \, \mathrm{K}$")

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

	if args.mag_only:
		print "U:", bb.magnitude_U()
		print "B:", bb.magnitude_B()
		print "V:", bb.magnitude_V()
		print "R:", bb.magnitude_R()
		print "I:", bb.magnitude_I()
		sys.exit()
	# print "Writing to file:", args.output_file
	if args.output_file:
		bb.show_plot(args.output_file)
	else:
		bb.show_plot()
