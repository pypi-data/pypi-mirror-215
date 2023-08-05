"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import ansys.api.sherlock.v0.SherlockCommonService_pb2
import ansys.api.sherlock.v0.SherlockPartsService_pb2
import grpc

class SherlockPartsServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    listPartsLibraries: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsLibrariesRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsLibrariesResponse] = ...
    """List the available parts libraries."""

    updatePartsList: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsListRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsListResponse] = ...
    """Update the parts list for a project's CCA."""

    listPartsNotUpdated: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsNotUpdatedRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsNotUpdatedResponse] = ...
    """List the parts that have not been updated from the Sherlock Part Library."""

    updateLeadModeling: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdateLeadModelingRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Enable lead modeling for all non LEADLESS parts leads in a project's CCA."""

    exportPartsList: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ExportPartsListRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Export parts list for all parts given a project's CCA."""

    importPartsList: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.ImportPartsListRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Import a parts list for a given a project's CCA."""

    setPartLocation: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.SetPartLocationRequest,
        ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode] = ...
    """Set a part's location."""

    updatePartsLocations: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsResponse] = ...
    """Update one or more parts' locations."""

    updatePartsLocationsByFile: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsByFileRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsByFileResponse] = ...
    """Update one or more parts' locations using a CSV file."""

    getPartLocationUnits: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationUnitsRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationUnitsResponse] = ...
    """Get a list of valid part location units."""

    getBoardSides: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetBoardSidesRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetBoardSidesResponse] = ...
    """Get a list of valid board side values."""

    getPartLocation: grpc.UnaryUnaryMultiCallable[
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationRequest,
        ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationResponse] = ...
    """Get the location properties for a part."""


class SherlockPartsServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def listPartsLibraries(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsLibrariesRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsLibrariesResponse:
        """List the available parts libraries."""
        pass

    @abc.abstractmethod
    def updatePartsList(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsListRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsListResponse:
        """Update the parts list for a project's CCA."""
        pass

    @abc.abstractmethod
    def listPartsNotUpdated(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsNotUpdatedRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.ListPartsNotUpdatedResponse:
        """List the parts that have not been updated from the Sherlock Part Library."""
        pass

    @abc.abstractmethod
    def updateLeadModeling(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdateLeadModelingRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Enable lead modeling for all non LEADLESS parts leads in a project's CCA."""
        pass

    @abc.abstractmethod
    def exportPartsList(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.ExportPartsListRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Export parts list for all parts given a project's CCA."""
        pass

    @abc.abstractmethod
    def importPartsList(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.ImportPartsListRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Import a parts list for a given a project's CCA."""
        pass

    @abc.abstractmethod
    def setPartLocation(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.SetPartLocationRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockCommonService_pb2.ReturnCode:
        """Set a part's location."""
        pass

    @abc.abstractmethod
    def updatePartsLocations(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsResponse:
        """Update one or more parts' locations."""
        pass

    @abc.abstractmethod
    def updatePartsLocationsByFile(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsByFileRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.UpdatePartsLocationsByFileResponse:
        """Update one or more parts' locations using a CSV file."""
        pass

    @abc.abstractmethod
    def getPartLocationUnits(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationUnitsRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationUnitsResponse:
        """Get a list of valid part location units."""
        pass

    @abc.abstractmethod
    def getBoardSides(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.GetBoardSidesRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.GetBoardSidesResponse:
        """Get a list of valid board side values."""
        pass

    @abc.abstractmethod
    def getPartLocation(self,
        request: ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.sherlock.v0.SherlockPartsService_pb2.GetPartLocationResponse:
        """Get the location properties for a part."""
        pass


def add_SherlockPartsServiceServicer_to_server(servicer: SherlockPartsServiceServicer, server: grpc.Server) -> None: ...
