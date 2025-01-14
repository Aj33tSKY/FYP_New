import bpy
import random
import os
from mathutils import Vector
import math
from math import atan, tan
  
# Parameters
num_renders = 10
delta = 0  # # Parameters for scaling range, Range of scaling: [1 - delta, 1 + delta]
num_blocks = 10 # Number of blocks in each arrangement


Stables = num_renders // 2
Unstables = num_renders // 2
output_folder1 = r"C:\Ajeet\FYP_code\OG_DS\10B-3D-Non_OG\Stable" #Stable Class
output_folder2 = r"C:\Ajeet\FYP_code\OG_DS\10B-3D-Non_OG\Unstable" #Unstable Class
uniform_y_coordinate = 0  # Set a uniform Y-coordinate for all blocks
unique_arrangements = set()

    

# Set up the scene for orthographic 2D rendering
def setup_scene():
    # Clear existing objects (only delete cubes)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
    bpy.ops.object.delete()
    
    # Add ground plane
    bpy.ops.mesh.primitive_plane_add(size=50)
    ground = bpy.context.object
    ground.name = "GroundPlane"
    ground.location = (0, 0, 0) 
    
    # Set ground plane as passive rigid body
    bpy.context.view_layer.objects.active = ground
    bpy.ops.rigidbody.object_add(type='PASSIVE')  # Add rigid body to the ground
    ground.rigid_body.collision_shape = 'BOX'
    
    
def create_block():
     
    # Generate random scaling factors
    scale = random.uniform(1 - delta, 1 + delta)
    block_length = 3.0 * scale
    block_width = 1.0 * scale
    block_height = 1.0  * scale
    # Add a cube to the scene
    bpy.ops.mesh.primitive_cube_add(size=1)
    block = bpy.context.object

    # Scale the block to the specified dimensions
    block.scale = (block_length / 2, block_width / 2, block_height / 2)

    # Apply random rotation for vertical or horizontal orientation
    orientation = random.choices(['horizontal', 'vertical'], weights=[65, 35], k=1)[0]
    if orientation == 'vertical':
        block.rotation_euler[1] = 1.5708  # 90 degrees in radians

    # Apply transformations to reflect the rotation and scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Get block dimensions
    block_height_z = block.dimensions.z
    block_width_x = block.dimensions.x

    return block, block_height_z, block_width_x

def create_block_BIAS():
    # Generate random scaling factors
    scale = random.uniform(1 - delta, 1 + delta)
    block_length = 3.0 * scale
    block_width = 1.0 * scale
    block_height = 1.0 * scale
    
    # Add a cube to the scene
    bpy.ops.mesh.primitive_cube_add(size=1)
    block = bpy.context.object

    # Scale the block to the specified dimensions
    block.scale = (block_length / 2, block_width / 2, block_height / 2)

    # Apply random rotation for vertical or horizontal orientation
    orientation = random.choices(['horizontal', 'vertical'], weights=[25, 75], k=1)[0]
    if orientation == 'vertical':
        block.rotation_euler[1] = 1.5708  # 90 degrees in radians

    # Apply transformations to reflect the rotation and scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Get block dimensions
    block_height_z = block.dimensions.z
    block_width_x = block.dimensions.x

    return block, block_height_z, block_width_x

def create_block_veritcal():
    # Generate random scaling factors
    scale = random.uniform(1 - delta, 1)
    block_length = 3.0 * scale
    block_width = 1.0 * scale
    block_height = 1.0 * scale
    
    # Add a cube to the scene
    bpy.ops.mesh.primitive_cube_add(size=1)
    block = bpy.context.object

    # Scale the block to the specified dimensions
    block.scale = (block_length / 2, block_width / 2, block_height / 2)

    # Apply random rotation for vertical
    block.rotation_euler[1] = 1.5708  # 90 degrees in radians

    # Apply transformations to reflect the rotation and scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Get block dimensions
    block_height_z = block.dimensions.z
    block_width_x = block.dimensions.x

    return block, block_height_z, block_width_x



def create_random_block_arrangement():
    global unique_arrangements  # Make sure to use the global variable
    
    while True:  # Loop until a unique arrangement is found
        # Delete existing blocks
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        for obj in bpy.data.objects:
            if obj.name.startswith("Cube"):  # Assuming your blocks are named "Cube" (default name)
                obj.select_set(True)  # Select blocks to delete
        bpy.ops.object.delete()  # Delete selected objects
        
        last_top_z = 0  # Track the top Z position of the previous block
        next_top_z = 0
        block_locations = []  # Store block locations and dimensions for each block
        block2 = None
        block3 = None
        total_blocks = 0
        
        for i in range(num_blocks):
            if total_blocks >= num_blocks:
               break
            max_top_z_1 = 0
            max_top_z_2 = 0
            max_top_z_3 = 0
            # create and position the block
            if i == 0:
                
                # Create the block and get its height and width
                block, block_height_z, block_width_x = create_block()
                total_blocks += 1
                x_offset = 0  # No offset for the base block
                block.location = (x_offset, uniform_y_coordinate, block_height_z / 2)
                max_top_z_1 = last_top_z + block_height_z
                bpy.context.view_layer.objects.active = block
                bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                block.rigid_body.collision_shape = 'BOX'
                
                if total_blocks < num_blocks and random.random() < 0.35:
                    block2, block2_height_z, block2_width_x = create_block()
                    total_blocks += 1
                    new_max_offset = 0.5
                        
                    new_x_offset = random.uniform(0, new_max_offset)
                    
                    new_x_location = block.location.x + block_width_x / 2 + block2_width_x / 2 + new_x_offset # Apply random offset for x position    
                    # Position the block with random x_offset
                    block2.location = (
                        new_x_location,
                        uniform_y_coordinate,                # All blocks share the same Y-coordinate
                        next_top_z + block2_height_z / 2
                        )         
                    max_top_z_2 = last_top_z + block2_height_z  
                    bpy.context.view_layer.objects.active = block2
                    bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                    block2.rigid_body.collision_shape = 'BOX'
                    
                if total_blocks < num_blocks and random.random() < 0.35:
                    block3, block3_height_z, block3_width_x = create_block()
                    total_blocks += 1
                    new_max_offset = 0.5
                        
                    new_x_offset = random.uniform(0, new_max_offset)
                    
                    new_x_location = block.location.x - block_width_x / 2 - block3_width_x / 2 - new_x_offset # Apply random offset for x position    
                    # Position the block with random x_offset
                    block3.location = (
                        new_x_location,
                        uniform_y_coordinate,                # All blocks share the same Y-coordinate
                        next_top_z + block3_height_z / 2
                        )         
                    max_top_z_3 = last_top_z + block3_height_z  
                    bpy.context.view_layer.objects.active = block3
                    bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                    block3.rigid_body.collision_shape = 'BOX'
                
                
                
            else:
                
                if next_top_z < last_top_z:
                    
                    # Create the block and get its height and width
                    block, block_height_z, block_width_x = create_block_veritcal()
                    total_blocks += 1
                    
                    # Determine the correct dimensions of the previous block's upward-facing face
                    prev_block_width = block_locations[i-1][2]
                    #prev_orientation = block_locations[i-1][5]  # Get orientation of the previous block
                    
                    max_x_offset = (max(prev_block_width, block_width_x)) *0.3
                
                    # Limit x_offset based on contact_length and current block's dimension
                    x_offset = random.uniform(-max_x_offset / 2, max_x_offset / 2)
                
                    x_location = block_locations[i-1][0] + x_offset # Apply random offset for x position
                    
                else:
                    
                # Create the block and get its height and width
                    block, block_height_z, block_width_x = create_block()
                    total_blocks += 1
                    
                    # Determine the correct dimensions of the previous block's upward-facing face
                    prev_block_width = block_locations[i-1][2]
                    #prev_orientation = block_locations[i-1][5]  # Get orientation of the previous block
                        
                    max_x_offset = (max(prev_block_width, block_width_x)) *0.5
                    
                    # Limit x_offset based on contact_length and current block's dimension
                    x_offset = random.uniform(-max_x_offset / 2, max_x_offset / 2)
                    
                    x_location = block_locations[i-1][0] + x_offset # Apply random offset for x position
                

                # Position the block with random x_offset
                #prev_block_top_z = last_top_z + block_height_z / 2
                block.location = (
                    x_location,
                    uniform_y_coordinate,                # All blocks share the same Y-coordinate
                    next_top_z + block_height_z / 2    
                )
                max_top_z_1 = next_top_z + block_height_z
                
                  # Set rigid body physics properties
                bpy.context.view_layer.objects.active = block
                bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                block.rigid_body.collision_shape = 'BOX'
                    
                remaining_right = (block_locations[i-1][0] + block_locations[i-1][2] / 2) - (block.location.x + block_width_x / 2)
                remaining_left = (block.location.x - block_width_x / 2) - (block_locations[i-1][0] - block_locations[i-1][2] / 2)
                if remaining_right > 0.5 and random.random() < 0.75:
                    if total_blocks < num_blocks:
                        if next_top_z < last_top_z:
                            block2, block2_height_z, block2_width_x = create_block_veritcal()
                        else: 
                            block2, block2_height_z, block2_width_x = create_block_BIAS()
                    
                        total_blocks += 1
                        if next_top_z < last_top_z:
                            new_max_offset = remaining_right * 0.2
                        else: 
                            new_max_offset = remaining_right * 0.6
                        
                        new_x_offset = random.uniform(new_max_offset * 0.2, new_max_offset)
                    
                        new_x_location = block.location.x + block_width_x / 2 + block2_width_x / 2 + new_x_offset # Apply random offset for x position
                        
                        
                        # Position the block with random x_offset
                        block2.location = (
                            new_x_location,
                            uniform_y_coordinate,                # All blocks share the same Y-coordinate
                            next_top_z + block2_height_z / 2
                            )
                            
                        max_top_z_2 = next_top_z + block2_height_z
                        
                        bpy.context.view_layer.objects.active = block2
                        bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                        block2.rigid_body.collision_shape = 'BOX'
                    
                if remaining_left > 0.5 and random.random() < 0.75:
                    if total_blocks < num_blocks:
                        if next_top_z < last_top_z:
                            block3, block3_height_z, block3_width_x = create_block_veritcal()
                        else: 
                            block3, block3_height_z, block3_width_x = create_block_BIAS()
                        
                        total_blocks += 1
                        
                        if next_top_z < last_top_z:
                            new_max_offset = remaining_right * 0.2
                        else: 
                            new_max_offset = remaining_right * 0.6
                        
                        new_x_offset = random.uniform(new_max_offset * 0.2, new_max_offset)
                    
                        new_x_location = block.location.x - block_width_x / 2 - block3_width_x / 2 - new_x_offset # Apply random offset for x position

                        # Position the block with random x_offset
                        block3.location = (
                            new_x_location,
                            uniform_y_coordinate,                # All blocks share the same Y-coordinate
                            next_top_z + block3_height_z / 2
                            )
                        max_top_z_3 = next_top_z + block3_height_z
                        
                        bpy.context.view_layer.objects.active = block3
                        bpy.ops.rigidbody.object_add(type='ACTIVE')  # Add rigid body to the block
                        block3.rigid_body.collision_shape = 'BOX'
                

            # Update last_top_z to the top of the tallest block
            #last_top_z = block.location.z + (block_height_z / 2)
            last_top_z = max(max_top_z_1, max_top_z_2, max_top_z_3)
            
            # Choose a random one
            options = [value for value in [max_top_z_1, max_top_z_2, max_top_z_3] if value > 0]
            next_top_z = random.choice(options)

            # Save current block's location, dimensions, and orientation
            if next_top_z == max_top_z_1:
                block_locations.append((block.location.x, block.location.y, block_width_x))
            elif next_top_z == max_top_z_2:
                block_locations.append((block2.location.x, block2.location.y, block2_width_x))
            elif next_top_z == max_top_z_3:
                block_locations.append((block3.location.x, block3.location.y, block3_width_x))
        
        # Convert block_locations to a hashable tuple for uniqueness check
        arrangement_tuple = tuple((loc[0], loc[1]) for loc in block_locations)  # Use (x, y) for uniqueness

        if arrangement_tuple not in unique_arrangements:
            unique_arrangements.add(arrangement_tuple)  # Add unique arrangement to the set
            break  # Exit the loop once a unique arrangement is found


def simulate_stability():
    # Store initial locations of each block to check for movement
    initial_positions = {obj.name: obj.matrix_world.translation.copy() for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.rigid_body}

    # Set the scene to the first frame and allow the simulation to run for a set number of frames
    bpy.context.scene.frame_set(1)  # Set to the initial frame
    
    # Allow the simulation to run for a set number of frames
    for frame in range(1, 20):  # Adjust this range as needed
        bpy.context.scene.frame_set(frame)  # Move to the next frame
        bpy.context.view_layer.update()  # Update the view layer to apply physics changes

    # Check if any block has moved from its initial position
    stable = True
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.name != "GroundPlane" and obj.rigid_body:
            final_position = obj.matrix_world.translation  # Get the world position
            if (final_position - initial_positions[obj.name]).length > 0.01:  # Check if movement occurred
                stable = False
                break
            
            
    # Debugging: Print the initial positions and final positions
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.name != "GroundPlane":
            print(f"{obj.name} - Initial Position: {initial_positions[obj.name]} - Final Position: {obj.matrix_world.translation}")


    return stable, initial_positions


def render_scene(iteration, stability_status):
    # Create the text overlay for the stability status
    #create_text_overlay(stability_status)

    # Get the active camera
    
    # Assign existing cameras by name
    perspective_camera_left = bpy.data.objects.get("Camera_left")
    perspective_camera_right = bpy.data.objects.get("Camera_right")
    ortho_camera = bpy.data.objects.get("Camera") 
    
    cameras = [perspective_camera_left, perspective_camera_right]
    camera_names = ["persp_left", "persp_right"]
    
    #cameras = [ortho_camera, perspective_camera_left, perspective_camera_right]
    #camera_names = ["ortho", "persp_left", "persp_right"]
    
    if ortho_camera:
        # Initialize min and max coordinates for the bounding box
        min_coords = Vector((float('inf'), float('inf'), float('inf')))
        max_coords = Vector((-float('inf'), -float('inf'), -float('inf')))
        
        # Calculate the bounding box for all blocks
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.name != "GroundPlane":
                # Update the min and max coordinates based on the bounding box
                for corner in obj.bound_box:
                    world_coord = obj.matrix_world @ Vector(corner)
                    min_coords.x = min(min_coords.x, world_coord.x)
                    min_coords.y = min(min_coords.y, world_coord.y)
                    min_coords.z = min(min_coords.z, world_coord.z)
                    max_coords.x = max(max_coords.x, world_coord.x)
                    max_coords.y = max(max_coords.y, world_coord.y)
                    max_coords.z = max(max_coords.z, world_coord.z)
        
        # Calculate the center of the bounding box
        center = (max_coords + min_coords) / 2

        # Calculate the total height and width for scaling
        total_height = max_coords.z - min_coords.z  # Get the total height of the blocks
        total_width = max_coords.x - min_coords.x  # Get the total width of the blocks

        
        # Move the camera's Z position to half the maximum height of the blocks
        ortho_camera.location.z = min_coords.z + (total_height * 0.5)  # Adjust height to half of the max height
        
        
        # Lock the camera's X-axis rotation at 90 degrees
        ortho_camera.rotation_euler[0] = 1.5708  # 90 degrees in radians
        ortho_camera.rotation_euler[1] = 0
        ortho_camera.rotation_euler[2] = 0  # Keep Z-axis rotation as needed

        # Adjust the orthographic scale based on the average of total height and width
        ortho_camera.data.ortho_scale = (total_height + total_width) * 1.1 # Average divided by 4 to fit everything in view
        
        
        
        for cam in [perspective_camera_left, perspective_camera_right]:
            if cam:
                cam.location.z = min_coords.z + (total_height * 0.5)  # Adjust height to half of the max height
                cam.location.z = min_coords.z + (total_height * 0.5)
                
                base_focal = 35
                # Adjust focal length based on FOV
                focal_length = (base_focal / total_height)
                
                min_focal_length = 20
                max_focal_length = 50
                 # Inverse proportionality
                focal_length = max_focal_length - ((max_focal_length - min_focal_length) * (total_height / 10))
                focal_length = max(min(focal_length, max_focal_length), min_focal_length)
                # Set the camera focal length
                cam.data.lens = focal_length

        
    

    # Determine the output folder based on stability_status
    if stability_status == "Stable":
        render_folder = output_folder1
    elif stability_status == "Unstable":
        render_folder = output_folder2
    else:
        raise ValueError("Unknown stability status: " + stability_status)
        
    # Set the active camera

    #bpy.context.scene.camera = ortho_camera   
    # Set the render filepath
    #bpy.context.scene.render.filepath = os.path.join(render_folder, f"render_{iteration:02d}.png") 
    # Render the scene
    #bpy.ops.render.render(write_still=True)    

    for cam, cam_name in zip(cameras, camera_names):
        if cam is None:
            print(f"Warning: Camera '{cam_name}' is not found. Skipping render for this camera.")
            continue  # Skip rendering for this camera

        # Set the active camera
        bpy.context.scene.camera = cam
        
        # Set the render filepath
        bpy.context.scene.render.filepath = os.path.join(render_folder, f"render_{iteration:02d}_{cam_name}.png")
        
        # Render the scene
        bpy.ops.render.render(write_still=True)   

    
    # Set the render filepath
    #bpy.context.scene.render.filepath = os.path.join(render_folder, f"render_{iteration:02d}.png")

    # Render the scene
    #bpy.ops.render.render(write_still=True)

    # Remove the text overlay object after rendering
    #for obj in bpy.context.scene.objects:
        #if obj.type == 'FONT':
            #bpy.data.objects.remove(obj, do_unlink=True)


def create_text_overlay(status):
    # Get the active camera
    camera = bpy.context.scene.camera
    if not camera:
        print("Error: No active camera found in the scene.")
        return

    # Add a new text object
    bpy.ops.object.text_add()
    text_object = bpy.context.object
    text_object.data.body = status  # Set the stability status as text
    text_object.scale = (0.3, 0.3, 0.3)  # Adjust the scale to be smaller

    # Set the origin of the text to geometry center
    bpy.context.view_layer.objects.active = text_object
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    # Position the text just below the world origin
    text_object.location = (0, 0, -0.5)  # Position below the origin (Z = -0.5)

    # Align the text to face the camera
    # Calculate the direction from the text object to the camera
    direction_to_camera = camera.location - text_object.location
    direction_to_camera.normalize()  # Normalize the direction vector

    # Get the rotation needed to align the text object to face the camera
    rot_quaternion = direction_to_camera.to_track_quat('Z', 'Y')  # Track the Z axis towards the camera
    text_object.rotation_euler = rot_quaternion.to_euler()  # Convert to Euler angles

    # Ensure the text is selected for rendering
    bpy.context.view_layer.objects.active = text_object



def main():

    #for render_num in range(num_renders):
    Stables_count = 0
    Unstables_count = 0
    max_iterations = num_renders * 5  # Set a reasonable limit
    iteration = 0
    while (Stables_count < Stables or Unstables_count < Unstables) and iteration < max_iterations:
        setup_scene()
        create_random_block_arrangement()
        
        stable, initial_positions = simulate_stability()  # Check stability of the arrangement
        
        if stable and Stables_count < Stables:
            stability_status = "Stable"
            Stables_count += 1
            #print(f"Render {iteration:02d} - Stability: {stability_status}")
            # Set the scene back to the first frame to prepare for rendering
            bpy.context.scene.frame_set(1)  # Reset the frame to the first

            # Render scene
            render_scene(iteration, stability_status)  # Pass the stability status here
        
            iteration += 1
        elif not stable and Unstables_count < Unstables:
            stability_status = "Unstable"
            Unstables_count += 1
            #print(f"Render {iteration:02d} - Stability: {stability_status}")
            # Set the scene back to the first frame to prepare for rendering
            bpy.context.scene.frame_set(1)  # Reset the frame to the first

            # Render scene
            render_scene(iteration, stability_status)  # Pass the stability status here
            
            iteration += 1
            
        else:
            continue


if __name__ == "__main__":
    main()