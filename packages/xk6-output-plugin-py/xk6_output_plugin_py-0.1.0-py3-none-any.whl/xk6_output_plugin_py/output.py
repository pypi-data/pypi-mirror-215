from concurrent import futures
import sys
import logging
from pythonjsonlogger import jsonlogger

from abc import ABC, abstractmethod

import grpc

from xk6_output_plugin_py.output_pb2 import *
from xk6_output_plugin_py.output_pb2_grpc import *

from grpc_health.v1.health import HealthServicer
from grpc_health.v1 import health_pb2, health_pb2_grpc

__all__ = [
    "Output",
    "Info",
    "Params",
    "Metrics",
    "Submetrics",
    "Samples",
    "MetricType",
    "ValueType",
    "serve",
]


class Output(ABC):
    """Output is the gRPC service to be implemented by output plugins."""

    @abstractmethod
    def Init(self, params):
        """Init is called before registering the output plugin.

        Init receives the environment variables of the k6 process as parameters.
        In addition, standard command line arguments can be used to configure the plugin.
        A description of the plugin and various configuration parameters for the xk6-output-plugin can be returned.

        :param Params params: contains all possible parameters an output plugin may need
        :return: description of the plugin and xk6-output-plugin configuration parameters
        :rtype: Info
        """
        pass

    @abstractmethod
    def Start(self):
        """Start is called before the k6 Engine tries to use the output and should be
        used for any long initialization tasks.
        """
        pass

    @abstractmethod
    def Stop(self):
        """Flush all remaining metrics and finalize the test run."""
        pass

    @abstractmethod
    def AddMetrics(self, metrics):
        """AddMetrics is called on all metrics, the plugin can use it to save metric parameters.

        The call is made before AddSample is called with the given metric's sample.

        :param list[Metric] metrics: array containing metric descriptors
        """
        pass

    @abstractmethod
    def AddSamples(self, samples):
        """AddSamples receives samples of the metrics periodically.
        
        :param list[Sample] samples: an array containing current samples of metrics
        """
        pass


class OutputServicerImpl(object):
    """Implementation of Output service."""

    def __init__(self, impl: Output):
        self.impl = impl

    def Init(self, request, context):
        return InitResponse(info=self.impl.Init(request))

    def Start(self, request, context):
        self.impl.Start()
        return Empty()

    def Stop(self, request, context):
        self.impl.Stop()
        return Empty()


    def AddMetrics(self, request, context):
        self.impl.AddMetrics(request.metrics)
        return Empty()

    def AddSamples(self, request, context):
        self.impl.AddSamples(request.samples)
        return Empty()

def serve(impl:Output):
    """Starts the gRPC server serving the plugin.

    :param Output impl: plugin implementation object
    """

    health = HealthServicer()
    health.set("plugin", health_pb2.HealthCheckResponse.ServingStatus.Value("SERVING"))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_OutputServicer_to_server(OutputServicerImpl(impl), server)
    health_pb2_grpc.add_HealthServicer_to_server(health, server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()

    print(f"1|1|tcp|127.0.0.1:{port}|grpc")
    sys.stdout.flush()

    server.wait_for_termination()

def initLogging():
    logHandler = logging.StreamHandler()
    formatter = LogFormatter("%(level)s %(message)s")
    logHandler.setFormatter(formatter)
    logging.root.addHandler(logHandler)
    logging.root.setLevel(logging.INFO)

class LogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(LogFormatter, self).add_fields(log_record, record, message_dict)
        if log_record.get("level"):
            log_record["@level"] = log_record["level"].lower()
        else:
            log_record["@level"] = record.levelname.lower()
        if log_record['@level'] == 'warning':
            log_record["@level"] = 'warn'
        log_record.pop("level")
        log_record["@message"] = log_record["message"]
        log_record.pop("message")

initLogging()
