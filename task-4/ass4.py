import pysu2
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD

    # Initialize the SU2 solver driver
    try:
        SU2Driver = pysu2.CSinglezoneDriver('turb_SA_flatplate.cfg', 1, comm)
    except TypeError as exception:
        print('A TypeError occurred in pysu2.CDriver:', exception)
        raise

    # Get the marker ID for 'wall'
    AllMarkerIDs = SU2Driver.GetMarkerIndices()
    MarkerName = 'wall'
    MarkerID = AllMarkerIDs[MarkerName] if MarkerName in AllMarkerIDs else -1

    # Number of vertices on the specified marker
    nVertex = SU2Driver.GetNumberMarkerNodes(MarkerID) if MarkerID >= 0 else 0

    # Define linear temperature variation: T = m*x + c
    m = 50.0  # Slope of the temperature variation
    c = 300.0  # Base temperature

    if nVertex > 0:
        for i_vertex in range(SU2Driver.GetNumberMarkerNodes(MarkerID)):
            marker_coords = SU2Driver.MarkerCoordinates(MarkerID)
            x = marker_coords(i_vertex, 0)
            WallTemp = m * x + c  # Linear variation
            SU2Driver.SetMarkerCustomTemperature(MarkerID, i_vertex, WallTemp)

    # Run the solver
    SU2Driver.StartSolver()
    SU2Driver.Finalize()

if __name__ == '__main__':
    main()

