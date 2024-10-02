sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev libgdbm-dev libnss3-dev wget

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
sudo tar xzf Python-3.10.13.tgz

cd Python-3.10.13
sudo ./configure --enable-optimizations
sudo make altinstall

python3.10 -m ensurepip --upgrade
python3.10 -m pip install --upgrade pip

cd ~/kapibara-project/backend
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# pip install poetry
# poetry install
mkdir src/log
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
