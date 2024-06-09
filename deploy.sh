#!/bin/bash

cd ${PROJECT_PATH}
export DOCKER_CLI_EXPERIMENTAL=enabled
docker run --privileged --rm tonistiigi/binfmt --install all
docker buildx create --use --name amd64-builder
/bin/cp -f ${BUILD_PATH}/Dockerfile .
docker buildx build --platform=linux/amd64 -t image . --load
cd ${BUILD_PATH}
docker image save image > image.tar
scp -oStrictHostKeyChecking=no -i ./id_ed25519 image.tar json@${HOST}:/home/json/image.tar
ssh  -oStrictHostKeyChecking=no  json@${HOST} -i ./id_ed25519 << "EOF"
  until caddy; do echo "Waiting for caddy"; done
  sudo docker image load -i /home/json/image.tar

  sudo docker ps -q --filter "publish=${PORT}" | xargs sudo docker rm -f
  sudo docker run -d -p ${PORT}:${PORT} $$(sudo docker images | awk '{print $$1}' | awk 'NR==2')

  ${CADDY_DEPLOY_BLOCK}
EOF
