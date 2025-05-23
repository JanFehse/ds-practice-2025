# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from database import database_pb2 as database_dot_database__pb2
from shared import order_pb2 as shared_dot_order__pb2

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
        + f' but the generated code in database/database_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DatabaseServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/bookstore.DatabaseService/Read',
                request_serializer=database_dot_database__pb2.ReadRequest.SerializeToString,
                response_deserializer=database_dot_database__pb2.ReadResponse.FromString,
                _registered_method=True)
        self.Write = channel.unary_unary(
                '/bookstore.DatabaseService/Write',
                request_serializer=database_dot_database__pb2.WriteRequest.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.Decrement = channel.unary_unary(
                '/bookstore.DatabaseService/Decrement',
                request_serializer=database_dot_database__pb2.ChangeAmountRequest.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.Increment = channel.unary_unary(
                '/bookstore.DatabaseService/Increment',
                request_serializer=database_dot_database__pb2.ChangeAmountRequest.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.Prepare = channel.unary_unary(
                '/bookstore.DatabaseService/Prepare',
                request_serializer=database_dot_database__pb2.PrepareRequestDatabase.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.Commit = channel.unary_unary(
                '/bookstore.DatabaseService/Commit',
                request_serializer=shared_dot_order__pb2.ExecInfo.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.Abort = channel.unary_unary(
                '/bookstore.DatabaseService/Abort',
                request_serializer=shared_dot_order__pb2.ExecInfo.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)
        self.PingPrimary = channel.unary_unary(
                '/bookstore.DatabaseService/PingPrimary',
                request_serializer=database_dot_database__pb2.PingPrimaryRequest.SerializeToString,
                response_deserializer=shared_dot_order__pb2.ErrorResponse.FromString,
                _registered_method=True)


class DatabaseServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Decrement(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Increment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Prepare(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Commit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Abort(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PingPrimary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=database_dot_database__pb2.ReadRequest.FromString,
                    response_serializer=database_dot_database__pb2.ReadResponse.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=database_dot_database__pb2.WriteRequest.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'Decrement': grpc.unary_unary_rpc_method_handler(
                    servicer.Decrement,
                    request_deserializer=database_dot_database__pb2.ChangeAmountRequest.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'Increment': grpc.unary_unary_rpc_method_handler(
                    servicer.Increment,
                    request_deserializer=database_dot_database__pb2.ChangeAmountRequest.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'Prepare': grpc.unary_unary_rpc_method_handler(
                    servicer.Prepare,
                    request_deserializer=database_dot_database__pb2.PrepareRequestDatabase.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'Commit': grpc.unary_unary_rpc_method_handler(
                    servicer.Commit,
                    request_deserializer=shared_dot_order__pb2.ExecInfo.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'Abort': grpc.unary_unary_rpc_method_handler(
                    servicer.Abort,
                    request_deserializer=shared_dot_order__pb2.ExecInfo.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
            'PingPrimary': grpc.unary_unary_rpc_method_handler(
                    servicer.PingPrimary,
                    request_deserializer=database_dot_database__pb2.PingPrimaryRequest.FromString,
                    response_serializer=shared_dot_order__pb2.ErrorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bookstore.DatabaseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('bookstore.DatabaseService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DatabaseService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(request,
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
            '/bookstore.DatabaseService/Read',
            database_dot_database__pb2.ReadRequest.SerializeToString,
            database_dot_database__pb2.ReadResponse.FromString,
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
    def Write(request,
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
            '/bookstore.DatabaseService/Write',
            database_dot_database__pb2.WriteRequest.SerializeToString,
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
    def Decrement(request,
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
            '/bookstore.DatabaseService/Decrement',
            database_dot_database__pb2.ChangeAmountRequest.SerializeToString,
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
    def Increment(request,
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
            '/bookstore.DatabaseService/Increment',
            database_dot_database__pb2.ChangeAmountRequest.SerializeToString,
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
    def Prepare(request,
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
            '/bookstore.DatabaseService/Prepare',
            database_dot_database__pb2.PrepareRequestDatabase.SerializeToString,
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
    def Commit(request,
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
            '/bookstore.DatabaseService/Commit',
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
    def Abort(request,
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
            '/bookstore.DatabaseService/Abort',
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
    def PingPrimary(request,
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
            '/bookstore.DatabaseService/PingPrimary',
            database_dot_database__pb2.PingPrimaryRequest.SerializeToString,
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
