# cd into project folder
cd /root/mlh-portfolio

# ensure repo is up-to-date
git fetch
git checkout main
git reset origin/main --hard

# enter python virtual env
source python3-virtualenv/bin/activate

# install python repositories
pip install -r requirements.txt

# restart daemon
systemctl daemon-reload
systemctl restart myportfolio

