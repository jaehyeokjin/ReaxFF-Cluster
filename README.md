# Time Correlation Analysis with Clustering

**Authors:** Jaehyeok Jin and Youngbae Jeon

This repository contains a Python script that performs time correlation analysis, clustering, and manipulation of trajectory data from molecular simulations. The script utilizes `networkx` for graph analysis to identify clusters in the simulation and processes the trajectory data accordingly.

## Features

- Reads molecular trajectory files (`simulate.trj` and `reax_interface_npt.lammpstrj`).
- Applies clustering techniques to identify connected components or cycles in molecular data.
- Outputs the processed clusters in different cases (`cluster_casea.lammpstrj`, `cluster_caseb.lammpstrj`, `cluster_casec.lammpstrj`).
- Supports multiple clustering cases with customizable thresholds.

## Requirements

- Python 3.x
- `networkx`

To install the required packages, run:
`pip install networkx`

## Usage

### Input Files
The script reads from two input files:
- `simulate.trj`: The primary trajectory file.
- `reax_interface_npt.lammpstrj`: The processed output file.

### Cluster Cases
- **case_a**: Processes cluster data using connected components.
- **case_b**: Adds a threshold for clustering (default: 6).
- **case_c**: Uses directed graph cycles to identify clusters.

### Editable Parameters
- **case**: Select the clustering case (`case_a`, `case_b`, `case_c`).
- **bond_dist**: Adjust the bond distance threshold (default: 0.1).

### Output Files
- Clustering results are written to:
  - `cluster_casea.lammpstrj`, `cluster_caseb.lammpstrj`, `cluster_casec.lammpstrj` depending on the case.
- The cluster length results are stored in `cluster_result.out`.

### Running the Script
To run the script, simply execute it with Python:
`python script.py`
Make sure to set the appropriate case and bond distance values inside the script before execution.

## Notes
- The script processes large files and may take time depending on the dataset.
- The processed clusters are written back to the output file, allowing further post-processing or visualization.
- Ensure the input trajectory files are formatted correctly for smooth execution.
