import bpy
import bpy_extras.image_utils as bpyimage
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

bl_info= {
    "name" : "Screenify",
    "blender" : (4, 3, 0),
    
    }

obj = bpy.context.active_object

class LoadImage():
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



class AssignScreenMaterial():

    bl_idname = ""
    bl_label = "Assign Screen Material to Specified Object"
    bl_options = {'REGISTER', 'UNDO'}
    screen_num = 0

    def __init__(self):
        self.create_material()

    def check_material_existance(self):
        exists = False
        for material in obj.material_slots:
            for num in range(0,10):
                if material.name.replace(str(num),"") == "Screen":
                    self.setup_material(material)
                    #Assign existing material to screen_mat to allow for editing
        return(exists)
            

    def create_material(self):
        screen_mat = bpy.data.materials.new(name=f"Screen")
        #self.screen_num += 1
        #Creates additional material every time function is run to avoid issues, may be unnecessary as blender already does this.
        self.setup_material(screen_mat)
    
    def setup_material(self, screen_mat):
        screen_mat.use_nodes = True
        node_tree = screen_mat.node_tree
        screen_nodes = node_tree.nodes
        self.create_nodes(screen_nodes)
        

    def create_nodes( self, screen_nodes):
        bsdf_node = screen_nodes.get('Principled BSDF')
        output_node = screen_nodes.get('Material Output')
        img_node = screen_nodes.new('ShaderNodeTexImage')
        sep_rgb_node_img = screen_nodes.new('ShaderNodeSeparateColor')
        pixel_node = screen_nodes.new('ShaderNodeTexImage')
        sep_rgb_node_pix = screen_nodes.new('ShaderNodeSeparateColor')
        mult_nodes = self.create_mult_nodes(screen_nodes)
        mapping_node = screen_nodes.new('ShaderNodeMapping')
        coord_node = screen_nodes.new('ShaderNodeTexCoord')

        node_list = [output_node, bsdf_node, mult_nodes["r"], mult_nodes["b"], mult_nodes["g"], sep_rgb_node_img, img_node, sep_rgb_node_pix, pixel_node, mapping_node, coord_node]
        self.set_location(node_list)
        return(node_list)




    def create_mult_nodes(self, screen_nodes):
        math_template = screen_nodes.new('ShaderNodeMath')
        math_template.operation = 'MULTIPLY'
        return({
        'r' : math_template,
        'g' : math_template,
        'b' : math_template
        }
        )


    def set_location(self, node_list):
        x_pos = 200
        counter = 0
        for node in node_list:
            if counter%2 == 1:
                node.location = (x_pos, -50)
            else: node.location = (x_pos, 50)
            counter+=1
            x_pos -= 250


        


  
        


    def execute(self):
        self.create_material
        

        return {'FINISHED'}
    



AssignScreenMaterial

def register():
    bpy.utils.register_class(AssignScreenMaterial)

def unregister():
 bpy.utils.unregister_class(AssignScreenMaterial)

if __name__ == "__main__":
    register()