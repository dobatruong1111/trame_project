from trame.widgets import vtk, vuetify
import vtk as vtkmodule
from trame.ui.vuetify import SinglePageLayout
from trame.app import get_server

DEFAULT_RESOLUTION = 6

# VTK Pipeline
render = vtkmodule.vtkRenderer()
renWin = vtkmodule.vtkRenderWindow()
renWin.AddRenderer(render)
renWinIn = vtkmodule.vtkRenderWindowInteractor()
renWinIn.SetRenderWindow(renWin)

cone = vtkmodule.vtkConeSource()
cone.SetResolution(8)

map = vtkmodule.vtkPolyDataMapper()
map.SetInputConnection(cone.GetOutputPort())

actor = vtkmodule.vtkActor()
actor.SetMapper(map)

render.AddActor(actor)
render.ResetCamera()

# Trame Setup
server = get_server()
ctrl = server.controller
state = server.state

# Functions
@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone.SetResolution(resolution)
    ctrl.view_update()

def reset_resolution():
    state.resolution = DEFAULT_RESOLUTION

# GUI
with SinglePageLayout(server) as layout:
    layout.title.set_text("Cone Viewer")

    with layout.content:
        # Vuetify component
        with vuetify.VContainer(
                fluid=True, # to get full width container
                classes="pa-0 fill-height" # CSS stylings
        ):
            # local rendering
            view = vtk.VtkLocalView(renWin)
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera

    with layout.toolbar:
        # The VSpacer Vuetify component pushes the extra space on the left side of the component
        vuetify.VSpacer()

        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION), # we defined and initialized state variable
            min=3, 
            max=60, 
            step=1,
            hide_details=True, 
            dense=True,
            style="max-width: 300px"
        )

        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-restore")

        vuetify.VDivider(
            vertical=True, 
            classes="mx-2"
        )

        vuetify.VSwitch(
            v_model="$vuetify.theme.dark", # $vuetify.theme.dark : Vuetify variable
            hide_details=True,
            dense=True
            # The hide_details and dense attribute creates a smaller, tighter switch
        )

        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera): # The VBtn component is a button
            # The click attribute tells the application what method to call when the button is pressed
            vuetify.VIcon("mdi-restore")

if __name__ == "__main__":
    server.start()
