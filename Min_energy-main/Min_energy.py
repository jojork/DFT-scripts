#Here's the script of finding the minimum energy of a element
from ase import Atoms
import numpy as np
import matplotlib.pyplot as plt
from gpaw import GPAW, FermiDirac

vacua = np.linspace(3.0, 12.0, 6)
energies = []

for vac in vacua:
    ag = Atoms('Ag',
               positions=[[0, 0, 0]],
               pbc=False)

    # THIS creates the cell correctly
    ag.center(vacuum=vac)

    calc = GPAW(mode='lcao',
                basis='dzp',
                xc='PBE',
                occupations=FermiDirac(0.1),
                txt=f'ag_lcao_vac{vac:.1f}.log')

    ag.calc = calc
    energy = ag.get_potential_energy()
    energies.append(energy)

    print(f'Vacuum: {vac:.1f} Å --> Energy: {energy:.6f} eV')

# Plot
plt.figure()
plt.plot(vacua, energies, 'o-')
plt.xlabel('Vacuum (Å)')
plt.ylabel('Total Energy (eV)')
plt.title('Total Energy of Isolated Ag Atom vs Vacuum (LCAO)')
plt.grid(True)
plt.tight_layout()
plt.show()
