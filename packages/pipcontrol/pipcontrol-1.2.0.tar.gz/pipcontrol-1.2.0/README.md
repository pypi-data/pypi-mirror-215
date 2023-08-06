# pipcontrol

This package is developed for automation of pip install

## How to use

```python
# list of packages
packages = ["python-crontab", "requests", "psutil", "selenium==4.8"]

# fuctions
# pipcontrol = PipControl(__file__)
# pipcontrol.install(packages)
# pipcontrol.update(packages)
# pipcontrol.uninstall(packages)
# pipcontrol.requirement_freeze()
# pipcontrol.requirement_install()
# pipcontrol.requirement_unistall()

# Run in global python evironment 1
with PipControl(__file__) as pip1:
    pip1.install(packages)

# # Run in global python evironment 2
# with PipControl(__file__, packages, "test.py test2"):
#     pass  # install packages and run file in __init__

# Run in venv1
# ! Run in virtual environment python
pipv_1 = PipControl(__file__, venv_folder="venv1")
pipv_1.setup_venv()
pipv_1.install(packages)
pipv_1.run("test.py venv_test1")
pipv_1.delete_venv()

# Run in venv2
with PipControl(__file__, venv_folder="venv2", venv=True) as pipv_2:
    pipv_2.install(packages)
    pipv_2.run("test.py venv_test2")

# Run in venv3
with PipControl(__file__, packages, "test.py venv_test3", "venv3", True):
    pass

```
