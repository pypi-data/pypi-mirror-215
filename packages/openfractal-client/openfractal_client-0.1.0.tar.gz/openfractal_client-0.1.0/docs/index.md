# openfractal-client

**Important: if you are planning to work with the Openfractal instances, it is highly recommended to read the upstream documentation at <https://molssi.github.io/QCFractal/overview/index.html>.**

## Available Openfractal instances

| Name               | Comment                                                                                                 | API URL                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `openfractal-test` | A test instance for learn how to use QCFractal. In case of reset, it will be communicated pro-actively. | <https://openfractal-test-pgzbs3yryq-uc.a.run.app> |

Oepnfractal Dashboard: <https://openfractal-backend.vercel.app/>

### User accounts

To interact with any Openfractal instances, you must have a user account. Ask an administrator to create one for you. Here are the 5 roles you can have associated with your account:

- Admin
- Compute
- Read
- Submit
- Monitor

## Usage and installation

The two main libraries to interact with the Openfractal instances are:

- [`qcportal`](https://github.com/MolSSI/QCFractal/tree/next/qcportal): a Python client for Openfractal (QCFractal instance).
- [`qcfractalcompute`](https://github.com/MolSSI/QCFractal/tree/next/qcfractalcompute): a Python client for Openfractal (QCFractal instance) that can launch a worker (also called a manager).

For now the Python library of this repo `openfractal-client` does not contain any particular logic. The plan is to use it if we need custom logic related to openfractal moving forward.

### Docker

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
