# Model Validation Framework

description here...

## Getting Started

For full documentation of the project and instructions on how to get started, visit the [documentation site](https://tomkimcta.gitlab.io/model-validation-framework).

## Project Administration

### Dependencies

R dependencies are managed using `renv`. Spin up a Python Virtual Environment

Python dependencies are specified by `requirements.txt`. This file is generated from `requirements.in` by running `python3 -m piptools compile`.

### Git

This project operates using two Git branches

- dev
- main

All development work should be undertaken on the development branch. The dev branch should then be merged into the master branch when key milestones are met.

### Testing Framework

Tests run in CI on every commit. Python code is tested using [pytest](https://docs.pytest.org) in a Python Virtual Environment specified by `requirements.txt`. 

### Documentation

This project uses a static site generator called [Docusaurus](https://docusaurus.io) to create its documentation. The content for the documentation site is contained in `documentation/docs/`. Any updates to documentation can be verified in a development server by running `npm i && npm start` from the `documentation/` directory. The public documentation site is rebuilt only for commits to the main branch. This is primarily to economise CI minutes.

