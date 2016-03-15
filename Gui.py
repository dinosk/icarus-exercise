import Tkinter
import os
import BlackBody
import IPython
import matplotlib.pyplot as plt
import numpy as np
import random

class Gui(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        # list that will save the black bodies to plot
        self.bbs = []
        self.temps = ""


    def initialize(self):
        """
        Initialization of the GUI.
        """
        self.grid()

        self.temp_text = Tkinter.StringVar()
        self.filename_text = Tkinter.StringVar()
        self.magnitude_U = Tkinter.StringVar()
        self.magnitude_B = Tkinter.StringVar()
        self.magnitude_V = Tkinter.StringVar()
        self.magnitude_R = Tkinter.StringVar()

        # Temperature field and slider
        self.temp_label_text = Tkinter.StringVar()
        self.temp_label = Tkinter.Label(self, textvariable=self.temp_label_text, anchor="w")
        self.temp_label.grid(column=0, row=0, sticky='EW')
        self.temp_label_text.set(u"Temperature")
        self.temp_slider = Tkinter.Scale(orient='horizontal', from_=3000, to=25000, command=self.set_temp_slider)
        self.temp_slider.grid(column=1, row=1, sticky='EW')
        self.temp_input = Tkinter.Entry(self, textvariable=self.temp_text)
        self.temp_input.grid(column=1, row=0, sticky='EW')
        self.temp_text.set(u"Enter Temperature in K")

        # Save as field and button
        self.filename_label_text = Tkinter.StringVar()
        self.filename_label = Tkinter.Label(self, textvariable=self.filename_label_text, anchor="w")
        self.filename_label.grid(column=0, row=3, sticky='EW')
        self.filename_label_text.set(u"Save as")
        self.filename_input = Tkinter.Entry(self, textvariable=self.filename_text)
        self.filename_input.grid(column=1, row=3, sticky='EW')
        self.filename_input.bind("<Return>", self.save_plot)
        self.filename_text.set(u"fig.png")

        # Magnitude U: field
        self.magnitude_U_label = Tkinter.Label(self, textvariable=self.magnitude_U, anchor="w")
        self.magnitude_U_label.grid(column=5, row=0, sticky='EW')
        self.magnitude_U.set(u"U:")

        # Magnitude B: field
        self.magnitude_B_label = Tkinter.Label(self, textvariable=self.magnitude_B, anchor="w")
        self.magnitude_B_label.grid(column=6, row=0, sticky='EW')
        self.magnitude_B.set(u"B:")

        # Magnitude V: field
        self.magnitude_V_label = Tkinter.Label(self, textvariable=self.magnitude_V, anchor="w")
        self.magnitude_V_label.grid(column=5, row=1, sticky='EW')
        self.magnitude_V.set(u"V:")

        # Magnitude R: field
        self.magnitude_R_label = Tkinter.Label(self, textvariable=self.magnitude_R, anchor="w")
        self.magnitude_R_label.grid(column=6, row=1, sticky='EW')        
        self.magnitude_R.set(u"R:")

        # Magnitude I: field
        calc_mag_button = Tkinter.Button(self, text=u"Calculate Magnitudes", command=self.calc_mag)
        calc_mag_button.grid(column=6, row=4)

        # Set temperature button
        temp_button = Tkinter.Button(self, text=u"Set", command=self.set_temp)
        temp_button.grid(column=0, row=1)        

        # Plot button
        filename_button = Tkinter.Button(self, text=u"Plot", command=self.save_plot)
        filename_button.grid(column=0, row=4)

        # Feedback field
        self.feedback = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.feedback,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=6, columnspan=3, sticky='EW')
        self.feedback.set(u"To create a plot: specify temperature(s) press set and press plot")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True,False)
        self.temp_input.focus_set()
        self.temp_input.selection_range(0, Tkinter.END)

    
    def set_temp(self):
        """
        Add the black body with the given temperature to the array with
        black bodies to plot.
        """
        try:
            newtemp = int(self.temp_text.get())
            if newtemp < 0:
                raise ValueError
            self.temp_slider.set(int(self.temp_text.get()))
        except ValueError:
            self.feedback.set("Please enter a positive integer value")
            return
        self.temps += self.temp_text.get()+" "
        self.feedback.set("Plot Flux vs Wavelength of: %sK" % self.temps)
        bb = BlackBody.BlackBody(newtemp)
        self.bbs.append(bb)

    
    def set_temp_slider(self, event):
        """
        What happens if you move the slider.
        """
        self.temp_text.set(event)


    def calc_mag(self):
        """
        What happens if you press the Calculate Magnitudes button.
        """
    	if self.temp_text.get() is None:
    		self.feedback.set(u"First must set a temperature!")
        bb = BlackBody.BlackBody(int(self.temp_text.get()))
    	self.magnitude_U.set(u"U: %f" % bb.magnitude("u"))
    	self.magnitude_B.set(u"B: %f" % bb.magnitude("b"))
    	self.magnitude_V.set(u"V: %f" % bb.magnitude("v"))
    	self.magnitude_R.set(u"R: %f" % bb.magnitude("r"))


    def save_plot(self):
        """
        What happens if you press the Plot button.
        """
    	self.show_plot(self.filename_text.get())
        self.feedback.set("Plot saved in: "+os.getcwd()+"/"+self.filename_text.get())


    def show_plot(self, output_file=None):
        """
        Creates the plot of the black body or multiple black bodies.
        Saves it under the specified name.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
        fig.subplots_adjust(**adjustprops)

        # Setting the labels for the X and Y axis
        ax.set_xlabel(r'$Wavelength \, [nm]$', size=15, labelpad=20)
        ax.set_ylabel(r'$Flux \, [\mathrm{erg\, m^{-2}\, nm^{-1}\, s^{-1}}]$', size=15)

        ax.minorticks_on()
        ax.grid()

        # We will create the plot for wavelengths of 1nm up to 1um
        wavelength = np.arange(1e-9, 1e-6, 1e-9)
        # print wavelength

        #legend_lines = []
        for bb in self.bbs:
            #legend_lines.append( ax.plot(wavelength*10**9, bb.radiation(wavelength), color="red", linewidth=3, linestyle="-", label=bb.T) )
            ax.plot(wavelength*10**9, bb.radiation(wavelength), color=np.random.rand(3,1), linewidth=3, linestyle="-", label=bb.T)
        plt.legend()

        plt.title('Flux vs Wavelength of BlackBody.BlackBody at %s K' % self.temps, y=1.04)
        fig.show()
        if output_file:
            plt.savefig(output_file)

