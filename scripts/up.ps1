& docker-compose down --volumes --remove-orphans
del -Force -ErrorAction SilentlyContinue .\.env
del -Force -ErrorAction SilentlyContinue .\docker-compose.yml
del -Force -ErrorAction SilentlyContinue -Recurse .\out\
& python .\scripts\generate.py
& docker-compose build
& docker-compose up --detach
