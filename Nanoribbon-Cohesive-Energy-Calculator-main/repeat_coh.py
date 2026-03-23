from ase.io import read, write
from ase.build import make_supercell
import numpy as np
import os

from gpaw import GPAW, FermiDirac
from ase.parallel import parprint

# =====================================
# ATOMIC ENERGIES (EDITABLE BY USER)
# =====================================
E_A_atom = -0.1   # replace with your element A energy
E_B_atom = -0.1   # replace with your element B energy

# =====================================
# LOAD STRUCTURE
# =====================================
atoms_input = read("input_structure.xyz")   # generic name

a_x = atoms_input.cell[0, 0]
vacuum_x = 10.0

parprint("\nNx | A | B | Total_Energy(eV) | Cohesive_Energy")
parprint("--------------------------------------------------")

for Nx in range(1, 30):

    if os.path.exists(f"calc_{Nx}.txt"):
        parprint(f"Nx {Nx} already done — skipping")
        continue

    # =====================================
    # BUILD NANORIBBON
    # =====================================
    T = np.array([[Nx, 0, 0], [0, 1, 0], [0, 0, 1]])
    nanoribbon = make_supercell(atoms_input, T)

    # =====================================
    # ADD VACUUM
    # =====================================
    new_cell = nanoribbon.get_cell()
    new_cell[0, 0] = Nx * a_x + 2 * vacuum_x

    nanoribbon.positions[:, 0] += vacuum_x
    nanoribbon.set_cell(new_cell)

    write(f"nanoribbon_{Nx}.xyz", nanoribbon)

    # =====================================
    # COUNT ATOMS (generic labels)
    # =====================================
    symbols = nanoribbon.get_chemical_symbols()
    N_A = symbols.count("A")   # user should adapt
    N_B = symbols.count("B")   # user should adapt
    N_total = len(symbols)

    # =====================================
    # MAGNETIC MOMENTS (kept same style)
    # =====================================
    magmoms = []
    for s in symbols:
        if s == "A":     # user-defined magnetic element
            magmoms.append(3.0)
        else:
            magmoms.append(0.0)

    nanoribbon.set_initial_magnetic_moments(magmoms)

    # =====================================
    # GPAW CALCULATION (UNCHANGED)
    # =====================================
    if Nx == 1:
        calc = GPAW(
            mode='lcao',
            basis='dzp',
            xc='PBE',
            kpts=(1, 15, 1),
            occupations=FermiDirac(0.1),
            spinpol=True,
            symmetry='off',
            maxiter=300,
            txt=f"calc_{Nx}.txt"
        )
    else:
        calc = GPAW(
            f"calc_{Nx-1}.gpw",
            kpts=(1, 15, 1),
            occupations=FermiDirac(0.3),
            txt=f"calc_{Nx}.txt"
        )

    nanoribbon.calc = calc
    total_energy = nanoribbon.get_potential_energy()

    calc.write(f"calc_{Nx}.gpw")

    # =====================================
    # COHESIVE ENERGY
    # =====================================
    cohesive_energy = (
        total_energy - (N_A * E_A_atom + N_B * E_B_atom)
    ) / N_total

    parprint(f"{Nx:2d} | {N_A:3d} | {N_B:3d} | {total_energy:14.6f} | {cohesive_energy:12.6f}")

parprint("\nAll calculations finished.")
