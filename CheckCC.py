import spam.helpers
import numpy
import matplotlib.pyplot as plt
import tifffile
import spam.label
import tkinter #python3
from tkinter import messagebox as tkMessageBox #python3
from tkinter import filedialog as tkFileDialog #python3

root = tkinter.Tk()
root.withdraw()
fTyp = [("","*.tsv")]
iDir='/home/hideharu/work'
print('select PSfile of .tsv')
PS_file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
PS = spam.helpers.readCorrelationTSV(PS_file, readPixelSearchCC=1)

print("Minimum and Average CC value for bad correlation")
print(numpy.min(PS['pixelSearchCC'][1:]))
print(numpy.mean(PS[ 'pixelSearchCC'][1:]))

plt.hist(PS['pixelSearchCC'][1:], bins=100, range=[0.96, 1.0], label='CC',  histtype='step')
plt.legend(loc='upper left')
plt.xlabel("NCC value")
plt.ylabel("Number of particles")
plt.show()

print('select the labeled file')
fTyp = [("","*.tif")]
lab = tifffile.imread(tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir))
#lab = tifffile.imread("0-1_label.tif")
labCCbad = spam.label.convertLabelToFloat(lab, PS['pixelSearchCC'])
tifffile.imsave("00-lab-CC.tif", labCCbad.astype('<f4'))