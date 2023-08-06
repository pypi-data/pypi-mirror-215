[![badge doc](https://img.shields.io/badge/docs-latest-orange.svg)](https://www.idiap.ch/software/bob/docs/bob/bob.pad.base/master/sphinx/index.html)
[![badge pipeline](https://gitlab.idiap.ch/bob/bob.pad.base/badges/master/pipeline.svg)](https://gitlab.idiap.ch/bob/bob.pad.base/commits/master)
[![badge coverage](https://gitlab.idiap.ch/bob/bob.pad.base/badges/master/coverage.svg)](https://www.idiap.ch/software/bob/docs/bob/bob.pad.base/master/coverage/)
[![badge gitlab](https://img.shields.io/badge/gitlab-project-0000c0.svg)](https://gitlab.idiap.ch/bob/bob.pad.base)

# Scripts to run anti-spoofing experiments

This package is part of the signal-processing and machine learning toolbox
[Bob](https://www.idiap.ch/software/bob).
This package is the base of the `bob.pad` family of packages, which allow to
run comparable and reproducible presentation attack detection (PAD) experiments
on publicly available databases.

This package contains basic functionality to run PAD experiments.
It provides a generic API for PAD including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A PAD algorithm

All these steps of the PAD system are given as configuration files.
All the algorithms are standardized on top of scikit-learn estimators.

In this base package, only a core functionality is implemented. The specialized
algorithms should be provided by other packages, which are usually in the
`bob.pad` namespace, like
[`bob.pad.face`](https://gitlab.idiap.ch/bob/bob.pad.face).

## Installation

Complete Bob's
[installation instructions](https://www.idiap.ch/software/bob/install). Then,
to install this package, run:
``` sh
conda install bob.pad.base
```

## Contact

For questions or reporting issues to this software package, contact our
development [mailing list](https://www.idiap.ch/software/bob/discuss).
