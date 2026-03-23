import numpy as np
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from ase.io import read
from ase import Atoms
from gpaw import GPAW, PW, FermiDirac, mpi
import matplotlib.pyplot as plt
import os
import pickle
from datetime import datetime

# ==================================================
# MPI INFO
# ==================================================
rank = mpi.world.rank
size = mpi.world.size

# ==================================================
# OUTPUT SETUP
# ==================================================
if rank == 0:
    os.makedirs("phonopy_outputs", exist_ok=True)

CHECKPOINT_FILE = "phonopy_outputs/checkpoint.pkl"

if rank == 0:
    progress_log = open("phonopy_outputs/progress_log.txt", "a")
else:
    progress_log = None


def log(message):
    if rank == 0:
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        print(full_message)
        progress_log.write(full_message + "\n")
        progress_log.flush()


def save_checkpoint(stage, data):
    if rank == 0:
        checkpoint = {'stage': stage, 'data': data}
        with open(CHECKPOINT_FILE, 'wb') as f:
            pickle.dump(checkpoint, f)
        log(f"✓ Checkpoint saved: {stage}")


def load_checkpoint():
    if rank == 0 and os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'rb') as f:
            return pickle.load(f)
    return None


# ==================================================
# START MESSAGE
# ==================================================
if rank == 0:
    print("=" * 60)
    print(f"Running with {size} MPI cores")
    print("=" * 60)

checkpoint = load_checkpoint()

if checkpoint:
    log("=" * 60)
    log(f"RESUMING FROM CHECKPOINT: {checkpoint['stage']}")
    log("=" * 60)
else:
    log("=" * 60)
    log("STARTING NEW PHONON CALCULATION")
    log("=" * 60)

# ==================================================
# 1) READ STRUCTURE
# ==================================================
ase_atoms = read("input_structure.vasp")   # generic name
log(f"Structure: {ase_atoms.get_chemical_formula()}, {len(ase_atoms)} atoms")

phonopy_atoms = PhonopyAtoms(
    symbols=ase_atoms.get_chemical_symbols(),
    cell=ase_atoms.cell,
    scaled_positions=ase_atoms.get_scaled_positions()
)

# ==================================================
# 2) CREATE PHONOPY OBJECT
# ==================================================
phonon = Phonopy(
    phonopy_atoms,
    supercell_matrix=[[3, 0, 0],
                      [0, 3, 0],
                      [0, 0, 1]],
)

log(f"Supercell: {len(phonon.supercell.symbols)} atoms")
phonon.generate_displacements(distance=0.01)
log(f"Number of displacements: {len(phonon.displacements)}")
log("")

supercells = phonon.supercells_with_displacements

# ==================================================
# 3) FORCE CALCULATIONS
# ==================================================
if checkpoint and checkpoint['stage'] == 'forces_done':
    forces_list = checkpoint['data']['forces_list']
    energies_list = checkpoint['data']['energies_list']
    log(f"✓ Loaded {len(forces_list)} force calculations")
else:
    log("=" * 60)
    log("CALCULATING FORCES")
    log("=" * 60)

    calc = GPAW(
        mode=PW(600),
        xc="PBE",
        kpts=(4, 4, 1),
        occupations=FermiDirac(0.01),
        symmetry="off",
        txt="phonopy_outputs/gpaw_calculation.txt"
    )

    forces_list = []
    energies_list = []

    if rank == 0:
        forces_csv = open("phonopy_outputs/forces_summary.csv", "w")
        forces_csv.write("ID,Energy_eV,Max_Force,Mean_Force\n")

    for i, scell in enumerate(supercells):
        log(f"Displacement {i+1}/{len(supercells)}")

        ase_scell = Atoms(
            symbols=scell.symbols,
            scaled_positions=scell.scaled_positions,
            cell=scell.cell,
            pbc=True
        )

        ase_scell.calc = calc
        energy = ase_scell.get_potential_energy()
        forces = ase_scell.get_forces()

        forces_list.append(forces)
        energies_list.append(energy)

        max_force = np.max(np.abs(forces))
        mean_force = np.mean(np.abs(forces))

        log(f"  Energy: {energy:.6f} eV")
        log(f"  Max force: {max_force:.6f} eV/A")
        log("")

        if rank == 0:
            forces_csv.write(f"{i},{energy:.8f},{max_force:.8f},{mean_force:.8f}\n")

    if rank == 0:
        forces_csv.close()

    save_checkpoint('forces_done', {
        'forces_list': forces_list,
        'energies_list': energies_list
    })

# ==================================================
# 4) FORCE CONSTANTS
# ==================================================
log("BUILDING FORCE CONSTANTS")
phonon.forces = forces_list
phonon.produce_force_constants()
log("✓ Force constants calculated")

# ==================================================
# 4.1) WRITE PHONON ANIMATION
# ==================================================
if rank == 0:
    log("WRITING PHONON ANIMATION")

    try:
        phonon.write_animation(
            q_point=[0, 0, 0],
            anime_type='xyz',
            band_index=0,
            amplitude=0.3,
            filename="phonopy_outputs/anime.xyz"
        )

        log("✓ Animation saved: phonopy_outputs/anime.xyz")

    except Exception as e:
        log(f"Animation generation failed: {e}")

# ==================================================
# 5) GAMMA FREQUENCIES
# ==================================================
log("GAMMA-POINT FREQUENCIES")

phonon.run_mesh([20, 20, 1])
gamma_freqs = phonon.get_mesh_dict()['frequencies'][0]

if rank == 0:
    gamma_csv = open("phonopy_outputs/gamma_frequencies.csv", "w")
    gamma_csv.write("Mode,THz,cm^-1\n")

for i, f in enumerate(gamma_freqs):
    cm_inv = f * 33.356
    log(f"{i:3d}  {f:12.6f} THz  {cm_inv:10.2f} cm^-1")

    if rank == 0:
        gamma_csv.write(f"{i},{f:.8f},{cm_inv:.4f}\n")

if rank == 0:
    gamma_csv.close()

if np.any(gamma_freqs < -0.01):
    log("⚠ Imaginary frequencies detected")
else:
    log("✓ All Gamma frequencies positive")

# ==================================================
# 6) BAND STRUCTURE
# ==================================================
log("CALCULATING BAND STRUCTURE")

path = [
    [[0,0,0],[0.5,0,0]],
    [[0.5,0,0],[0.5,0.5,0]],
    [[0.5,0.5,0],[0,0.5,0]],
    [[0,0.5,0],[0,0,0]]
]

phonon.run_band_structure(path, 51)
bs = phonon.get_band_structure_dict()

# ==================================================
# 7) PLOT
# ==================================================
if rank == 0:
    distances = np.concatenate(bs['distances'])
    freqs = np.concatenate(bs['frequencies']) * 33.356

    fig, ax = plt.subplots(figsize=(8,6))

    for i in range(freqs.shape[1]):
        ax.plot(distances, freqs[:, i], 'b-')

    ax.axhline(0, color='k', linestyle='--', linewidth=0.5)
    ax.set_xlabel("Wave vector")
    ax.set_ylabel("Frequency (cm$^{-1}$)")
    ax.set_title("Phonon Band Structure")
    ax.set_ylim(-200, 1000)

    plt.tight_layout()
    plt.savefig("phonopy_outputs/phonon_bandstructure.png", dpi=300)
    plt.show()

    phonon.save("phonopy_outputs/phonopy_params.yaml")

    log("=" * 60)
    log("COMPLETE")
    log("=" * 60)

    progress_log.close()

    print("\n✓ All outputs saved in phonopy_outputs/")
