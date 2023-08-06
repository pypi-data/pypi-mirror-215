# dummy python release project

This is a *dummy* project that exists to test changes to the release process for Python projects at eLife.

It *should* illustrate how to incorporate a Python project into the Jenkins release process.

It is *not* a template for Python projects at eLife. Projects come in all shapes and sizes.

## usage


1. create a new branch
2. bump the version number in `setup.py`
3. commit, push, open a PR
4. merge PR

CI will then move the changes into `approved`, then `master`, then detect that a version change has occured and do a
Pypi release.
