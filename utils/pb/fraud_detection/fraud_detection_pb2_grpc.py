# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from fraud_detection import fraud_detection_pb2 as fraud__detection_dot_fraud__detection__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in fraud_detection/fraud_detection_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class FraudDetectionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DetectFraud = channel.unary_unary(
                '/bookstore.FraudDetectionService/DetectFraud',
                request_serializer=fraud__detection_dot_fraud__detection__pb2.DetectFraudRequest.SerializeToString,
                response_deserializer=fraud__detection_dot_fraud__detection__pb2.DetectFraudResponse.FromString,
                _registered_method=True)


class FraudDetectionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DetectFraud(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FraudDetectionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DetectFraud': grpc.unary_unary_rpc_method_handler(
                    servicer.DetectFraud,
                    request_deserializer=fraud__detection_dot_fraud__detection__pb2.DetectFraudRequest.FromString,
                    response_serializer=fraud__detection_dot_fraud__detection__pb2.DetectFraudResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bookstore.FraudDetectionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bookstore.FraudDetectionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FraudDetectionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DetectFraud(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/bookstore.FraudDetectionService/DetectFraud',
            fraud__detection_dot_fraud__detection__pb2.DetectFraudRequest.SerializeToString,
            fraud__detection_dot_fraud__detection__pb2.DetectFraudResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
