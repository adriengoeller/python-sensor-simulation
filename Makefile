python -m venv .venv3.8 

 .\.venv3.8\Scripts\Activate.ps1

 python -m pip install -e .

 py -m pip install -e .

 py -m pip install build

 py -m build --sdist

 ####
 

 pip wheel -r requirements.txt
 python -m setup.py bdist_wheel