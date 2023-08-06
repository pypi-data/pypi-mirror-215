#!/bin/bash

set -e

# This script fetches the latest protobuf files from the docarray repository
# and copies them to the `cmon-core/proto` directory.

# The script is meant to be run from the root of the repository.

docarray_VERSION=$1

if [ -z "$docarray_VERSION" ]; then
    echo "Please provide a docarray version as the second argument."
    exit 1
fi

if [[ $docarray_VERSION != "v*" ]]; then
    docarray_VERSION="v$docarray_VERSION"
fi

echo "Fetching protos for docarray version $docarray_VERSION"
wget https://raw.githubusercontent.com/cmon.pw/docarray/$docarray_VERSION/docarray/proto/docarray.proto -O cmon/proto/docarray.proto