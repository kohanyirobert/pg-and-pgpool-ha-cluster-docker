docker-compose down --volumes --remove-orphans
rm -rf ./.env
rm -rf ./docker-compose.yml
rm -rf -Recurse ./out
python ./scripts/generate.py
docker-compose build
docker-compose up --detach
