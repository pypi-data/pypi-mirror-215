mamba activate pypi-test-entrain

python3 -m build

python3 -m twine upload dist/* -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYWViOTg1NjgtMDc2Zi00ODU3LTg3NDAtZjg2OTg2YjcyNzIxAAIqWzMsImRmZTY2N2U1LTNiODYtNDE2MC05ODk1LWZlZjQzZjI4MjY3NSJdAAAGIB9ACQDlIqjMYchW3WxMLSRwo2KqVlKTevS4YIiTVQZx

# mamba install squidpy anndata scvelo scanpy rpy2
# python3 -m pip install --no-deps entrain_spatial
