# openfractal-client

**Important: if you are planning to work with the Openfractal instances, it is highly recommended to read the upstream documentation at <https://molssi.github.io/QCFractal/overview/index.html>.**

## Available Openfractal instances

| Name               | Comment                                                                                                 | API URL                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `openfractal-test` | A test instance for learn how to use QCFractal. In case of reset, it will be communicated pro-actively. | <https://openfractal-test-pgzbs3yryq-uc.a.run.app> |

Oepnfractal Dashboard: <https://openfractal-backend.vercel.app/>

## User accounts

To interact with any Openfractal instances, you must have a user account. Ask an administrator to create one for you. Here are the 5 roles you can have associated with your account:

- Admin
- Compute
- Read
- Submit
- Monitor

## Overview

The two main libraries to interact with the Openfractal instances are:

- [`qcportal`](https://github.com/MolSSI/QCFractal/tree/next/qcportal): a Python client for Openfractal (QCFractal instance).
- [`qcfractalcompute`](https://github.com/MolSSI/QCFractal/tree/next/qcfractalcompute): a Python client for Openfractal (QCFractal instance) that can launch a worker (also called a manager).

For now the Python library of this repo `openfractal-client` does not contain any particular logic. The plan is to use it if we need custom logic related to openfractal moving forward.

## Next Steps

- [Installation](./installation.md): Install the openfractal-client and its dependencies
- [Tutorials](./tutorials/01_submit_dataset.ipynb): Work with datasets, execute manager, export generated data.
