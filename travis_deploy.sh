#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push andrumdev/rumplenator:$TRAVIS_COMMIT
