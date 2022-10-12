import tifffile
import spam.DIC
import spam.plotting
import spam.label
import matplotlib.pyplot as plt
import tkinter #python3
from tkinter import messagebox as tkMessageBox #python3
from tkinter import filedialog as tkFileDialog #python3

root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir='/home/hideharu/spam/work'



print('enter the first file name')
first = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
iDir = first
print('enter the secondo file name')
second = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
grey = spam.DIC.binning(tifffile.imread(first), 2) # downscale the image while reading it
grey2 = spam.DIC.binning(tifffile.imread(second), 2) # downscale the image while reading it
tifffile.imsave(first + "bin.tif", grey) # save it for later
tifffile.imsave(second + "bin.tif", grey2) # save it for later


plt.imshow(grey[:, :, grey.shape[2]//2], cmap="Greys_r"); plt.show()

spam.plotting.plotGreyLevelHistogram(grey, showGraph=True)

# following from above
binary = grey >= 40000 # i.e., binary is where "grey" is bigger than or equal to 18000

print(binary.sum()) # let's count the number of "True" voxels:
# output:
# 4985517

plt.imshow(binary[:, :, binary.shape[2]//2], cmap="Greys_r"); plt.show()

print('labeling. Please wait a few minutes')

labelled = spam.label.watershed(binary) # about 3 minutes on Eddy's laptop
# tifffile.imsave(""M2EA05-01-bin4-watershed.tif", labelled) # save it for later

print(labelled.max())
# output:
# 3105
# *i.e.,* there are 3105 different particles

# use spam.label.randomCmap to show different labels
plt.imshow(labelled[:, :, labelled.shape[2]//2], cmap=spam.label.randomCmap); plt.show()

print('select the name of save label image')
save_name = tkinter.filedialog.asksaveasfilename(filetypes = fTyp,initialdir = iDir)
tifffile.imsave(save_name, labelled)



