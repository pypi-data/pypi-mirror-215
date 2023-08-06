from typing import Optional

import grpc
from grpc import RpcError
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from cmon.proto import cmon_pb2, cmon_pb2_grpc
from cmon.serve.helper import get_server_side_grpc_options
from cmon.serve.networking.utils import send_health_check_async, send_health_check_sync
from cmon.serve.runtimes.servers import BaseServer
from cmon._docarray import docarray_v2


class GRPCServer(BaseServer):
    """GRPC Server implementation"""

    def __init__(
        self,
        grpc_server_options: Optional[dict] = None,
        ssl_keyfile: Optional[str] = None,
        ssl_certfile: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the gateway
        :param grpc_server_options: Dictionary of kwargs arguments that will be passed to the grpc server as options when starting the server, example : {'grpc.max_send_message_length': -1}
        :param ssl_keyfile: the path to the key file
        :param ssl_certfile: the path to the certificate file
        :param kwargs: keyword args
        """
        super().__init__(**kwargs)
        self.grpc_server_options = grpc_server_options
        self.grpc_tracing_server_interceptors = self.aio_tracing_server_interceptors()
        self.ssl_keyfile = ssl_keyfile
        self.ssl_certfile = ssl_certfile
        self.health_servicer = health.aio.HealthServicer()

    async def setup_server(self):
        """
        setup GRPC server
        """
        self.logger.debug(f'Setting up GRPC server')
        if docarray_v2:
            from cmon.serve.runtimes.gateway.request_handling import GatewayRequestHandler
            if isinstance(self._request_handler, GatewayRequestHandler):
                await self._request_handler.streamer._get_endpoints_input_output_models(is_cancel=self.is_cancel)
                self._request_handler.streamer._validate_flow_docarray_compatibility()

        self.server = grpc.aio.server(
            options=get_server_side_grpc_options(self.grpc_server_options),
            interceptors=self.grpc_tracing_server_interceptors,
        )

        cmon_pb2_grpc.add_CmonRPCServicer_to_server(self._request_handler, self.server)

        cmon_pb2_grpc.add_CmonSingleDataRequestRPCServicer_to_server(
            self._request_handler, self.server
        )

        if hasattr(self._request_handler, 'endpoint_discovery'):
            cmon_pb2_grpc.add_CmonDiscoverEndpointsRPCServicer_to_server(
                self._request_handler, self.server
            )

        if hasattr(self._request_handler, 'process_data'):
            cmon_pb2_grpc.add_CmonDataRequestRPCServicer_to_server(
                self._request_handler, self.server
            )

        if hasattr(self._request_handler, 'dry_run'):
            cmon_pb2_grpc.add_CmonGatewayDryRunRPCServicer_to_server(
                self._request_handler, self.server
            )
        if hasattr(self._request_handler, 'snapshot'):
            cmon_pb2_grpc.add_CmonExecutorSnapshotServicer_to_server(
                self._request_handler, self.server
            )
        if hasattr(self._request_handler, 'snapshot_status'):
            cmon_pb2_grpc.add_CmonExecutorSnapshotProgressServicer_to_server(
                self._request_handler, self.server
            )
        if hasattr(self._request_handler, 'restore'):
            cmon_pb2_grpc.add_CmonExecutorRestoreServicer_to_server(
                self._request_handler, self.server
            )
        if hasattr(self._request_handler, 'restore_status'):
            cmon_pb2_grpc.add_CmonExecutorRestoreProgressServicer_to_server(
                self._request_handler, self.server
            )

        cmon_pb2_grpc.add_CmonInfoRPCServicer_to_server(
                self._request_handler, self.server
            )

        service_names = (
            cmon_pb2.DESCRIPTOR.services_by_name['CmonRPC'].full_name,
            cmon_pb2.DESCRIPTOR.services_by_name['CmonSingleDataRequestRPC'].full_name,
            cmon_pb2.DESCRIPTOR.services_by_name['CmonDataRequestRPC'].full_name,
            cmon_pb2.DESCRIPTOR.services_by_name['CmonGatewayDryRunRPC'].full_name,
            cmon_pb2.DESCRIPTOR.services_by_name['CmonDiscoverEndpointsRPC'].full_name,
            cmon_pb2.DESCRIPTOR.services_by_name['CmonInfoRPC'].full_name,
            reflection.SERVICE_NAME,
        )
        # Mark all services as healthy.
        health_pb2_grpc.add_HealthServicer_to_server(self.health_servicer, self.server)

        reflection.enable_server_reflection(service_names, self.server)

        bind_addr = f'{self.host}:{self.port}'

        if self.ssl_keyfile and self.ssl_certfile:
            with open(self.ssl_keyfile, 'rb') as f:
                private_key = f.read()
            with open(self.ssl_certfile, 'rb') as f:
                certificate_chain = f.read()

            server_credentials = grpc.ssl_server_credentials(
                (
                    (
                        private_key,
                        certificate_chain,
                    ),
                )
            )
            self.server.add_secure_port(bind_addr, server_credentials)
        elif (
            self.ssl_keyfile != self.ssl_certfile
        ):  # if we have only ssl_keyfile and not ssl_certfile or vice versa
            raise ValueError(
                f"you can't pass a ssl_keyfile without a ssl_certfile and vice versa"
            )
        else:
            self.server.add_insecure_port(bind_addr)
        self.logger.info(f'start server bound to {bind_addr}')
        await self.server.start()
        self.logger.debug(f'server bound to {bind_addr} started')
        for service in service_names:
            await self.health_servicer.set(
                service, health_pb2.HealthCheckResponse.SERVING
            )
        self.logger.debug(f'GRPC server setup successful')

    async def shutdown(self):
        """Free other resources allocated with the server, e.g, gateway object, ..."""
        self.logger.debug(f'Shutting down server')
        await super().shutdown()
        await self.health_servicer.enter_graceful_shutdown()
        await self._request_handler.close()  # allow pending requests to be processed
        await self.server.stop(1.0)
        self.logger.debug(f'Server shutdown finished')

    async def run_server(self):
        """Run GRPC server forever"""
        await self.server.wait_for_termination()

    @staticmethod
    def is_ready(ctrl_address: str, timeout: float = 1.0, logger=None, **kwargs) -> bool:
        """
        Check if status is ready.
        :param ctrl_address: the address where the control request needs to be sent
        :param timeout: timeout of the health check in seconds
        :param logger: CmonLogger to be used
        :param kwargs: extra keyword arguments
        :return: True if status is ready else False.
        """
        try:
            from grpc_health.v1 import health_pb2, health_pb2_grpc

            response = send_health_check_sync(ctrl_address, timeout=timeout)
            return (
                response.status == health_pb2.HealthCheckResponse.ServingStatus.SERVING
            )
        except RpcError as exc:
            if logger:
                logger.debug(f'Exception: {exc}')
            return False

    @staticmethod
    async def async_is_ready(ctrl_address: str, timeout: float = 1.0, logger=None, **kwargs) -> bool:
        """
        Async Check if status is ready.
        :param ctrl_address: the address where the control request needs to be sent
        :param timeout: timeout of the health check in seconds
        :param logger: CmonLogger to be used
        :param kwargs: extra keyword arguments
        :return: True if status is ready else False.
        """
        try:
            from grpc_health.v1 import health_pb2, health_pb2_grpc

            response = await send_health_check_async(ctrl_address, timeout=timeout)
            return (
                response.status == health_pb2.HealthCheckResponse.ServingStatus.SERVING
            )
        except RpcError as exc:
            if logger:
                logger.debug(f'Exception: {exc}')
            return False
