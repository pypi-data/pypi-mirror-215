# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['covdrugsim',
 'covdrugsim.mdsim',
 'covdrugsim.qmcalc.runGaussian',
 'covdrugsim.qmcalc.unitConv',
 'covdrugsim.qmcalc.visAnalysis']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.0.2,<3.0.0',
 'seaborn>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'covdrugsim',
    'version': '0.1.0',
    'description': 'Quantum mechanical calculations and molecular dynamics simulations of covalent drugs',
    'long_description': '# covdrugsim\n\nQuantum mechanical calculations and molecular dynamics simulations of covalent drugs.\n\nWritten by Jonathan Yik Chang Ting (Student ID: 44254124) for UQ BAdSc(Hons) Honours Project 2019.\nProject Title: Molecular Modelling of Reversible Covalent Inhibition of Bruton’s Tyrosine Kinase by Cyanoacrylamides\n\n## Installation\n\n```bash\n$ pip install covdrugsim\n```\n\n## Usage\n\n`covdrugsim` can be used to conduct quantum mechanical calculations and molecular dynamics simulations as follows:\n\n```python\nfrom covdrugsim.qmCalc import qmCalc\nfrom covdrugsim.mdSim import mdSim\nimport matplotlib.pyplot as plt\n\nfilePath = "test.txt"  # Path to your file\nqmCalc(filePath)\nmdSim(filePath)\nplt.show()\n```\n\n\nDescriptions of source codes:\n### Quantum Mechanical Calculations (qmcalc)\n\n#### unitConv\nunitConv.py - Interconverts between kinetics and thermodynamic quantities (dGbarr, k, t_half, RT).\n\n#### runGaussian\nsettings.py - Contains variables for different type of Gaussian jobs that are used by prepGaussian.py.\nadmin.py - Group files with the same names (before extension, e.g. abc.inp is the same as abc.xyz) into individual directories.\nprepGaussian.py - Batch generation of Gaussian input files and job submission files on HPCs with PBS Scheduler.\ntabulate.py - Batch tabulation of interested values from Gaussian (version 16) output files into an Excel file.\ngsub.sh - Batch submission of Gaussian QM calculation jobs on HPCs.\n\nTypical work flow for a mechanism-based project where flexible molecules are involved would be:\n1) Conduct conformational searches on the species along the reaction coordinate (using MacroModel).\n2) Export all conformers within 3 kcal/mol of the lowest energy structure to a directory in .xyz format. The naming convention is very important, be consistent, but make sure each conformer has a different name (I do this by adding numbers at the end of their names, signifying their ranks from the conformational searches).\n3) Change your input directory in admin.py to where you store the coordinate files and run it. This will group all of the conformers into individual directories.\n4) Change your input directory in prepGaussian.py to the same location and run it. This will generate the Gaussian input files and job submission files in the corresponding directory. Make sure you check at least a few of the files generated to see that you got the charges, spacing at the end of file, solvents, resources requested, etc right. I named all of the Gaussian job submission jobs with *.sh, feel free to change it according to your preference (Line 52 in prepGaussian.py).\n5) Copy the directories across to the HPCs (Raijin/Gadi/Tinaroo/Awoonga, NOTE: The details for job submissions on Raijin and RCC HPCs are different, specify the cluster before running prepGaussian.py in Step 4).\n6) Change directory to the directory that contains all the conformers subdirectories and run \'gsub.sh\' (Make sure it\'s an executable, if you can\'t run it, use chmod to change it). This will submit all of the Gaussian submission jobs to the HPC. Note that prior to this you need to adjust Line 6 in the gsub.sh file to the naming convention you give to your Gaussian submit files if you have changed them in the prepGaussian.py.\n7) After the jobs are done, copy them over to your local machine.\n8) Change your input directory in tabulate.py to the directory that contains all the conformers and run it. Note that you need to have the Python package pandas installed for it to work.\n\n#### visAnalysis\nenergyLeveller.py - Draws energy profile diagrams.\nplotConfig.py - Stores configuration for figure-plotting functions.\nplotFigs.py - Plots figures for QM data analysis.\n\n\n### Molecular Dynamics Simulations (mdsim)\n- config.py contains some variables that are used repetitively for almost all files.\n- baseID.py plots the distances between potential base species and the targeted protons.\n- bbRMSD.py plots the RMSD of BTK backbones over time, for the purpose of checking the stability of the simulations.\n- hbondAnalysis.py plots the distribution of the number of hydrogen bonds between BTK backbones over time.\n- ligDihedral.py plots the distribution of the critical C=C-C=O dihedral angle near BTK active site over time.\n- SCbondDist.py plots the distances between the reacting S and C atoms over time.\n- sumCharge.py sums up the charges to aid in the parameterisation of non-standard amino acids.\n- prepMTB.py was written during an attempt to map the unbound ligand to covalently bound ligand. Was not utilised in the end.\n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`covdrugsim` was created by Jonathan Yik Chang Ting. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`covdrugsim` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Jonathan Yik Chang Ting',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
