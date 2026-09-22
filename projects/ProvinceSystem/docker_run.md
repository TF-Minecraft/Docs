> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/ProvinceSystem/blob/9b34fd3fd336af9025ca187ca9610690695c0efa/docker_run.txt). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

docker compose down --volumes --remove-orphans
docker compose build --no-cache
docker compose up -d --force-recreate

# uvicorn
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --log-level warning