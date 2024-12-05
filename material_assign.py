import bpy
import bpy_extras.image_utils as bpyimage
from bpy_extras.io_utils import ImportHelper
from bpy.types import (Panel, Menu, Operator, PropertyGroup)
from bpy.props import (StringProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty
                       )
from bpy.utils import register_class, unregister_class

bl_info= {
    "name" : "Screenify",
    "blender" : (4, 3, 0),
    }


class ScreenProperties(PropertyGroup):

    x_pixels = IntProperty(
        name = "Horizontal Pixels",
        description="Pixels on the horizontal axis of the screen (X axis)",
        default = 1920,
        min = 0,
        max = 10000,
    )

    y_pixels = IntProperty(
        name = "Vertical Pixels",
        description="Pixels on the vertical axis of the screen (Y axis)",
        default = 1080,
        min = 0,
        max = 10000,
    )

    screen_size = FloatProperty(
        name = "Screen Size in inches",
        description="The size of the display!",
        default = 50,
        min = 0,
    )

    screen_type = EnumProperty(
        name = "Display Type",
        description="Changes the style of display",
        items=[('OP1', 'Regular', ''),
               ('OP2', 'Billboard', ''),
               ('OP2', 'CRT', '')
               ]
    )


    

class ScreenMaterialOperator(bpy.types.Operator):

    bl_idname = "screen_material_operator"
    bl_label = "Assign Screen Material to Specified Object"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        screenception = context.scene.screenception
        self.create_material(screenception)
        return {'FINISHED'}        

    def create_material(self, screenception):
        screen_mat = bpy.data.materials.new(name=f"Screen")
        #self.screen_num += 1
        #Creates additional material every time function is run to avoid issues, may be unnecessary as blender already does this.
        self.create_nodes(screen_mat, screenception)
        self.assign_material(screen_mat)

        
    def create_nodes(self, screen_mat, screenception):
        screen_mat.use_nodes = True
        node_tree = screen_mat.node_tree
        screen_nodes = node_tree.nodes
        nodes = {
        'output_node' : screen_nodes.get('Material Output'),
        'bsdf_node' : screen_nodes.get('Principled BSDF'),
        'combine_rgb' : screen_nodes.new('ShaderNodeCombineColor'),
        'r' : self.mult_template(screen_nodes),
        'g' : self.mult_template(screen_nodes),
        'b' : self.mult_template(screen_nodes),
        'img_node' : screen_nodes.new('ShaderNodeTexImage'),
        'sep_rgb_node_img' : screen_nodes.new('ShaderNodeSeparateColor'),
        'pixel_node' : screen_nodes.new('ShaderNodeTexImage'),
        'sep_rgb_node_pix' : screen_nodes.new('ShaderNodeSeparateColor'),
        'img_mapping_node' : screen_nodes.new('ShaderNodeMapping'),
        'pix_mapping_node' : screen_nodes.new('ShaderNodeMapping'),
        'pixel_scale' : screen_nodes.new('ShaderNodeVectorTransform'),
        'coord_node' : screen_nodes.new('ShaderNodeTexCoord')
        }
        #if self.is_crt:
            #crt_tex = screen_nodes.new("ShaderNodeTexWave")
        

        self.link_nodes(nodes, node_tree)
        self.set_location(nodes)
        self.assign_values(nodes, screenception)

    def mult_template(self, screen_nodes):
        math_template = screen_nodes.new('ShaderNodeMath')
        math_template.operation = 'MULTIPLY'
        return(math_template)

    def set_location(self, nodes):
        x_pos = 200
        counter = 0
        for node in nodes.values():
            if counter%2 == 1:
                node.location = (x_pos, -150)
            else: node.location = (x_pos, 150)
            counter+=1
            x_pos -= 250
        # Somewhat unorganized result, may need to redo later.

    def link_nodes(self, nodes, node_tree):

        links = node_tree.links
        links.new(nodes['coord_node'].outputs['UV'], nodes['img_mapping_node'].inputs[0])
        links.new(nodes['img_mapping_node'].outputs['Vector'], nodes['img_node'].inputs[0])
        links.new(nodes['coord_node'].outputs['UV'], nodes['pix_mapping_node'].inputs[0])
        links.new(nodes['pixel_scale'].outputs['Vector'], nodes['pix_mapping_node'].inputs[3])
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
        links.new(nodes['b'].outputs['Value'], nodes['combine_rgb'].inputs[2])
        links.new(nodes['g'].outputs['Value'], nodes['combine_rgb'].inputs[1])
        links.new(nodes['combine_rgb'].outputs['Color'], nodes['bsdf_node'].inputs[27])
    
    def assign_values(self, nodes, screenception):
        nodes["bsdf_node"].inputs[0].default_value = (0, 0, 0, 1)
        nodes["bsdf_node"].inputs[28].default_value = 1
        nodes["pixel_scale"].inputs[0].default_value[0] = screenception.x_pixels
        nodes["pixel_scale"].inputs[0].default_value[1] = screenception.x_pixels
        nodes["pixel_scale"].inputs[0].default_value[2] = 1


    def assign_material(self, mat):
        obj = bpy.context.active_object
        obj.data.materials[0] = mat

    



class ScreenCreationPanel(Panel):
    bl_label = "Screenception"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "object"


    def draw(self, context):
        layout = self.layout
        screenception = context.scene.screenception
        layout.prop(screenception, "x_pixels")
        layout.prop(screenception, "y_pixels")
        layout.prop(screenception, "screen_size")

        layout.separator(factor=1.5)
        layout.operator("screen_material_operator")


classes = (
    ScreenMaterialOperator,
    ScreenProperties,
    ScreenCreationPanel,
)


def register():
    for c in classes:
        register_class(c)

    bpy.types.Scene.screenception = PointerProperty(ScreenProperties)

def unregister():
    for c in reversed(classes):
        unregister_class(c)
    del bpy.types.Scene.screenception

if __name__ == "__main__":
    register()

    