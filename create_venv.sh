rm -rf ./.venv
python -m venv .venv
pip install --upgrade pip
pip install -r requirements.txt
source ./.venv/bin/activate
