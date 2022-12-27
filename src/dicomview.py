from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify
import vtk as vtkmodule

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

path = "C:\\Users\\DELL E5540\\Desktop\\ImageProcessing\\image\\matlab\\examples\\sample_data\\DICOM\\digest_article"
colors = vtkmodule.vtkNamedColors()
reader = vtkmodule.vtkDICOMImageReader()
volumeMapper = vtkmodule.vtkSmartVolumeMapper()
volumeProperty = vtkmodule.vtkVolumeProperty()
volume = vtkmodule.vtkVolume()

renderer = vtkmodule.vtkRenderer()

renderWindow = vtkmodule.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.OffScreenRenderingOn()

renWinIn = vtkmodule.vtkRenderWindowInteractor()
renWinIn.SetRenderWindow(renderWindow)
renWinIn.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

gradientOpacity = vtkmodule.vtkPiecewiseFunction()
scalarOpacity = vtkmodule.vtkPiecewiseFunction()
color = vtkmodule.vtkColorTransferFunction()

reader.SetDirectoryName(path)
reader.Update()

volumeMapper.SetBlendModeToComposite()
volumeMapper.SetRequestedRenderModeToGPU()
volumeMapper.SetInputData(reader.GetOutput())

volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# Lighting
volumeProperty.SetDiffuse(0.9)
volumeProperty.SetSpecular(0.2)

gradientOpacity.AddPoint(0.0,0.0) # (x,y)
gradientOpacity.AddPoint(2000.0,1.0)
volumeProperty.SetGradientOpacity(gradientOpacity)

scalarOpacity.AddPoint(-800.0, 0.0)
scalarOpacity.AddPoint(-750.0, 1.0)
scalarOpacity.AddPoint(-350.0, 1.0)
scalarOpacity.AddPoint(-300.0, 0.0)
scalarOpacity.AddPoint(-200.0, 0.0)
scalarOpacity.AddPoint(-100.0, 1.0)
scalarOpacity.AddPoint(1000.0, 0.0)
scalarOpacity.AddPoint(2750.0, 0.0)
scalarOpacity.AddPoint(2976.0, 1.0)
scalarOpacity.AddPoint(3000.0, 0.0)
volumeProperty.SetScalarOpacity(scalarOpacity)

color.AddRGBPoint(-750.0, 0.08, 0.05, 0.03) # x,R,G,B
color.AddRGBPoint(-350.0, 0.39, 0.25, 0.16)
color.AddRGBPoint(-200.0, 0.80, 0.80, 0.80)
color.AddRGBPoint(2750.0, 0.70, 0.70, 0.70)
color.AddRGBPoint(3000.0, 0.35, 0.35, 0.35)
volumeProperty.SetColor(color)

volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

renderer.AddVolume(volume)
renderer.ResetCamera()

# -----------------------------------------------------------------------------
# Trame
# -----------------------------------------------------------------------------

server = get_server()
ctrl = server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Dicom Viewer")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            # local rendering
            view = vtk.VtkRemoteView(renderWindow)
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera

    with layout.toolbar:
        vuetify.VSpacer()

        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-restore")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()