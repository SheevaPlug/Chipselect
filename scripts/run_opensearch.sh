#!/bin/bash

docker run --name opensearch-node1 --publish 9200:9200 --memory 4g --network opensearch-net --env "discovery.type=single-node" --env "node.name=opensearch-node1" opensearchproject/opensearch
