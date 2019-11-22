from __future__ import division
import numpy as np
import lalsimulation as lalsim
import lal
import matplotlib.pyplot as plt

m1     = 20
m2     = 50
spin1x = 0.0
spin1y = 0.0
spin1z = 0.0
spin2x = 0.0
spin2y = 0.0
spin2z = 0.0
d      = 500
phi0   = 2.0
inclination = 0.0

sampling_rate = 2048
dt            = 1./sampling_rate
flow          = 20
fref          = 20
LALpars       = lal.CreateDict()
approx        = lalsim.SimInspiralGetApproximantFromString('SEOBNRv2')

hp, hc = lalsim.SimInspiralChooseTDWaveform(
                        m1*lalsim.lal.MSUN_SI,
                        m2*lalsim.lal.MSUN_SI,
                        spin1x, spin1y, spin1z,
                        spin2x, spin2y, spin2z,
                        d*1e6*lalsim.lal.PC_SI,
                        inclination,
                        phi0,
                        0, #longAscNodes
                        0, #eccentricity
                        0, #meanPerAno
                        dt,
                        flow,
                        fref,
                        LALpars,
                        approx
                        )
times = dt*np.array(range(len(hp.data.data)))
                 
plt.figure()
plt.plot(times, hp.data.data, label='Plus polarisation')
plt.plot(times, hc.data.data, label ='Cross polarisation')
plt.xlabel('time (s)')
plt.ylabel('h')
plt.title('BBH coalescence of {0} and {1} solar masses'.format(m1,m2))
plt.legend(loc='best')
plt.show()
plt.close()