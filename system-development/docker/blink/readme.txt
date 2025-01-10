#コンテナ作成
docker-compose up -d .
docker create --name {名前} {イメージ名}

# コンテナへの接続
docker start {名前}
docker exec -it {名前}  bash

# コンテナの停止
docker compose down