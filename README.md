# DFT-Scripts

A collection of Python scripts developed to assist with **Density Functional Theory (DFT)** simulations and post-processing analyses of **2D materials and nanomaterials**.

These scripts are primarily designed for computational materials science research using first-principles methods.

## Features

This repository currently includes scripts for:

* **Band Structure Calculations**

  * Generation and analysis of electronic band structures.

* **Brillouin Zone High-Symmetry Points**

  * Tools for defining and generating high-symmetry k-point paths.

* **Density of States (DOS)**

  * Scripts for calculating and plotting total and projected density of states.

* **Minimum Energy Calculations**

  * Utilities for determining optimized structures and minimum-energy configurations.

* **Nanoribbon Cohesive Energy Calculations**

  * Calculation of cohesive energies for low-dimensional nanostructures.

* **Phonon Band Structure**

  * Post-processing and visualization tools for phonon dispersion calculations.

* **Structural Relaxation for Phonon Calculations**

  * Structure optimization workflows prior to phonon calculations.

* **Bond Length and Bond Energy Analysis**

  * Automated extraction and analysis of bond characteristics.

* **Quantum Capacitance**

  * Computation and visualization of quantum capacitance from electronic density of states.

* **HOMO-LUMO Analysis**

  * Extraction and analysis of HOMO-LUMO gaps.

## Repository Structure

```text
DFT-scripts/
│
├── Band_structure-main/
├── Brillouin-Zone-high-symmetry-points-main/
├── Density-of-states-main/
├── Min_energy-main/
├── Nanoribbon-Cohesive-Energy-Calculator-main/
├── Phonon_band_structure-main/
├── Quantum_capacitance-main/
├── Relax-structure-for-phonon-band-structure/
├── bond_length-and-bond-energy-main/
└── homo-lumo-main/
```

## Requirements

Most scripts require Python 3 and commonly used scientific libraries such as:

* NumPy
* Matplotlib
* ASE (Atomic Simulation Environment)
* GPAW
* SciPy

Install dependencies using:

```bash
pip install numpy matplotlib scipy ase
```

## Intended Use

These scripts are intended for researchers and students working in:

* Computational Materials Science
* Density Functional Theory (DFT)
* Condensed Matter Physics
* Nanomaterials Research
* 2D Materials Research

## Disclaimer

These scripts were developed for research purposes and may require modification depending on the simulation package, material system, or computational workflow being used.

## Author

**Rohit Kumar**

MSc Physics | Computational Materials Science

Interests: DFT, 2D Materials, Nanomaterials, Electronic Structure, Python Development

GitHub: https://github.com/jojork
