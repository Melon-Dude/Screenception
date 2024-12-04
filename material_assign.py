import bpy

bl_info= {
    "name" : "Screenify",
    "blender" : (4, 0, 0),
    
    }

obj = bpy.context.active_object



class AssignScreenMaterial():

    bl_idname = ""
    bl_label = "Assign Screen Material to Specified Object"
    bl_options = {'REGISTER', 'UNDO'}
    screen_num = 0


    def material_exists(self):
        exists = False
        for material in obj.material_slots:
            for num in range(0,10):
                if material.name.replace(str(num),"") == "Screen":
                    exists = True
        return(exists)
            
    

    def create_material(self):
        screen_mat = bpy.data.materials.new(name=f"Screen{self.screen_num}")
        self.screen_num += 1
        #Creates additional material every time function is run to avoid issues
        screen_mat.use_nodes = True
        screen_nodes = screen_mat.node_tree.nodes
        


    def assign_material(obj, self):
        


    def execute(self):
        if self.material_exists():
            
        else:
            self.create_material()

    


def register():


def unregister():


if __name__ == "__main__":
    register()