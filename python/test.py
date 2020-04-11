import alturialog as al
import matplotlib.pyplot as plt

log = al.Alturialog("../data/log1.dat")
log.tracks[0].to_dataframe().plot()
plt.show()

