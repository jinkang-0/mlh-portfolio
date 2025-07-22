# cd into project folder
cd /root/mlh-portfolio

# ensure repo is up-to-date
git fetch
git checkout main
git reset origin/main --hard

# ensure server is down
docker compose -f docker-compose.prod.yml down

# spin up docker containers
# specify --build to force rebuild in case of code changes
docker compose -f docker-compose.prod.yml up -d --build
