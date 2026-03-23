import numpy as np
import matplotlib.pyplot as plt
from gpaw import GPAW, FermiDirac
from ase.io import read
import csv

# ------------------------------------------------------------
# LOAD STRUCTURE
# ------------------------------------------------------------
atoms = read('fle_name.xyz')

# ------------------------------------------------------------
# DEFINE CALCULATOR
# ------------------------------------------------------------
calc = GPAW(
    mode='lcao',
    basis='dzp',
    xc='PBE',
    kpts=(15, 15, 1),              # adjust if needed
    occupations=FermiDirac(0.01),
    spinpol=True,
    symmetry='off',
    txt='dos_run.log'
)

atoms.calc = calc

# ------------------------------------------------------------
# RUN CALCULATION
# ------------------------------------------------------------
atoms.get_potential_energy()

Ef = calc.get_fermi_level()

# ------------------------------------------------------------
# DOS PARAMETERS
# ------------------------------------------------------------
npts = 2000
width = 0.1

# ------------------------------------------------------------
# TOTAL DOS
# ------------------------------------------------------------
energy, dos = calc.get_dos(npts=npts, width=width)

# shift Fermi level to 0
energy -= Ef

# ------------------------------------------------------------
# FILTER ENERGY RANGE (-5 to +5 eV)
# ------------------------------------------------------------
mask = (energy >= -5) & (energy <= 5)
energy = energy[mask]
dos = dos[mask]

# ------------------------------------------------------------
# SAVE CSV
# ------------------------------------------------------------
with open('dos_total.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Energy_eV', 'DOS'])

    for e, d in zip(energy, dos):
        writer.writerow([f'{e:.6f}', f'{d:.6e}'])

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(8,6))
plt.plot(energy, dos, color='red', linewidth=1.5)

# Fermi level line
plt.axvline(0, linestyle='--', color='black', linewidth=1)

plt.xlabel('Energy - Ef (eV)')
plt.ylabel('DOS (states/eV)')
plt.title('Total DOS (-5 to +5 eV)')

plt.xlim(-5, 5)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('dos.png', dpi=300)
plt.show()

print("✅ DOS calculated (range: -5 to +5 eV)")
