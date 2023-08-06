# Installation

## Automatic Installation

For participating to the data generation effort only. If you want to interact with the datasets or submit datasets yourself, you must use one of the other installation methods.

```bash
curl https://raw.githubusercontent.com/OpenDrugDiscovery/openfractal-client/main/auto_install.sh | bash
```

## Docker

Public docker images are available at <https://github.com/OpenDrugDiscovery/openfractal-client/pkgs/container/openfractal-client>.

```bash
docker run --rm -ti ghcr.io/opendrugdiscovery/openfractal-client:main
```

### Using mamba

The QCFractal libraries ecosystem have not yet been released. It is actively being developed in the `next` branch at <https://github.com/MolSSI/QCFractal/tree/next>.

For now here is a minimal Conda `env.yml` file you can use to perform the installation (this will be simplified in the future):

```yaml
channels:
  - hadim/label/qcportal_next
  - conda-forge/label/libint_dev # for psi4
  - conda-forge

dependencies:
  - python >=3.9
  - pip

  # QCPortal deps
  - hadim/label/qcportal_next::qcportal
  - hadim/label/qcportal_next::qcfractalcompute

  # Compute managers
  - parsl
  - psi4 =1.8
  - openmm
  - openff-forcefields
  - openmmforcefields

  # Optional
  - datamol
  - openff-toolkit
  - zarr

  # Optional utilities
  - loguru
  - typer
  - python-dotenv
```

Put the above YAML file into `env.yml`. Then:

```bash
micromamba create -n openfractal -f env.yml
```

_In the future, it will be as simple as `micromamba create -n openfractal openfractal-client`._
