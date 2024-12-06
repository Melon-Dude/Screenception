import bpy
import os.path
from bpy.types import (Panel, Operator, PropertyGroup)
from bpy.props import (StringProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty
                       )
from bpy.utils import register_class, unregister_class
from bpy_extras.image_utils import load_image

bl_info= {
    "name" : "Screenify",
    "blender" : (4, 3, 0),
    }


class SC_PG_ScreenProperties(PropertyGroup):

    x_pixels: IntProperty(
        name = "Horizontal Pixels",
        description="Pixels on the horizontal axis of the screen (X axis)",
        default = 1920,
        min = 0,
        max = 10000,
    )

    y_pixels: IntProperty(
        name = "Vertical Pixels",
        description="Pixels on the vertical axis of the screen (Y axis)",
        default = 1080,
        min = 0,
        max = 10000,
    )

    width: FloatProperty(
        name = "Width of screen (in)",
        description="Width of the screen (in)",
        default = 50,
        min = 0,
    )

    height: FloatProperty(
            name = "Height of screen (in)",
            description="Height of the screen (in)",
            default = 50,
            min = 0,
        )
    
    res_scale_fac: FloatProperty(
            name = "Resolution Scale Factor",
            description="Scales image to be a different resolution",
            default = 1,
            min = 0,
            max=5
        )


    emit_strength: FloatProperty(
        name = "Screen Brightness",
        description="How bright the screen is",
        default = 1,
        min = 0,
    )

    screen_type: EnumProperty(
        name = "Display Type",
        description="Changes the style of display",
        items=[('OP1', 'Regular', ''),
               ('OP2', 'Billboard', ''),
               ('OP2', 'CRT', '')
               ]
    )

    img_path: StringProperty(
        name = "Image_Path",
        description="Choose an Image:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )


    

class SC_OT_ScreenMaterialOperator(Operator):

    bl_idname = "sc.material_operator"
    bl_label = "Create Screen Material"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        screenception = context.scene.screenception
        image = bpy.data.images.load(screenception.img_path)
        img_size = image.size
        if screenception.screen_type == "Billboard":
            pixel = bpy.data.images.load(os.path.join('single_pixel_image', 'single_pixel_billboard.png'))
        else:
            pixel = bpy.data.images.load(os.path.join('single_pixel_image', 'single_pixel.png'))
        self.create_mesh()
        self.create_material(screenception, image, pixel, img_size)
        return {'FINISHED'}




    def create_mesh(self, img_res):
        bpy.ops.mesh.primitive_plane_add(align='CURSOR')
        screen_mesh = bpy.context.active_object
        screen_mesh.scale = (img_res[0], img_res[1], 1)




    def calculate_scale(self, screenception):
        #Meter to inch conversion, only technically correct if world unit is in meters, can add feature to check later
        #Divide by 2, as 
        width = ((screenception.width/2)*0.0254) 
        height = ((screenception.height/2)*0.0254) 
        return(width, height, 1)


    def create_material(self, screenception, image, pixel, img_size):
        screen_mat = bpy.data.materials.new(name=f"Screen")
        #self.screen_num += 1
        #Creates additional material every time function is run to avoid issues, may be unnecessary as blender already does this.
        self.create_nodes(screen_mat, screenception, image, pixel, img_size)
        self.assign_material(screen_mat)

        
    def create_nodes(self, screen_mat, screenception, image, pixel, img_size):
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
        if screenception.screen_type == "CRT":
            nodes['wave'] = screen_nodes.new("ShaderNodeTexWave")
            nodes['crt_mix'] = screen_nodes.new("ShaderNodeMix")
        

        self.link_nodes(nodes, node_tree, screenception)
        self.set_location(nodes)
        self.assign_values(nodes, screenception, image, pixel, img_size)

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

    def link_nodes(self, nodes, node_tree, screenception):

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
        if screenception.screen_type == "CRT":
            links.new(nodes['combine_rgb'].outputs['Color'], nodes['crt_mix'].inputs[1])
            links.new(nodes['wave'].outputs['Fac'], nodes['crt_mix'].inputs[2])
            links.new(nodes['crt_mix'].outputs['Result'], nodes['bsdf_node'].inputs[27])
        else:
            links.new(nodes['combine_rgb'].outputs['Color'], nodes['bsdf_node'].inputs[27])


    
    def assign_values(self, nodes, screenception, image, pixel, img_size):
        nodes["bsdf_node"].inputs[0].default_value = (0, 0, 0, 1)
        nodes["bsdf_node"].inputs[28].default_value = screenception.emit_strength
        nodes["pixel_scale"].inputs[0].default_value[0] = img_size[0]
        nodes["pixel_scale"].inputs[0].default_value[1] = img_size[1] //
        nodes["pixel_scale"].inputs[0].default_value[2] = 1
        nodes["img_node"].image = image
        nodes["pixel_node"].image = pixel
        
        if screenception.screen_type == "CRT":
            nodes["wave"].inputs[1].default_value = 15
            nodes["crt_mix"].data_type = 'RGBA'
            nodes["crt_mix"].inputs[0].default_value = .75
        


    def assign_material(self, material):
        obj = bpy.context.active_object
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

    



class OBJECT_PT_ScreenPanel(Panel):
    bl_label = "Screenception"
    bl_category = "Screenception" 
    bl_idname = "OBJECT_PT_screen_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'



    def draw(self, context):
        layout = self.layout
        screenception = context.scene.screenception
        layout.prop(screenception, "x_pixels")
        layout.prop(screenception, "y_pixels")
        layout.separator(factor=1.5)
        layout.prop(screenception, "width")
        layout.prop(screenception, "height")
        layout.separator(factor=1.5)
        layout.prop(screenception, "res_scale_fac")
        layout.prop(screenception, "emit_strength")
        layout.prop(screenception, "screen_type")
        layout.prop(screenception, "img_path")

        layout.separator(factor=1.5)
        layout.operator("sc.material_operator")


classes = (
    SC_OT_ScreenMaterialOperator,
    SC_PG_ScreenProperties,
    OBJECT_PT_ScreenPanel
)


def register():
    for c in classes:
        register_class(c)

    bpy.types.Scene.screenception = PointerProperty(type=SC_PG_ScreenProperties)

def unregister():
    for c in reversed(classes):
        unregister_class(c)
    del bpy.types.Scene.screenception

if __name__ == "__main__":
    register()

    