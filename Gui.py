import Tkinter
import os
from BlackBody import BlackBody


class Gui(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()


    def initialize(self):
        self.grid()

        self.temp_text = Tkinter.StringVar()
        self.filename_text = Tkinter.StringVar()
        self.magnitude_U = Tkinter.StringVar()
        self.magnitude_B = Tkinter.StringVar()
        self.magnitude_V = Tkinter.StringVar()
        self.magnitude_R = Tkinter.StringVar()

        self.temp_label_text = Tkinter.StringVar()
        self.temp_label = Tkinter.Label(self, textvariable=self.temp_label_text, anchor="w")
        self.temp_label.grid(column=0, row=0, sticky='EW')
        self.temp_label_text.set(u"Temperature")
        self.temp_slider = Tkinter.Scale(orient='horizontal', from_=3000, to=25000, command=self.set_temp_slider)
        self.temp_slider.grid(column=1, row=1, sticky='EW')
        self.temp_input = Tkinter.Entry(self, textvariable=self.temp_text)
        self.temp_input.grid(column=1, row=0, sticky='EW')
        self.temp_text.set(u"Enter Temperature in K")
        #temp_button = Tkinter.Button(self, text=u"Set", command=self.set_temp)
        #temp_button.grid(column=1, row=0)
        self.filename_label_text = Tkinter.StringVar()
        self.filename_label = Tkinter.Label(self, textvariable=self.filename_label_text, anchor="w")
        self.filename_label.grid(column=0, row=3, sticky='EW')
        self.filename_label_text.set(u"Save as")
        self.filename_input = Tkinter.Entry(self, textvariable=self.filename_text)
        self.filename_input.grid(column=1, row=3, sticky='EW')
        self.filename_input.bind("<Return>", self.save_plot)
        self.filename_text.set(u"fig.png")

        self.magnitude_U_label = Tkinter.Label(self, textvariable=self.magnitude_U, anchor="w")
        self.magnitude_U_label.grid(column=5, row=0, sticky='EW')
        self.magnitude_U.set(u"U:")

        self.magnitude_B_label = Tkinter.Label(self, textvariable=self.magnitude_B, anchor="w")
        self.magnitude_B_label.grid(column=6, row=0, sticky='EW')
        self.magnitude_B.set(u"B:")

        self.magnitude_V_label = Tkinter.Label(self, textvariable=self.magnitude_V, anchor="w")
        self.magnitude_V_label.grid(column=5, row=1, sticky='EW')
        self.magnitude_V.set(u"V:")

        self.magnitude_R_label = Tkinter.Label(self, textvariable=self.magnitude_R, anchor="w")
        self.magnitude_R_label.grid(column=6, row=1, sticky='EW')        
        self.magnitude_R.set(u"R:")

        calc_mag_button = Tkinter.Button(self, text=u"Calculate Magnitudes", command=self.calc_mag)
        calc_mag_button.grid(column=6, row=4)

        filename_button = Tkinter.Button(self, text=u"Plot", command=self.save_plot)
        filename_button.grid(column=0, row=4)

        self.feedback = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.feedback,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=6, columnspan=3, sticky='EW')
        self.feedback.set(u"Please specify the Black Body temperature and set a filename for the plot!")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True,False)
        self.temp_input.focus_set()
        self.temp_input.selection_range(0, Tkinter.END)

    
    def set_temp(self):
        self.feedback.set("Plot black body with temperature: "+self.temp_text.get()+"K")
        # self.temp_input.focus_set()
        # self.temp_input.selection_range(0, Tkinter.END)
        self.temp_slider.set(int(self.temp_text.get()))

    
    def set_temp_slider(self, event):
        self.bb = BlackBody(int(event))
        self.feedback.set("Plot black body with temperature: "+event+"K")
        self.temp_text.set(event)
        self.temp_input.focus_set()
        self.temp_input.selection_range(0, Tkinter.END)


    def calc_mag(self):
    	if self.bb is None:
    		self.feedback.set(u"First must set a temperature!")
    	self.magnitude_U.set(u"U: %f" % self.bb.magnitude("u"))
    	self.magnitude_B.set(u"B: %f" % self.bb.magnitude("b"))
    	self.magnitude_V.set(u"V: %f" % self.bb.magnitude("v"))
    	self.magnitude_R.set(u"R: %f" % self.bb.magnitude("r"))


    def save_plot(self):
    	self.set_temp()
    	self.bb = BlackBody(int(self.temp_text.get()))
        self.bb.show_plot(self.filename_text.get())
        self.feedback.set("Plot saved in: "+os.getcwd()+"/"+self.filename_text.get())
        self.temp_input.focus_set()
        self.temp_input.selection_range(0, Tkinter.END)


    def on_enter(self, event):
        self.feedback.set(self.entryVariable.get() + "You pressed enter !")
        self.temp_input.focus_set()
        self.temp_input.selection_range(0, Tkinter.END)
        print event
        # IPython.embed()
