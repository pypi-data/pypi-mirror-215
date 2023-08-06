# gdsfactory 6.107.5

[![docs](https://github.com/gdsfactory/gdsfactory/actions/workflows/pages.yml/badge.svg)](https://gdsfactory.github.io/gdsfactory/)
[![PyPI](https://img.shields.io/pypi/v/gdsfactory)](https://pypi.org/project/gdsfactory/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/gdsfactory.svg)](https://anaconda.org/conda-forge/gdsfactory)
[![Dockerhub](https://img.shields.io/docker/pulls/joamatab/gdsfactory)](https://hub.docker.com/r/joamatab/gdsfactory)
[![PyPI Python](https://img.shields.io/pypi/pyversions/gdsfactory.svg)](https://pypi.python.org/pypi/gdsfactory)
[![issues](https://img.shields.io/github/issues/gdsfactory/gdsfactory)](https://github.com/gdsfactory/gdsfactory/issues)
[![forks](https://img.shields.io/github/forks/gdsfactory/gdsfactory.svg)](https://github.com/gdsfactory/gdsfactory/network/members)
[![GitHub stars](https://img.shields.io/github/stars/gdsfactory/gdsfactory.svg)](https://github.com/gdsfactory/gdsfactory/stargazers)
[![Downloads](https://pepy.tech/badge/gdsfactory)](https://pepy.tech/project/gdsfactory)
[![Downloads](https://pepy.tech/badge/gdsfactory/month)](https://pepy.tech/project/gdsfactory)
[![Downloads](https://pepy.tech/badge/gdsfactory/week)](https://pepy.tech/project/gdsfactory)
[![MIT](https://img.shields.io/github/license/gdsfactory/gdsfactory)](https://choosealicense.com/licenses/mit/)
[![codecov](https://img.shields.io/codecov/c/github/gdsfactory/gdsfactory)](https://codecov.io/gh/gdsfactory/gdsfactory/tree/main/gdsfactory)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gdsfactory/binder-sandbox/HEAD)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gdsfactory/gdsfactory)

![logo](https://i.imgur.com/v4wpHpg.png)

gdsfactory: An open source platform for end to-end chip design and validation.

gdsfactory is a python library to design chips (Photonics, Analog, Quantum, MEMs, ...), objects for 3D printing or PCBs.

You can describe your hardware in code (python or YAML), verify it (DRC, simulation, extraction) and validate it (to make sure it meets your specifications after fabrication).

![workflow](https://i.imgur.com/abvxJJw.png)

It provides you and end to end design flow to:

- Design (Layout, Simulation, Optimization)
  - Define Components using parametric cells functions in python or YAML.
  - Test component settings, ports and geometry to avoid unwanted regressions.
  - Capture design intent in a schematic.
- Verify (DRC, DFM, LVS)
  - Run simulations directly from the layout thanks to the simulation interfaces. No need to draw the geometry more than once.
    - Run Component simulations (solve modes, FDTD, EME, TCAD, thermal ...)
    - Run Circuit simulations from the Component netlist (Sparameters, Spice ...)
    - Build Component models and study Design For Manufacturing.
  - Create DRC rule decks in Klayout.
  - Ensure complex layouts match their design intent (Layout Versus Schematic).
- Validate
  - Define layout and test protocols simultaneously, so when the chips come back you already know how to test and analyze them.
  - Model extraction: extract the important parameters for each component.
  - Build a data pipeline from raw data, to structured data and dashboards for monitoring your chip performance.

As input, you write python or YAML code.

As output you write a GDSII or OASIS file that you can send to your foundry for fabrication.
It also exports component settings (for measurement and data analysis) and netlists (for circuit simulations) in YAML.

![layout_to_components](https://i.imgur.com/S96RSil.png)

![flow](https://i.imgur.com/XbhWJDz.png)

It provides you a common syntax for design (KLayout, gdstk, Ansys Lumerical, tidy3d, MEEP, MPB, DEVSIM, SAX, MEOW ...), verification and validation.

![tool interfaces](https://i.imgur.com/9fNLRvJ.png)

Multiple foundries have gdsfactory PDKs available. Talk to your foundry to access their gdsfactory PDK as some are only provided under NDA:

- AIM photonics PDK
- AMF photonics PDK
- TowerSemi PH18 photonics PDK
- GlobalFoundries 45SPCLO Photonics PDK
- IMEC photonics PDK
- [GlobalFoundries 180nm MCU CMOS PDK](https://gdsfactory.github.io/gf180/) (open source)
- [SiEPIC Ebeam UBC PDK](https://gdsfactory.github.io/ubc) (open source)
- [Skywater130 CMOS PDK](https://gdsfactory.github.io/skywater130) (open source)

You can also access:

- instructions on [how to build your own PDK](https://gdsfactory.github.io/gdsfactory/notebooks/08_pdk.html)
- instructions on [how to import a PDK from a library of fixed GDS cells](https://gdsfactory.github.io/gdsfactory/notebooks/09_pdk_import.html)

## Installation

Use python3.10 or python3.11, as some tools like kfactory are not available for older versions of python. We recommend [VSCode](https://code.visualstudio.com/) as an IDE.

You have 2 options to install gdsfactory:


### 1. Installation for new users

If you don't have python installed on your system you can [download the gdsfactory installer](https://github.com/gdsfactory/gdsfactory/releases) that includes python3, miniconda and gdsfactory.

You can also install python with mamba package manager (faster than conda):

| OS      | Architecture          | Download  |
| --------|-----------------------|-----------|
| Linux   | x86_64 (amd64)        | [Linux-x86_64](https://github.com/gdsfactory/gdsfactory/releases/latest/download/Mambaforge-Linux-x86_64.sh) |
| OS X    | x86_64                | [MacOSX-x86_64](https://github.com/gdsfactory/gdsfactory/releases/latest/download/Mambaforge-MacOSX-x86_64.sh) |
| OS X    | arm64 (Apple Silicon) | [MacOSX-arm64](https://github.com/gdsfactory/gdsfactory/releases/latest/download/Mambaforge-MacOSX-arm64.sh) |
| Windows | x86_64                | [Windows-x86_64](https://github.com/gdsfactory/gdsfactory/releases/latest/download/Mambaforge-Windows-x86_64.exe) |


Once you have python installed, open Anaconda Prompt and then install the latest gdsfactory using pip.

![anaconda prompt](https://i.imgur.com/Fyal5sT.png)

```
conda install gdstk -y
pip install "gdsfactory[full]" --upgrade
```

Then you can install Klayout-live `klive` integration in the klayout GUI `Tools --> Manage Packages --> Install New Packages --> Klive` as well as the genericpdk layermap `Tools --> Manage Packages --> Install New Packages --> gdsfactory` and restart klayout.

### 2. Installation for developers

As a developer, if you are on windows you need to download [Git](https://git-scm.com/download/win) and optionally [GitHub Desktop](https://desktop.github.com/).

Then you need to fork the [GitHub repository](https://github.com/gdsfactory/gdsfactory), git clone it (download it), git add, git commit, git push your improvement. Then pull request your changes to the main branch from the GitHub website.
For that you can install gdsfactory locally on your computer in `-e` edit mode.

```
git clone https://github.com/gdsfactory/gdsfactory.git
cd gdsfactory
mamba install gdstk -y
pip install -e .[full] pre-commit
pre-commit install
```

### Update gdsfactory

- Users can `pip install gdsfactory --upgrade`
- Developers can `git pull` the GitHub repository you downloaded and installed on your computer.

Some PDKs may require a specific versions of gdsfactory, so make sure you install the correct gdsfactory version specified in the `pyproject.toml` file. This will automatically happen when you install gdsfactory as one of the PDK dependencies. For example `pip install gf180` will install the latest gdsfactory version that has been tested for the GlobalFoundries180 PDK.


This code will tell you which gdsfactory you are using:

```
import gdsfactory as gf

gf.config.print_version()
```

### Docker container

Alternatively, one may use the pre-built Docker image from [hub.docker.com/r/joamatab/gdsfactory](https://hub.docker.com/r/joamatab/gdsfactory) or build it yourself with:

```bash
docker build -t joamatab/gdsfactory .
```
For example, VS Code supports development inside a container, see [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers) for details.


### Plugins

You can install all plugins with:

```
pip install "gdsfactory[full]" --upgrade
```

Or Install only the plugins you need `pip install gdsfactory[plugin1,plugin2]` from the available plugins:

- `cad` 3D rendering, 3D meshing, klayout.
- `database` for simulation and measurement database.
- `devsim` TCAD device simulator.
- `femwell` Finite Element Method Solver (heaters, modes, TCAD, RF waveguides).
- `gmsh` mesh structures.
- `kfactory` for fill, dataprep and testing.
- `meow` Eigen Mode Expansion (EME).
- `ray` for distributed computing and optimization.
- `sax` Sparameter circuit solver.
- `tidy3d` Finite Difference Time Domain (FDTD) simulations on the cloud using GPU.

To install open source FDTD Meep you need to use `conda` or `mamba` on MacOS or Linux, so for Windows you need to use the [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install).
- `conda install pymeep=*=mpi_mpich_* -y`

## Plugins

* [Optimization](https://gdsfactory.github.io/gdsfactory/plugins_optimization.html)
  - [Ray Tune Generic Black-Box Optimiser](https://gdsfactory.github.io/gdsfactory/notebooks/ray/optimiser.html)
* [Meshing](https://gdsfactory.github.io/gdsfactory/notebooks/devsim/01_pin_waveguide.html#Meshing)
* [Device Simulators](https://gdsfactory.github.io/gdsfactory/plugins_process.html)
  - [Thermal Simulation](https://gdsfactory.github.io/gdsfactory/notebooks/thermal/thermal.html)
  - [DEVSIM TCAD Simulation](https://gdsfactory.github.io/gdsfactory/notebooks/devsim/01_pin_waveguide.html)
  - [Analytical Process Simulation](https://gdsfactory.github.io/gdsfactory/notebooks/tcad/02_analytical_process.html)
  - [Montecarlo Implant Simulation](https://gdsfactory.github.io/gdsfactory/notebooks/tcad/03_numerical_implantation.html)
* [Mode Solvers & Eigenmode Expansion (EME)](https://gdsfactory.github.io/gdsfactory/plugins_mode_solver.html)
  - Finite Element Mode Solvers
    - [Femwell](https://gdsfactory.github.io/gdsfactory/notebooks/fem/01_mode_solving.html)
  - Finite Difference Mode Solvers
    - [tidy3d](https://gdsfactory.github.io/gdsfactory/notebooks/tidy3d/01_tidy3d_modes.html)
    - [MPB](https://gdsfactory.github.io/gdsfactory/notebooks/mpb/001_mpb_waveguide.html)
  - Eigenmode Expansion (EME)
    - [MEOW](https://gdsfactory.github.io/gdsfactory/notebooks/eme/01_meow.html)
* [Electromagnetic Wave Solvers using Finite Difference Time Domain (FDTD)](https://gdsfactory.github.io/gdsfactory/plugins_fdtd.html)
  - [tidy3d](https://gdsfactory.github.io/gdsfactory/notebooks/tidy3d/00_tidy3d.html)
  - [MEEP](https://gdsfactory.github.io/gdsfactory/notebooks/meep/001_meep_sparameters.html)
  - [Ansys Lumerical FDTD](https://gdsfactory.github.io/gdsfactory/notebooks/lumerical/1_fdtd_sparameters.html)
* [S-Parameter Circuit Solvers](https://gdsfactory.github.io/gdsfactory/plugins_circuits.html)
  - [SAX](https://gdsfactory.github.io/gdsfactory/notebooks/sax/sax.html)
  - [Ansys Lumerical INTERCONNECT](https://gdsfactory.github.io/gdsfactory/notebooks/lumerical/2_interconnect.html)
* [Database](https://gdsfactory.github.io/gdsfactory/notebooks/12_database.html)

## Getting started

- Run notebooks on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gdsfactory/binder-sandbox/HEAD)
- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=250169028)
- [See slides](https://docs.google.com/presentation/d/1_ZmUxbaHWo_lQP17dlT1FWX-XD8D9w7-FcuEih48d_0/edit#slide=id.g11711f50935_0_5)
- [Read docs](https://gdsfactory.github.io/gdsfactory/)
- [![Video Tutorials](https://img.shields.io/badge/youtube-Video_Tutorials-red.svg?logo=youtube)](https://www.youtube.com/@gdsfactory625/playlists)
- [![Join the chat at https://gitter.im/gdsfactory-dev/community](https://badges.gitter.im/gdsfactory-dev/community.svg)](https://gitter.im/gdsfactory-dev/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
- See announcements on [GitHub](https://github.com/gdsfactory/gdsfactory/discussions/547), [google-groups](https://groups.google.com/g/gdsfactory) or [LinkedIn](https://www.linkedin.com/company/gdsfactory)

## Testimonals

"I've used **gdsfactory** since 2017 for all my chip tapeouts. I love that it is fast, easy to use, and easy to extend. It's the only tool that allows us to have an end-to-end chip design flow (design, verification and validation)."

<div style="text-align: right; margin-right: 10%;">Joaquin Matres - <strong>Google</strong></div>

---

"I've relied on **gdsfactory** for several tapeouts over the years. It's the only tool I've found that gives me the flexibility and scalability I need for a variety of projects."

<div style="text-align: right; margin-right: 10%;">Alec Hammond - <strong>Meta Reality Labs Research</strong></div>

---

"The best photonics layout tool I've used so far and it is leaps and bounds ahead of any commercial alternatives out there. Feels like gdsfactory is freeing photonics."

<div style="text-align: right; margin-right: 10%;">Hasitha Jayatilleka - <strong>LightIC Technologies</strong></div>

---

"As an academic working on large scale silicon photonics at CMOS foundries I've used gdsfactory to go from nothing to full-reticle layouts rapidly (in a few days). I particularly appreciate the full-system approach to photonics, with my layout being connected to circuit simulators which are then connected to device simulators. Moving from legacy tools such as gdspy and phidl to gdsfactory has sped up my workflow at least an order of magnitude."

<div style="text-align: right; margin-right: 10%;">Alex Sludds - <strong>MIT</strong></div>

---

"I use gdsfactory for all of my photonic tape-outs. The Python interface makes it easy to version control individual photonic components as well as entire layouts, while integrating seamlessly with KLayout and most standard photonic simulation tools, both open-source and commercial.

<div style="text-align: right; margin-right: 10%;">Thomas Dorch - <strong>Freedom Photonics</strong></div>


## Contributors

Thanks to all the contributors that make this awesome project possible!

[![Meet our contributors!](https://contrib.rocks/image?repo=gdsfactory/gdsfactory)](https://github.com/gdsfactory/gdsfactory/graphs/contributors)
