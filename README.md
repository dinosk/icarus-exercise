Icarus Exercise
===================
**Google Summer of Code 2016**
**Konstantinos Kousidis** <dinos.kousidis@tum.de>
**Technische Universitaet Muenchen**

Hi! This is my exercise for my application for the __Lightcurve modeling with Icarus__ project.
This python app can create a plot of Flux vs Wavelength for 1 or more black bodies of certain temperatures, and calculate their U, B, V, R magnitudes based on Î± Lyr Flux values taken from Bessell et al. (1998) Johnson-Cousins-Glass System.

Project Description
-------------
> **Prerequisites:**
> python 2.7
> scipy 
> numpy
> matplotlib
> Tkinter (for the GUI, should come with python)

The project has just 2 python files, 1 for the black body class and 1 for the GUI.
You can start it with:  
```
python BlackBody.py
```

A window will popup where you can choose some temperatures (press the Set button after selecting each one)
and create a plot by pressing the Plot button.
For the U, B, V, R magnitudes press the calculate magnitudes button.
If you don't want to spawn the GUI and just run it from the command line pass:
```
python BlackBody.py --no-gui -t 4000 -o fig4000.png
```

-t: sets the temperature and
 -o: specifies the output file
-h: shows help text
--no-gui: doesn't spawn the gui
--mag-only: prints the U, B, V, R magnitudes

----------
#### Calculations

The BlackBody class can calculate the radiation, observed flux and magnitude using the following formulas:

$$
B_\lambda(\lambda, t) = \int_0^\infty   \frac{2\pi h c ^ 2}{\lambda^5} * \frac{1}{e^\frac{hc}{\lambdak_BT} - 1}
$$

$$
F_Î»(Î», t) = \frac{2\pi h c ^ 2}{Î»^5} * \frac{1}{e^\frac{hc}{Î»k_BT} - 1} * (\frac{R}{r})^2
$$

$$
m_V = m_{v,o} - 2.5 * log_{10} (\frac{\int_{Î»_{eff} - Î”_Î»/2}^{Î»_{eff} + Î”_Î»/2}  F(Î»)dÎ»}{Î»F_{v,0}})
$$

![B_\lambda(\lambda, t) = \int_0^\infty   \frac{2\pi h c ^ 2}{\lambda^5} * \frac{1}{e^\frac{hc}{\lambdak_BT} - 1}](http://www.sciweavers.org/tex2img.php?eq=1%2Bsin%28mc%5E2%29&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=)