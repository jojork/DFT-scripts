import numpy as np
import matplotlib.pyplot as plt
from ase.io import read

# --------------------------------------------------
# 1) Read structure
# --------------------------------------------------
atoms = read("Your_structure.vasp")

# --------------------------------------------------
# 2) Get reciprocal lattice vectors
# --------------------------------------------------
rec_cell = atoms.cell.reciprocal()
b1 = rec_cell[0][:2]
b2 = rec_cell[1][:2]

# --------------------------------------------------
# 3) Define high-symmetry points (fractional → cartesian)
# --------------------------------------------------
G = np.array([0.0, 0.0])
X = 0.5 * b1
Y = 0.5 * b2
M = 0.5 * (b1 + b2)

points = {
    r"$\Gamma$": G,
    "X": X,
    "Y": Y,
    "M": M
}

# --------------------------------------------------
# 4) Build Brillouin Zone (rectangle)
# --------------------------------------------------
BZ = np.array([
    -0.5 * b1 - 0.5 * b2,
     0.5 * b1 - 0.5 * b2,
     0.5 * b1 + 0.5 * b2,
    -0.5 * b1 + 0.5 * b2,
    -0.5 * b1 - 0.5 * b2
])

# --------------------------------------------------
# 5) Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 6))

# Plot BZ
ax.plot(BZ[:, 0], BZ[:, 1], "k-", lw=2)

# Plot high-symmetry points
for label, p in points.items():
    ax.scatter(p[0], p[1], s=80)
    ax.text(p[0]*1.05, p[1]*1.05, label, fontsize=14)

# Draw symmetry path Γ-X-M-Y-Γ
path = [G, X, M, Y, G]
path = np.array(path)
ax.plot(path[:, 0], path[:, 1], "r--", lw=1)

# --------------------------------------------------
# 6) Plot settings
# --------------------------------------------------
ax.set_aspect("equal")
ax.set_xlabel(r"$k_x$")
ax.set_ylabel(r"$k_y$")
ax.set_title("2D Rectangular Brillouin Zone & High-Symmetry Points")

ax.grid(True)
plt.tight_layout()
plt.savefig("BZ_high_symmetry.png", dpi=300)
plt.show()
