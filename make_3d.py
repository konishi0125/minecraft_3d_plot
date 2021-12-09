import numpy as np
import mcpi.minecraft as minecraft
import mcpi.block as block
import csv
import obj2dot

vertices, uvs, normals, faceVertIDs, uvIDs, normalIDs, vertexColors = \
    obj2dot.loadOBJ('modelpath.obj')
P = np.array(vertices)
P = obj2dot.obj2dot(P, 256)

mc = minecraft.Minecraft()
playerPos = mc.player.getPos()
for p in P:
    mc.setBlock(playerPos.x+p[0],playerPos.y+p[1],playerPos.z+p[2],block.IRON_BLOCK)