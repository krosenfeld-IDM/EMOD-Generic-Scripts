# EMOD-Generic-Scripts

See documentation at https://docs.idmod.org/projects/emod-generic-scripts/en/latest/ for
additional information about how to use these scripts.

---------------------

## Contents:

| Directory | Description |
| --- | --- |
| env_Alma9 <br /> env_Debian12 <br /> env_Fedora40 <br /> env_Rocky9 <br /> env_Ubuntu24 |  Contains the definition scripts for singularity containers. Produces the the EMOD executable, schema, and custom reporters; creates an environment for running EMOD on COMPS and contains the python packages available to the embedded python interpreter. All files remain on COMPS and are provided to the various workflows as Asset Collection IDs. |
| local_python             | Contains additional python scripts with helper functions common to all of the workflows. |
| model_covariance01       | [Demonstration simulations for heterogeneity in individual behavior.](https://docs.idmod.org/projects/emod-generic-scripts/en/latest/examples/model_covariance01.html) |
| model_covid01            | Baseline simulations for SARS-CoV-2 in EMOD. Collab with MvG. |
| model_demographics01     | Example demographics for UK measles simulations. |
| model_demographics02     | Example demographics using UN WPP data as inputs. |
| model_measles_cod01      | Documentation. |
| model_measles_gha01      | Examination of RDT use and responsive campaigns for measles using Ghana as an example context. |
| model_measles_nga01      | Documentation. |
| model_measles_nga02      | Documentation. |
| model_measles01          | Documentation. |
| model_network01          | Demonstration of the network infectivity feature. |
| model_polio_nga01        | Example outbreak simulations for cVDPV2 in Nigeria. Collab with JG and HL. |
| model_rubella01          | Projections of rubella infections and estimates of CRS burden following RCV introduction.  |
| model_transtree01        | [Demonstration of the infector labeling feature and generation of explicit transmission networks.](https://docs.idmod.org/projects/emod-generic-scripts/en/latest/examples/model_transtree01.html) |
| refdat_mcv1              | IHME MCV1 coverage estimates used to construct input files for EMOD simulations. |
| refdat_namesets          | Namesets used for region identification. |
| refdat_poppyr            | UN WPP age structured population estimates used to construct input files for EMOD simulations. |
| refdat_sias              | Documentation. |

---------------------

To get started:

1. Setup a virtual environment (e.g., conda)

2. Install requirements:
   ```
   pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
   ```

3. Run an experiment (requires COMPS credentials):
   ```
   cd EMOD-Generic-Scripts/model_covariance01/experiment_covariance01
    python make01_param_dict.py
    python make02_lauch_sims.py
    python make03_pool_brick.py
    ```

4. Make figures:
    ```
    cd EMOD-Generic-Scripts/model_covariance01/figure_attackfrac01
    python make_fig_attackrate.py
   ```

---------------------

To build the documentation locally, do the following:

1. Create and activate a venv.

2. Navigate to the root directory of the repo and enter the following

    ```
    pip install -r docs/requirements.txt
    ```

-------------------