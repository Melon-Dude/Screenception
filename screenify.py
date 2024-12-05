import bpy
import bpy_extras.image_utils as bpyimage
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

bl_info= {
    "name" : "Screenify",
    "blender" : (4, 0, 0),
}


class ImageImporter(Operator, ImportHelper):

    bl_idname = "import_image.screenify"
    bl_label = "Create a screen with an imported image"
    bl_options = {'REGISTER', 'UNDO'}


    def load_image(self):
#Add UI identifiers (bl_xxxx)
#def load_image function
#execute function requests image input (using Blender's file management system UI),
#execute function takes user input
#   manual or automatic 'pixel generation'
#   if manual, input width and height
#   option for screen type (electric billboard vs crt vs modern display)
#   option for 'shell' if any (might write in another function)
#create new plane at the correct size of the image (likely using bpy's image loading tools)

        bpyimage.load_image()
    


def register():


def unregister():