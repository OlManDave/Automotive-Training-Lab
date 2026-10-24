"""Run from Blender's Scripting workspace with Master cylinder v7.blend open.
Exports actual Blender mesh geometry and ABS ON/OFF animation variants for a website.
Requires Blender 4.x/5.x; no third-party add-ons.
"""
import bpy, os, traceback
from pathlib import Path

source=bpy.data.filepath
if not source:
    raise RuntimeError('Save your .blend file before exporting (File > Save As).')
output=Path(source).parent/'Brake_Classroom_Website'
output.mkdir(exist_ok=True)
scene=bpy.context.scene
original_frame=scene.frame_current
original_selection=list(bpy.context.selected_objects)
original_active=bpy.context.view_layer.objects.active
# Do not alter the user's saved .blend. We work in memory; reload after exporting.
# Convert Blender curves, pipes, torus profiles, and text labels to meshes so GLB includes them.
for mode in ('OFF','ON'):
    control=bpy.data.texts.get('ABS_'+mode)
    if control is None:
        raise RuntimeError('ABS_'+mode+' text block not found. Is this the V7 project?')
    exec(compile(control.as_string(), 'ABS_'+mode, 'exec'), {'bpy':bpy})
    scene.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT')
    originals=[o for o in scene.objects if o.type in {'MESH','CURVE','FONT','SURFACE'} and not o.hide_render]
    copies=[]
    for obj in originals:
        clone=obj.copy()
        clone.data=obj.data.copy()
        # Prevent links to original parents from changing export transforms
        clone.parent=None
        clone.matrix_world=obj.matrix_world.copy()
        scene.collection.objects.link(clone)
        clone.name='WEB_'+obj.name
        copies.append(clone)
    for clone in copies:
        if clone.type in {'CURVE','FONT','SURFACE'}:
            bpy.ops.object.select_all(action='DESELECT')
            clone.select_set(True)
            bpy.context.view_layer.objects.active=clone
            bpy.ops.object.convert(target='MESH')
    bpy.ops.object.select_all(action='DESELECT')
    for clone in copies:
        clone.select_set(True)
    bpy.context.view_layer.objects.active=copies[0]
    path=str(output/('brakes_abs_'+mode.lower()+'.glb'))
    # The GLB exporter bakes object animation to web-compatible glTF animation clips.
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
        export_animations=True, export_frame_range=True, export_frame_step=1,
        export_force_sampling=True, export_apply=False, export_cameras=False,
        export_lights=False)
    print('EXPORTED',path,os.path.getsize(path),'bytes')
    bpy.ops.object.select_all(action='DESELECT')
    for clone in copies:
        bpy.data.objects.remove(clone,do_unlink=True)
    # Reset original selection before next mode
scene.frame_set(original_frame)
for obj in original_selection:
    if obj.name in bpy.data.objects:obj.select_set(True)
if original_active and original_active.name in bpy.data.objects:
    bpy.context.view_layer.objects.active=original_active
print('SUCCESS. Copy the website index.html into:',output)
print('DO NOT SAVE this Blender session after exporting; reopen the original .blend to restore ABS mode.')
