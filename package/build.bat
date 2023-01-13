@ECHO OFF
ECHO Building package...
python -m build

ECHO Build complete.
ECHO Installing package...

pip install .

ECHO Done!