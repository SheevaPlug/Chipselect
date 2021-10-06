#!/bin/bash

docker run --name opendash --publish 5601:5601 --network opensearch-net --env OPENSEARCH_HOSTS='["https://opensearch-node1:9200"]' opensearchproject/opensearch-dashboards
