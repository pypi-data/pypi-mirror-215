from google.protobuf import __version__ as __pb__version__

from cmon._docarray import docarray_v2 as is_docarray_v2

if __pb__version__.startswith('4'):
    if is_docarray_v2:
        from cmon.proto.docarray_v2.pb.cmon_pb2_grpc import *
    else:
        from cmon.proto.docarray_v1.pb.cmon_pb2_grpc import *

else:
    if is_docarray_v2:
        from cmon.proto.docarray_v2.pb2.cmon_pb2_grpc import *
    else:
        from cmon.proto.docarray_v1.pb2.cmon_pb2_grpc import *
