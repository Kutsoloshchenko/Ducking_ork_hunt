platform= Ground([".//Grass//Grass_walls.png", 250])
platform.set_possition(301, 288)
self.ground_list.add(platform)

npc= NPC([self, ".//redactor//null_quest"])
npc.set_possition(425, 233)
self.use_list.add(npc)

self.player.set_possition(0,0)