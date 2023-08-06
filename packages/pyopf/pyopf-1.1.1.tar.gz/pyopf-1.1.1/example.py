from pyopf.io import load

from pyopf.resolve import resolve
from pyopf.uid64 import Uid64

# Path to the example project file.
project_path = "../opf-spec/examples/project.json"

# We are going to search for the calibrated position of the camera with this ID
camera_id = Uid64(hex = "0x57282923")

# Load the json data and resolve the project, i.e. load the project items as named attributes.
project = load(project_path)
project = resolve(project)

# Many objects are optional in OPF. If they are missing, they are set to None.
if project.calibration is None:
    print("No calibration data.")
    exit(1)

print(len(project.calibration.calibrated_cameras.cameras))
print(len(project.calibration.calibrated_control_points.points))
print(len(project.constraints.scale_constraints))
print(project.camera_list)

# Filter the list of calibrated cameras to find the one with the ID we are looking for.
calibrated_camera = [camera for camera in project.calibration.calibrated_cameras.cameras if camera.id == camera_id]

# Print the pose of the camera.
print("The camera {} is calibrated at:".format(camera_id), calibrated_camera[0].position)
print("with orientation", calibrated_camera[0].orientation_deg)
