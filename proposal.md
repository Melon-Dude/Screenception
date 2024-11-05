# Screenception 📺🖥️

## Repository
<https://github.com/Melon-Dude/Screenception>

## Description
This addon will take any image input and create a 'screen' material from it in blender, which emulates how real screens work. The user will have many options such as screen dimensions, image resolution and whether or not a TV/monitor model is included (multiple presets will be provided).

## Features
- **Screenify**
	- The main function, will use image input to create a screen material that emulates a real screen, by seperating RGB pixels, an example of the effect can be seen below:
  
  ![Example Gif](docs\example.gif)
- **Make it believable**
	- The addon will add a 'shell' to the screen using pre-existing assets, such as to give the screen a CRT Television shell, or give it a flatscreen TV shell.
- **Automate** 
	- The addon can read the size of an input image and automatically adjust parameters based on that, or can be adjusted manually

## Challenges
- I must learn how to create a blender extension using python by studying the Blender Documentation, a good place to start is here: <https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html>
- I will need to further study blender documentation on how to access assets that I have already created to create an 'instance' of that asset
- I will need to learn how to use python to interface with Blender's shader node system
- I will need to create a functional UI to allow the addon to be easily usable.
- I may need to study imagepy for some image processing needs
- I will need to find/create the TV assets (or create them procedurally, less likely option)

## Outcomes
Ideal Outcome:
- I would like to have an addon that from only a source image can create a good looking screen for set dressing or as a focal point in a photorealistic to stylized realistic environment.

Minimal Viable Outcome:
- To be able to create a shader node tree that applies the pixel filter over an image and if an image is the right size for it, creates a 'shell' for it

## Milestones

- Week 1
  1. Create a functioning addon in blender that spawns an asset
  2. Pass some arguments to effect the outcome
  3. Create a replicable yet customizeable shader tree with python

- Week 2
  1. Create the main 'screenify' part of the program using shader nodes
  2. Allow for user input to modify the output of the function

- Week 3 (Final)
  1. Create UI for the addon
  2. Debug


-   Extra Features (For after due date or if I have extra time)
    1. Option for a cracked screen
    2. Option to specify amount of wear/damage on televisions