# Version number for pyPi should contain the build as well
# Format: major.minor-build
# Update version number in setup.py as well
set VERSION = 0.2-1

python setup.py sdist
twine upload dist/*
git tag -a v$VERSION -m "Package version for $VERSION"
git push origin --tags
