import bge
from bge.logic import expandPath, LibLoad, LibFree, LibList

def camera_collision(cont):
	""" Avoids the camera to pass through objects.
	
	FILE: //libs/actors/player.blend
	OBJECT: player_collision
	FREQUENCY: continuous """
	
	own = cont.owner
	
	# Sensors
	always = cont.sensors[0]
	
	# Objects
	camera = own.childrenRecursive.get("camera")
	camera_axis = own.childrenRecursive.get("camera_axis")
	camera_root = own.childrenRecursive.get("camera_root")
	
	# Properties
	ray = own.rayCast(camera, camera_axis, camera_axis.getDistanceTo(camera_root), "obstacle")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Not detecting obstacle ###
	if ray[0] == None:
		camera.worldPosition = camera_root.worldPosition
		
	### Detecting obstacle ###
	if ray[0] != None:
		camera.worldPosition = ray[1]

def direction_arrow(cont):
	""" Rotates the player's compass arrow to always face north.
	
	FILE: //libs/actors/player.blend
	OBJECT: compass
	FREQUENCY: continuous """
	
	own = cont.owner
	
	# Sensors
	always = cont.sensors[0]
	
	############################
	######## INITIALIZE ########
	############################
	
	### Always rotate compass to north ###
	if always.positive:
		
		own.alignAxisToVect([0.0, 1.0, 0.0], 1, 0.2)

def load_chunks(cont):
	""" This function is intended to load parts of the scenery (named chunks) dynamically based on player position in the world, and this way, being possible to make open world games easily.
	Each part of the scenery is a blend file, named according to its coordinate (in a scale of 100 X 100 meters). """
	
	own = cont.owner
	maps = expandPath("//map/")
	ext = ".blend"
	
	# Sensors
	always = cont.sensors[0]
	in_chunk = cont.sensors[1]
	
	# Functions
	def gen_chunk_name(coords_list):
		"""  Generates a string name of the map chunk, in the format "001_002". """
		
		return str(coords_list[0]).zfill(3) + "_" + str(coords_list[1]).zfill(3)
		
	############################
	######## INITIALIZE ########
	############################
	
	### Load the current chunk at start ###
	if always.positive:
		
		# Chunks
		chunk_current = [own["current_chunk_x"], own["current_chunk_y"]]
		
		if not (maps + gen_chunk_name(chunk_current)) in LibList():
		
			# Load the current chunk at start
			LibLoad(maps + gen_chunk_name(chunk_current) + ext, "Scene", async = False)
			
		print("Player started at " + gen_chunk_name(chunk_current) + ext)
	
	### Load the adjacent chunks when inside a chunk ###
	if in_chunk.positive:
		
		# Chunks
		chunk_current = [in_chunk.hitObject["coord_x"], in_chunk.hitObject["coord_y"]]
		chunk_nw = [chunk_current[0] - 1, chunk_current[1] + 1] # Northwest
		chunk_n = [chunk_current[0], chunk_current[1] + 1] # North
		chunk_ne = [chunk_current[0] + 1, chunk_current[1] + 1] # Northeast
		chunk_w	= [chunk_current[0] - 1, chunk_current[1]] # West
		chunk_e = [chunk_current[0] + 1, chunk_current[1]] # East
		chunk_sw = [chunk_current[0] - 1, chunk_current[1] - 1] # Southwest
		chunk_s = [chunk_current[0], chunk_current[1] - 1] # South
		chunk_se = [chunk_current[0] + 1, chunk_current[1] - 1] # Southeast
		
		# Set current chunk properties in player
		own["current_chunk_x"] = chunk_current[0]
		own["current_chunk_y"] = chunk_current[1]
		
		### Load chunks ###
		# Northwest
		if in_chunk.hitObject["northwest"] and not (maps + gen_chunk_name(chunk_nw) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_nw) + ext, "Scene", async = True)
			
		# North
		if in_chunk.hitObject["north"] and not (maps + gen_chunk_name(chunk_n) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_n) + ext, "Scene", async = True)
			
		# Northeast
		if in_chunk.hitObject["northeast"] and not (maps + gen_chunk_name(chunk_ne) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_ne) + ext, "Scene", async = True)
			
		# West
		if in_chunk.hitObject["west"] and not (maps + gen_chunk_name(chunk_w) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_w) + ext, "Scene", async = True)
			
		# East
		if in_chunk.hitObject["east"] and not (maps + gen_chunk_name(chunk_e) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_e) + ext, "Scene", async = True)
			
		# Southwest
		if in_chunk.hitObject["southwest"] and not (maps + gen_chunk_name(chunk_sw) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_sw) + ext, "Scene", async = True)
			
		# South
		if in_chunk.hitObject["south"] and not (maps + gen_chunk_name(chunk_s) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_s) + ext, "Scene", async = True)
			
		# Southeast
		if in_chunk.hitObject["southeast"] and not (maps + gen_chunk_name(chunk_se) + ext) in LibList():
			LibLoad(maps + gen_chunk_name(chunk_se) + ext, "Scene", async = True)
			
		print("Loaded adjacents of " + str(own["current_chunk_x"]) + "_" + str(own["current_chunk_y"]) + ext)
		
		### Free unused chunks ###
		# Iterate over loaded libs
		for lib in LibList():
			
			# Check if libs have coordinates in its names
			if lib[-13:-10].isnumeric and lib[-9:-6].isnumeric:
				
				lib_coords = [int(lib[-13:-10]), int(lib[-9:-6])]
				
				# Check if lib is 2 chunks away from current coordinates
				if own["current_chunk_x"] > lib_coords[0] + 1 or own["current_chunk_x"] < lib_coords[0] - 1 or own["current_chunk_y"] > lib_coords[1] + 1 or own["current_chunk_y"] < lib_coords[1] - 1:
					
					# Free chunk and warn through message
					LibFree(lib)
					print("Freed", lib[-13:])
					
	### If not in a chunk area ###
	if not in_chunk.positive:
		print("Not in chunk area")
		
