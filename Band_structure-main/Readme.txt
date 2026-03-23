📂 Input
input_file.gpw → Ground-state file (must be pre-converged)
⚙️ Methodology
A manual k-path is constructed using fractional k-points
Band energies are calculated along high-symmetry directions
Energies are shifted relative to the Fermi level
Results are saved in both graphical and tabular formats
🚀 Usage
python band_structure.py
📊 Output
band_structure.png → Band structure plot
band_structure.csv → Numerical band data
band_structure.txt → GPAW calculation log
⚠️ Notes
Ensure the .gpw file is converged before running
Modify k-point path as per crystal symmetry if required
Suitable for low-dimensional and periodic systems
