& .\scripts\down.ps1
& python .\scripts\generate.py
& docker-compose build
& docker-compose up --detach
