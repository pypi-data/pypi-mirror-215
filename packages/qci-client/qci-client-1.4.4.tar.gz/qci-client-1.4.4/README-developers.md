# QCI Client

## Getting started

### Environment Variables

These environment variables must be set to fully run/test--

- QCI_TOKEN - token for Qatalyst API
<!-- markdown-link-check-disable-next-line -->
- QCI_API_URL - Example: "https://api.qci-next.com"

## Development Guide

### Installation

`qci-client` currently supports Python 3.8-11, as specified in the PEP-621-compliant
[pyproject.toml](pyproject.toml). ([pyenv](https://github.com/pyenv/pyenv) is
recommended for Python version management.)

Python package and management uses `pip` and `setuptools` (with `wheel` for legacy
support). Using the Python virtual environment of choice, upgrade all these tools to
latest--

```bash
pip install --upgrade pip setuptools wheel
```

#### Developer install

Only for those who plan to make code changes to qci-client and later merge those changes
into the upstream qci-client code repository.

After cloning the qci-client repository, install `qci-client` (in editable mode) from the repo's root
directory using--

```bash
pip install -e ".[dev]"
```

Verify your installation, including the SCM-controlled automatic versioning of
`qci-client`, using--

```bash
python -m pip list
```

Verify your installation by running the tests in the next section.

### Testing

#### Run Tests with Coverage Report

With the above environment variables properly set (esp. a "non_user" `QCI_TOKEN`), run
ALL the tests (incluing for some large problems) locally with coverage using--

```bash
python -m coverage run --source=qci_client -m pytest
python -m coverage report -m
python -m coverage html
```

Note:
- The `htmlcov` directory may cause issues with `pip` and `setuptools`. Move/delete
it when necessary.
- All the tests are not run and 100% code coverage is not yet required in CI.
- Some "online" tests consume both time and resources. Use the `-m offline` pytest
marker to run a subset of "offline" tests without a true backend and without the need to
set any environment variables, as is done in CI (cf. [.gitlab-ci.yml](.gitlab-ci.yml)).

### Code Quality and Security

The following code checkers are configured and must pass in CI. See
[.gitlab-ci.yml](.gitlab-ci.yml) for details. You will typically need to run the
following and commit any required changes before pushing.

#### Megalinter

[Megalinter](https://megalinter.io/latest/) lints many types of files and is configured
in [.mega-linter.yml](.mega-linter.yml). It does not run Python-specific linters.
Run it locally from the root directory, using same Docker container used in CI, with--

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock:rw -v $(pwd):/tmp/lint:rw oxsecurity/megalinter:v6
```

#### pylint

The `pylint` linter is configured in [pyproject.toml](pyproject.toml). Run it locally
from the root directory using--

```bash
python -m pylint .
```

#### black

The `black` auto-formatter is configured in [pyproject.toml](pyproject.toml). Run it
locally from the root directory using--

```bash
python -m black .
```

#### Semgrep

[Semgrep](https://semgrep.dev/docs/) scans the codebase in CI as a security measure.

#### Trivy

[Trivy](https://aquasecurity.github.io/trivy/) scans the codebase in CI as a security
measure.

### Building

Build source and wheel artifacts (into the `dist` directory) using--

```bash
python -m build
```

The version of `qci-client` is inferred automatically from SCM (i.e., git) using
[setuptools-scm](https://pypi.org/project/setuptools-scm/). Check the build's manifest
file using--

```bash
python -m check_manifest
```

### Releasing

Pushing a tag via command-line `git` or creating a tag using the Gitlab Web console
(usually from the `main` branch) should trigger a Gitlab release build in CI, with a
link to the build artifacts in an automatically generated Gitlab release. Use the format
vX.Y.Z, and make sure to consider the code changes since the last tag in order to follow
[semantic versioning](https://semver.org/). See [.gitlab-ci.yml](.gitlab-ci.yml) for
details, and the
[Python release documentation](https://qci-dev.atlassian.net/wiki/spaces/QD/pages/1057161219/Releases#Python).

The CI for release tags will also push the `qci-client` package to QCI's [internal PyPI
server](http://python.qci-dev.com/) via `twine`.
