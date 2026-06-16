#!/bin/bash

# Docker Hub Build & Push Script
# Usage: ./scripts/docker-push.sh [tag]

set -e

# Configuration
PROJECT_NAME="${PROJECT_NAME:-narratoai}"
DOCKER_IMAGE="${DOCKER_IMAGE:-tinnt-truman/narratoai}"
DEFAULT_TAG="latest"

# Get tag from argument or use default
TAG="${1:-$DEFAULT_TAG}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Building and pushing ${DOCKER_IMAGE}:${TAG}${NC}"

# Check if DOCKER_TOKEN is set
if [ -z "$DOCKER_TOKEN" ]; then
    echo -e "${RED}Error: DOCKER_TOKEN not set${NC}"
    echo "Usage: DOCKER_TOKEN=your_token ./scripts/docker-push.sh [tag]"
    exit 1
fi

# Login to Docker Hub
echo -e "${YELLOW}Logging in to Docker Hub...${NC}"
echo "$DOCKER_TOKEN" | docker login -u tinnt-truman --password-stdin

# Build image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t "${DOCKER_IMAGE}:${TAG}" .

# Push image
echo -e "${YELLOW}Pushing to Docker Hub...${NC}"
docker push "${DOCKER_IMAGE}:${TAG}"

# Also tag and push as latest if not already latest
if [ "$TAG" != "$DEFAULT_TAG" ]; then
    docker tag "${DOCKER_IMAGE}:${TAG}" "${DOCKER_IMAGE}:${DEFAULT_TAG}"
    docker push "${DOCKER_IMAGE}:${DEFAULT_TAG}"
fi

echo -e "${GREEN}Successfully pushed ${DOCKER_IMAGE}:${TAG}${NC}"
