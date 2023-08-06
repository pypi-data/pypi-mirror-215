# datazimmer

[![Documentation Status](https://readthedocs.org/projects/datazimmer/badge/?version=latest)](https://datazimmer.readthedocs.io/en/latest)
[![codeclimate](https://img.shields.io/codeclimate/maintainability/sscu-budapest/datazimmer.svg)](https://codeclimate.com/github/sscu-budapest/datazimmer)
[![codecov](https://img.shields.io/codecov/c/github/sscu-budapest/datazimmer)](https://codecov.io/gh/sscu-budapest/datazimmer)
[![pypi](https://img.shields.io/pypi/v/datazimmer.svg)](https://pypi.org/project/datazimmer/)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.7499121.svg)](https://doi.org/10.5281/zenodo.7499121)


## To create a new project

- make sure that `python` points to `python>=3.8` and you have `pip` and `git` then `pip install datazimmer`
- run `dz init project-name`
  - pulls [project-template](https://github.com/sscu-budapest/project-template)
- add a remote
  - both to git and dvc (can run `dz build-meta` to see available dvc remotes)
  - git remote can be given with `dz init`
- create, register and document steps in a pipeline you will run in different [environments](TODO)
- build metadata to exportable and serialized format with `dz build-meta`
  - if you defined importable data from other artifacts in the config, you can import them with `load-external-data` 
  - ensure that you import envs that are served from sources you have access to
- build and run pipeline steps by running `dz run`
- validate that the data matches the [datascript](TODO) description with `dz validate`

### Scheduling

- a project as a whole has a cron expression in `zimmer.yaml` to determine the schedule of reruns
- additionally, aswan projects within the dz project can have different cron expressions for scheduling new runs of the aswan projects

### Test projects

TODO: document dogshow and everything else much better here


## Lookahead

- overlapping names convention
- resolve naming confusion with colassigner, colaccessor and table feature / composite type / index base classes
- abstract composite type + subclass of entity class
  - import ACT, inherit from it and specify 
  - importing composite type is impossible now if it contains foreign key :(
- add option to infer data type of assigned feature
  - can be problematic b/c pandas int/float/nan issue
- create similar sets of features in a dry way
- overlapping in entities
  - detect / signal the same type of entity
- exports: postgres, postgis , superset


### W3C compliancy plan

- test suite for compliance: https://w3c.github.io/csvw/publishing-snapshots/PR-earl/earl.html
- https://github.com/w3c/csvw
  - https://www.w3.org/TR/2015/REC-tabular-data-model-20151217/
  - https://www.w3.org/TR/tabular-metadata/


```
@article{tennison2015model,
  title={Model for tabular data and metadata on the web},
  author={Tennison, Jeni and Kellogg, Gregg and Herman, Ivan},
  year={2015}
}
```

```
@article{pollock2015metadata,
  title={Metadata vocabulary for tabular data},
  author={Pollock, Rufus and Tennison, Jeni and Kellogg, Gregg and Herman, Ivan},
  journal={W3C Recommendation},
  volume={17},
  year={2015}
}
```