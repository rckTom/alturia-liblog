import alturialog as al
import matplotlib.pyplot as plt

log = al.Alturialog("../data/36c3.dat")
log.track_data[0].plot()
plt.show()

