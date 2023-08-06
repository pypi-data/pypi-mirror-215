#/bin/sh

set -e

# This script is used to generate gRPC client stubs from the proto files.

GO_MODULE="jraft"
DOCARRAY_PROTO="docarray.proto"
DOCARRAY_DIR="../../docarray"
DOCARRAY_PACKAGE="$GO_MODULE/docarray"

CMON_PROTO="cmon.proto"
CMON_DIR="../../cmon"
CMON_PACKAGE="$GO_MODULE/cmon-go-proto"


cd cmon/proto
if ! $(grep -q '^option go_package = ' docarray.proto);then
       awk '/package docarray;/{print; print "option go_package = \"'${DOCARRAY_PACKAGE}'\";";next}1' docarray.proto > temp.proto
       mv temp.proto docarray.proto
fi
protoc --go_out=${DOCARRAY_DIR} \
       --go_opt=paths=source_relative \
       --go_opt=M${DOCARRAY_PROTO}=${DOCARRAY_PACKAGE} \
       --go-grpc_out=${DOCARRAY_DIR} \
       --go-grpc_opt=paths=source_relative \
       --experimental_allow_proto3_optional \
       ${DOCARRAY_PROTO} 

if ! $(grep -q '^option go_package = ' cmon.proto);then
       awk '/package cmon;/{print; print "option go_package = \"'${CMON_PACKAGE}'\";";next}1' cmon.proto > temp.proto
       mv temp.proto cmon.proto
fi
protoc --go_out=${CMON_DIR} \
       --go_opt=paths=source_relative \
       --go_opt=M${CMON_PROTO}=${CMON_PACKAGE} \
       --go-grpc_out=${CMON_DIR} \
       --go-grpc_opt=paths=source_relative \
       --experimental_allow_proto3_optional \
       ${CMON_PROTO} 
cd -
