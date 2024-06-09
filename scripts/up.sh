./scripts/down.sh
python3 ./scripts/generate.py
docker-compose build
docker-compose up --detach
