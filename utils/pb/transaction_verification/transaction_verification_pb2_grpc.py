# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from shared import order_pb2 as shared_dot_order__pb2
from transaction_verification import transaction_verification_pb2 as transaction__verification_dot_transaction__verification__pb2

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
        + f' but the generated code in transaction_verification/transaction_verification_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TransactionVerificationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InitVerifyTransaction = channel.unary_unary(
                '/bookstore.TransactionVerificationService/InitVerifyTransaction',
                request_serializer=transaction__verification_dot_transaction__verification__pb2.TransactionRequest.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.VerifyTransaction = channel.unary_unary(
                '/bookstore.TransactionVerificationService/VerifyTransaction',
                request_serializer=shared_dot_order__pb2.ExecInfo.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.DeleteOrder = channel.unary_unary(
                '/bookstore.TransactionVerificationService/DeleteOrder',
                request_serializer=shared_dot_order__pb2.ExecInfo.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)


class TransactionVerificationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InitVerifyTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionVerificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InitVerifyTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.InitVerifyTransaction,
                    request_deserializer=transaction__verification_dot_transaction__verification__pb2.TransactionRequest.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'VerifyTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyTransaction,
                    request_deserializer=shared_dot_order__pb2.ExecInfo.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'DeleteOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteOrder,
                    request_deserializer=shared_dot_order__pb2.ExecInfo.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bookstore.TransactionVerificationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bookstore.TransactionVerificationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TransactionVerificationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InitVerifyTransaction(request,
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
            '/bookstore.TransactionVerificationService/InitVerifyTransaction',
            transaction__verification_dot_transaction__verification__pb2.TransactionRequest.SerializeToString,
            shared_dot_order__pb2.ErrorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def VerifyTransaction(request,
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
            '/bookstore.TransactionVerificationService/VerifyTransaction',
            shared_dot_order__pb2.ExecInfo.SerializeToString,
            shared_dot_order__pb2.ErrorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteOrder(request,
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
            '/bookstore.TransactionVerificationService/DeleteOrder',
            shared_dot_order__pb2.ExecInfo.SerializeToString,
            shared_dot_order__pb2.ErrorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
