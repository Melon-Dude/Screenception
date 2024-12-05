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



class ScreenMaterial():

    bl_idname = ""
    bl_label = "Assign Screen Material to Specified Object"
    bl_options = {'REGISTER', 'UNDO'}
    screen_num = 0

    def __init__(self, exists = False):
        self.create_material()
        is_crt = False

    def check_material_exist(self):
        for material in obj.material_slots:
            for num in range(0,10):
                if material.name.replace(str(num),"") == "Screen":
                    self.setup_material(material)
                    #Assign existing material to screen_mat to allow for editing
        return()
            

    def create_material(self):
        screen_mat = bpy.data.materials.new(name=f"Screen")
        #self.screen_num += 1
        #Creates additional material every time function is run to avoid issues, may be unnecessary as blender already does this.
        self.setup_material(screen_mat)
    
    def setup_material(self, screen_mat):
        screen_mat.use_nodes = True
        node_tree = screen_mat.node_tree
        screen_nodes = node_tree.nodes
        self.create_nodes(node_tree, screen_nodes)
        
    def create_nodes( self, node_tree, screen_nodes):
        nodes = {
        'output_node' : screen_nodes.get('Material Output'),
        'bsdf_node' : screen_nodes.get('Principled BSDF'),
        'combine_rgb' : screen_nodes.new('ShaderNodeCombineColor'),
        'r' : screen_nodes.new('ShaderNodeMath'),
        'g' : screen_nodes.new('ShaderNodeMath'),
        'b' : screen_nodes.new('ShaderNodeMath'),
        'img_node' : screen_nodes.new('ShaderNodeTexImage'),
        'sep_rgb_node_img' : screen_nodes.new('ShaderNodeSeparateColor'),
        'pixel_node' : screen_nodes.new('ShaderNodeTexImage'),
        'sep_rgb_node_pix' : screen_nodes.new('ShaderNodeSeparateColor'),
        'img_mapping_node' : screen_nodes.new('ShaderNodeMapping'),
        'pix_mapping_node' : screen_nodes.new('ShaderNodeMapping'),
        'coord_node' : screen_nodes.new('ShaderNodeTexCoord')
        }
        #if self.is_crt:
            #crt_tex = screen_nodes.new("ShaderNodeTexWave")
        
        links = node_tree.links
        links.new(nodes['coord_node'].outputs['UV'], nodes['img_mapping_node'].inputs[0])
        links.new(nodes['img_mapping_node'].outputs['Vector'], nodes['img_node'].inputs[0])
        links.new(nodes['coord_node'].outputs['UV'], nodes['pix_mapping_node'].inputs[0])
        links.new(nodes['pix_mapping_node'].outputs['Vector'], nodes['pixel_node'].inputs[0])
        links.new(nodes['img_node'].outputs['Color'], nodes['sep_rgb_node_img'].inputs[0])
        links.new(nodes['sep_rgb_node_img'].outputs['Red'], nodes['r'].inputs[0])
        links.new(nodes['sep_rgb_node_img'].outputs['Blue'], nodes['b'].inputs[0])
        links.new(nodes['sep_rgb_node_img'].outputs['Green'], nodes['g'].inputs[0])
        links.new(nodes['pixel_node'].outputs['Color'], nodes['sep_rgb_node_pix'].inputs[0])
        links.new(nodes['sep_rgb_node_pix'].outputs['Red'], nodes['r'].inputs[1])
        links.new(nodes['sep_rgb_node_pix'].outputs['Blue'], nodes['b'].inputs[1])
        links.new(nodes['sep_rgb_node_pix'].outputs['Green'], nodes['g'].inputs[1])
        links.new(nodes['r'].outputs['Value'], nodes['combine_rgb'].inputs[0])
        links.new(nodes['r'].outputs['Value'], nodes['combine_rgb'].inputs[1])
        links.new(nodes['r'].outputs['Value'], nodes['combine_rgb'].inputs[2])
        links.new(nodes['combine_rgb'].outputs['Color'], nodes['bsdf_node'].inputs[28])

        self.set_location(nodes)


  
        


    def mult_template(self, screen_nodes):
        math_template = screen_nodes.new('ShaderNodeMath')
        math_template.operation = 'MULTIPLY'
        return(math_template)


    def set_location(self, nodes):
        x_pos = 200
        counter = 0
        for node in nodes.values():
            if counter%2 == 1:
                node.location = (x_pos, -50)
            else: node.location = (x_pos, 50)
            counter+=1
            x_pos -= 250
        # Somewhat unorganized result, may need to redo later.

    def link_nodes(self, nodes, node_tree):
    


        


  
        


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