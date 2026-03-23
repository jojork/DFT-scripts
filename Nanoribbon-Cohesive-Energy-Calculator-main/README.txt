⚙️ How to Use
Edit the script:

Set atomic energies:

E_A_atom = ...
E_B_atom = ...
Replace element labels "A" and "B" with your actual elements.

Run the script:

python script.py
🚀 What the Script Does
Builds nanoribbons by repeating the structure along x-direction
Adds vacuum spacing
Performs spin-polarized DFT calculations using GPAW
Reuses previous wavefunctions for faster convergence
Calculates cohesive energy for each system size
📊 Output

For each Nx:

Generated structure file: nanoribbon_Nx.xyz
GPAW output log: calc_Nx.txt
Restart file: calc_Nx.gpw

Terminal output:

Nx | A | B | Total Energy (eV) | Cohesive Energy
