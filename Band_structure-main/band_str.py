# Band_structure
# this script helps to find band structure

import numpy as np
import matplotlib.pyplot as plt
from gpaw import GPAW
from ase.dft.dos import DOS
from gpaw.response.df import DielectricFunction


# ------------------------------------------------------------
# Load ground state
# ------------------------------------------------------------
calc = GPAW('input_file.gpw', txt=None)   # generic name
atoms = calc.get_atoms()

fermi = calc.get_fermi_level()
print(f"Fermi level = {fermi:.3f} eV")

# ============================================================
# BAND STRUCTURE (OLD GPAW – CORRECT METHOD)
# ============================================================
print("Calculating band structure...")

# Explicit fractional k-points (no symbols at all)
kpts_band = []

segments = [
    ([0.0, 0.0, 0.0], [0.5, 0.0, 0.0]),
    ([0.5, 0.0, 0.0], [0.5, 0.5, 0.0]),
    ([0.5, 0.5, 0.0], [0.0, 0.5, 0.0]),
    ([0.0, 0.5, 0.0], [0.0, 0.0, 0.0])
]

nseg = 25

for start, end in segments:
    for t in np.linspace(0, 1, nseg, endpoint=False):
        kpts_band.append((1 - t) * np.array(start) + t * np.array(end))
kpts_band.append([0.0, 0.0, 0.0])

calc_bs = GPAW(
    'input_file.gpw',   # generic name
    kpts=kpts_band,
    symmetry='off',
    txt='band_structure.txt'
)

atoms_bs = calc_bs.get_atoms()
atoms_bs.get_potential_energy()

bs = calc_bs.band_structure()
bs.plot(filename='band_structure.png', show=False)

# ============================================================
# SAVE BAND STRUCTURE TO CSV
# ============================================================
print("Saving band structure to CSV...")

energies = bs.energies  # eV

# Handle spin dimension safely
if energies.ndim == 3:
    energies = energies[0]

nkpts, nbands = energies.shape

# Simple k-path index
k_index = np.arange(nkpts)

# Shift by Fermi level
energies_shifted = energies - fermi

with open("band_structure.csv", "w") as f:
    header = "k_index"
    for b in range(nbands):
        header += f",band_{b+1}"
    f.write(header + "\n")

    for i in range(nkpts):
        line = f"{k_index[i]}"
        for b in range(nbands):
            line += f",{energies_shifted[i, b]}"
        f.write(line + "\n")

print("✅ band_structure.csv written successfully")
