📂 Input

input_structure.vasp → Relaxed structure file
⚙️ Methodology
Read relaxed structure
Generate supercell and atomic displacements
Compute forces for each displaced configuration
Construct force constants
Calculate phonon frequencies at Gamma point
Compute phonon dispersion along high-symmetry path
Export results and generate plots
🚀 Usage
python phonon_script.py
📊 Output (inside phonopy_outputs/)
forces_summary.csv → Force and energy summary
gamma_frequencies.csv → Gamma-point frequencies
phonon_bands.csv → Band structure data
phonon_bandstructure.png → Phonon dispersion plot
phonopy_params.yaml → Phonopy parameters
checkpoint.pkl → Restart checkpoint
progress_log.txt → Detailed log
⚠️ Notes
Input structure must be fully relaxed
Imaginary frequencies indicate structural instability
Adjust supercell size and k-points for accuracy
Checkpoint allows restarting interrupted calculations
