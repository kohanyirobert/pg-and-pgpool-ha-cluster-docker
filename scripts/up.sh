./scripts/down.sh
python ./scripts/generate.py
docker-compose build
docker-compose up --detach
