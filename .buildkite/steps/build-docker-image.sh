# @author: bilalm19

#!/bin/bash
set -e

build_image() {
  DOCKER_BUILDKIT=1 docker build --target $1 -t $2 --progress=plain .
}

if [[ $(uname -m) == 'x86_64' ]]; then
  TAG_NAME=${TAG_NAME_X86_64}
elif [[ $(uname -m) == 'aarch64' ]]; then
  TAG_NAME=${TAG_NAME_AARCH64}
fi

# Test image
if [[ ${BUILDKITE_BRANCH} != "master" ]]; then
  rm -rf $ARTIFACT_PATH
  mkdir $ARTIFACT_PATH

  # Production ready image
  build_image "$(uname -m)_production" ${TAG_NAME}
  # Run image to get coverage report
  docker run -v $ARTIFACT_PATH:/workspace/artifacts $TAG_NAME \
    /bin/bash -c "mv coverage-report.txt artifacts && chmod 777 -R artifacts"

  # Upload coverage report to buildkite
  buildkite-agent artifact upload $ARTIFACT_PATH/coverage-report.txt
fi

# Push image to docker hub
if [[ ${BUILDKITE_BRANCH} == "master" ]] || 
  [[ ${BUILDKITE_PULL_REQUEST_BASE_BRANCH} == "master" ]] ||
  [[ ! -z ${BUILDKITE_TAG} ]]; then
    build_image "$(uname -m)_production" ${TAG_NAME}
    docker push ${TAG_NAME}
fi

if [[ ${BUILDKITE_BRANCH} == "master" ]]; then
  docker system prune -f --volumes
fi
