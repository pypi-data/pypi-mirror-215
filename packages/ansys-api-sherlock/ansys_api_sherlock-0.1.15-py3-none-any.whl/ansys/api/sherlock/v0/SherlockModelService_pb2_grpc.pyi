"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import ansys.api.sherlock.v0.SherlockCommonService_pb2
import ansys.api.sherlock.v0.SherlockModelService_pb2
import grpc

class SherlockModelServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    exportFEAModel: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockModelService_pb2.ExportFEAModelRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Export an FEA Model."""

    exportTraceReinforcementModel: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockModelService_pb2.ExportTraceReinforcementModelRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Export a Trace Reinforcement model."""

    generateTraceModel: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockModelService_pb2.GenerateTraceModelRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Generate a trace model."""


class SherlockModelServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def exportFEAModel(self,
        request: ansys.api.sherlock.v0.SherlockModelService_pb2.ExportFEAModelRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Export an FEA Model."""
        pass

    @abc.abstractmethod
    def exportTraceReinforcementModel(self,
        request: ansys.api.sherlock.v0.SherlockModelService_pb2.ExportTraceReinforcementModelRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Export a Trace Reinforcement model."""
        pass

    @abc.abstractmethod
    def generateTraceModel(self,
        request: ansys.api.sherlock.v0.SherlockModelService_pb2.GenerateTraceModelRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Generate a trace model."""
        pass


def add_SherlockModelServiceServicer_to_server(servicer: SherlockModelServiceServicer, server: grpc.Server) -> None: ...
