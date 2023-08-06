"""This modules defines all kinds of exceptions raised in Cmon."""
from typing import List, Optional, Set, Union

import grpc.aio

from cmon.serve.helper import extract_trailing_metadata


class BaseCmonException(BaseException):
    """A base class for all exceptions raised by Cmon"""


class RuntimeFailToStart(SystemError, BaseCmonException):
    """When pod/deployment is failed to started."""


class RuntimeTerminated(KeyboardInterrupt, BaseCmonException):
    """The event loop of BasePod ends."""


class FlowTopologyError(Exception, BaseCmonException):
    """Flow exception when the topology is ambiguous."""


class FlowMissingDeploymentError(Exception, BaseCmonException):
    """Flow exception when a deployment can not be found in the flow."""


class FlowBuildLevelError(Exception, BaseCmonException):
    """Flow exception when required build level is higher than the current build level."""


class BadConfigSource(FileNotFoundError, BaseCmonException):
    """The yaml config file is bad, not loadable or not exist."""


class BadServerFlow(Exception, BaseCmonException):
    """A wrongly defined Flow on the server side"""


class BadClient(Exception, BaseCmonException):
    """A wrongly defined client, can not communicate with cmon server correctly."""


class BadServer(Exception, BaseCmonException):
    """Error happens on the server side."""


class BadClientCallback(BadClient, BaseCmonException):
    """Error in the callback function on the client side."""


class BadClientInput(BadClient, BaseCmonException):
    """Error in the request generator function on the client side."""


class BadRequestType(TypeError, BaseCmonException):
    """Exception when can not construct a request object from given data."""


class BadImageNameError(Exception, BaseCmonException):
    """Exception when an image name can not be found either local & remote"""


class BadYAMLVersion(Exception, BaseCmonException):
    """Exception when YAML config specifies a wrong version number."""


class NotSupportedError(Exception, BaseCmonException):
    """Exception when user accidentally using a retired argument."""


class RuntimeRunForeverEarlyError(Exception, BaseCmonException):
    """Raised when an error occurs when starting the run_forever of Runtime"""


class DockerVersionError(SystemError, BaseCmonException):
    """Raised when the docker version is incompatible"""


class NoContainerizedError(Exception, BaseCmonException):
    """Raised when trying to use non-containerized Executor in K8s or Docker Compose"""


class PortAlreadyUsed(RuntimeError, BaseCmonException):
    """Raised when trying to use a port which is already used"""


class EstablishGrpcConnectionError(Exception, BaseCmonException):
    """Raised when Exception occurs when establishing or resetting gRPC connection"""


class InternalNetworkError(grpc.aio.AioRpcError, BaseCmonException):
    """
    Raised when communication between microservices fails.
    Needed to propagate information about the root cause event, such as request_id and dest_addr.
    """

    def __init__(
        self,
        og_exception: grpc.aio.AioRpcError,
        request_id: str = '',
        dest_addr: Union[str, Set[str]] = {''},
        details: str = '',
    ):
        """
        :param og_exception: the original exception that caused the network error
        :param request_id: id of the request that caused the error
        :param dest_addr: destination (microservice) address(es) of the problematic network call(s)
        :param details: details of the error
        """
        self.og_exception = og_exception
        self.request_id = request_id
        self.dest_addr = dest_addr
        self._details = details
        super().__init__(
            og_exception.code(),
            og_exception.initial_metadata(),
            og_exception.trailing_metadata(),
            self.details(),
            og_exception.debug_error_string(),
        )

    def __str__(self):
        return self.details()

    def __repr__(self):
        return self.__str__()

    def code(self):
        """
        :return: error code of this exception
        """
        return self.og_exception.code()

    def details(self):
        """
        :return: details of this exception
        """
        if self._details:
            trailing_metadata = extract_trailing_metadata(self.og_exception)
            if trailing_metadata:
                return f'{self._details}\n{trailing_metadata}'
            else:
                return self._details

        return self.og_exception.details()


class ExecutorError(RuntimeError, BaseCmonException):
    """Used to wrap the underlying Executor error that is serialized as a cmon_pb2.StatusProto.ExceptionProto.
    This class is mostly used to propagate the Executor error to the user. The user can decide to act on the error as
    desired.
    """

    def __init__(
        self,
        name: str,
        args: List[str],
        stacks: List[str],
        executor: Optional[str] = None,
    ):
        self._name = name
        self._args = args
        self._stacks = stacks
        self._executor = executor

    @property
    def name(self) -> str:
        """
        :return: the name of the Executor exception
        """
        return self._name

    @property
    def args(self) -> List[str]:
        """
        :return: a list of arguments used to construct the exception
        """
        return self._args

    @property
    def stacks(self) -> List[str]:
        """
        :return: a list of strings that contains the exception traceback
        """
        return self._stacks

    @property
    def executor(self) -> Optional[str]:
        """
        :return: the name of the executor that raised the exception if available
        """
        return self._executor

    def __str__(self):
        return "\n".join(self.stacks)

    def __repr__(self):
        return self.__str__()
