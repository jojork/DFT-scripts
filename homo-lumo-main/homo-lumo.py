import numpy as np
import matplotlib.pyplot as plt
import csv
from gpaw import GPAW

# ------------------------------------------------------------
# Load ground state
# ------------------------------------------------------------
calc = GPAW('your_structure.gpw', txt=None)
atoms = calc.get_atoms()

fermi_raw = calc.get_fermi_level()
print(f"Raw Fermi level = {fermi_raw:.3f} eV")

# ------------------------------------------------------------
# HOMO–LUMO calculation (CORRECT)
# ------------------------------------------------------------
eigs_raw = calc.get_eigenvalues()

# Shift eigenvalues so that EF = 0
eigs = eigs_raw - fermi_raw

fermi = 0.0

homo = np.max(eigs[eigs < 0.0])
lumo = np.min(eigs[eigs > 0.0])
gap = lumo - homo

print(f"Fermi level = {fermi:.3f} eV")
print(f"HOMO = {homo:.3f} eV")
print(f"LUMO = {lumo:.3f} eV")
print(f"HOMO–LUMO gap = {gap:.3f} eV")


# ------------------------------------------------------------
# Save CSV files
# ------------------------------------------------------------

# 1. HOMO & LUMO levels
with open("homo_lumo_levels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Level", "Energy_eV"])
    writer.writerow(["HOMO", homo])
    writer.writerow(["LUMO", lumo])

# 2. HOMO–LUMO gap
with open("homo_lumo_gap.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Quantity", "Value_eV"])
    writer.writerow(["HOMO-LUMO Gap", gap])

print("CSV files saved successfully.")

# ------------------------------------------------------------
# Plot HOMO & LUMO energy levels
# ------------------------------------------------------------
plt.figure(figsize=(4, 6))

plt.hlines(homo, 0.9, 1.1, linewidth=3, label="HOMO")
plt.hlines(lumo, 0.9, 1.1, linewidth=3, label="LUMO")
plt.hlines(fermi, 0.85, 1.15, linestyles="dashed", label="Fermi level")

plt.text(1.12, homo, f"{homo:.2f} eV", va="center")
plt.text(1.12, lumo, f"{lumo:.2f} eV", va="center")

plt.xlim(0.8, 1.4)
plt.ylabel("Energy (eV)")
plt.xticks([])
plt.title("HOMO–LUMO Energy Levels")
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Plot HOMO–LUMO gap
# ------------------------------------------------------------
plt.figure(figsize=(4, 4))
plt.bar(["HOMO–LUMO Gap"], [gap])
plt.ylabel("Energy (eV)")
plt.title("HOMO–LUMO Gap")
plt.tight_layout()
plt.show()
