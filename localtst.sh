docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD" "$DOCKER_REPO"
docker push "$DOCKER_REPO"/ "$DEPLOY_TARGET"/"$DOCKER_IMAGE":latest
./bin/ecs-deploy.sh  \
 -n "$ECS_SERVICE_NAME" \
 -c "$ECS_CLUSTER"   \
 -i "$DOCKER_REPO"/ "$DEPLOY_TARGET"/"$DOCKER_IMAGE":latest
