# Open World Template
Open world template for UPBGE (Blender Game Engine).

Needs UPBGE 0.1.2 or above to run. Download at: https://download.upbge.org/

Earlier version of UPBGE may work, but official Blender can't run this project.

## Project overview
- libs/actors: contains the "player.blend" library.

- lib/scenery: contains various scenery props, like "buildings.blend", "grass.blend", "rocks.blend" and "trees.blend".

- map: contains map chunks to be loaded at runtime. The scenery is composed through linked libraries (using dupli groups). Note that the map chunks have an offset relative to the world center, and each chunk has a size of 100 X 100 meters. Its names are based on its position in world. See "map_reference.xls" for more information.

- scripts: contains the used scripts. The "player.py" script have functions to be used. The function "load_chunks" is the magic in this project.

- textures: contains the used textures. For now, only the compass has a texture, other models were simply material colored or vertex paint colored.

- open_world.blend: Where the game must run.

- map_reference.xls: a simple map chart, in Excel format.
