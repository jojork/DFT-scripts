import numpy as np
import matplotlib.pyplot as plt
from gpaw import GPAW
import csv
import glob
import re

# ------------------------------------------------------------
# DOS parameters
# ------------------------------------------------------------
npts = 2000
width = 0.1

# fixed energy grid
energy_grid = np.linspace(-2, 2, 1000)

# ------------------------------------------------------------
# get gpw files in order
# ------------------------------------------------------------
gpw_files = sorted(glob.glob("file_name*.gpw"), #keep the * as it is,because it helps to loop the mulitple nanoribbon gpw files
                   key=lambda x: int(re.findall(r'\d+', x)[0]))

print("Files found:", gpw_files)

all_dos = []
labels = []

# ------------------------------------------------------------
# loop over gpw files
# ------------------------------------------------------------
for file in gpw_files:

    print("Processing:", file)

    calc = GPAW(file, txt=None)

    energy, dos = calc.get_dos(npts=npts, width=width)

    Ef = calc.get_fermi_level()
    energy = energy - Ef

    # interpolate onto fixed grid
    dos_interp = np.interp(energy_grid, energy, dos)

    all_dos.append(dos_interp)
    labels.append(file.replace(".gpw",""))

all_dos = np.array(all_dos)

# ------------------------------------------------------------
# save single CSV
# ------------------------------------------------------------
with open("all_ribbon_DOS.csv", "w", newline="") as f:

    writer = csv.writer(f)

    header = ["Energy(eV)"] + labels
    writer.writerow(header)

    for i in range(len(energy_grid)):
        row = [energy_grid[i]] + list(all_dos[:, i])
        writer.writerow(row)

print("Saved: all_ribbon_DOS.csv")

# ------------------------------------------------------------
# plot
# ------------------------------------------------------------
plt.figure(figsize=(8,6))

for i in range(len(labels)):
    plt.plot(energy_grid, all_dos[i], label=labels[i])

plt.axvline(0, color='k', linestyle='--')

plt.xlabel("Energy (E − Ef) [eV]")
plt.ylabel("DOS (states/eV)")
plt.xlim(-2,2)

plt.title("Nanoribbon DOS Evolution")
plt.legend()

plt.tight_layout()
plt.savefig("all_ribbon_DOS.png", dpi=300)
plt.show()

print("Saved: all_ribbon_DOS.png")
