docker-compose down --volumes --remove-orphans
rm -f ./.env
rm -f ./docker-compose.yml
rm -rf  ./out
python ./scripts/generate.py
docker-compose build
docker-compose up --detach
