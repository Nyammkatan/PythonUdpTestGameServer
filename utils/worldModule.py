from PIL import Image, ImageDraw
import utils.perlin as perlin
import random

class WorldClass:

    w = 300
    h = 300

    DIRT = 1
    DIRT_FLOOR = 0
    ICE = 3
    ICE_FLOOR = 2
    JUNGLE = 5
    JUNGLE_FLOOR = 4
    FIRE = 7
    FIRE_FLOOR = 6
    SAND = 9
    SAND_FLOOR = 8
    RUINS = 11
    RUINS_FLOOR = 10
    NEON = 13
    NEON_FLOOR = 12
    SEW = 15
    SEW_FLOOR = 14
    WATER = 20
    LAVA = 21

    BLOCK_COLORS = {
        DIRT: (89, 59, 43),
        DIRT_FLOOR: (143, 101, 79),
        ICE: (0, 88, 117),
        ICE_FLOOR: (36, 170, 214),
        JUNGLE: (0, 110, 9),
        JUNGLE_FLOOR: (33, 173, 44),
        FIRE: (66, 3, 3),
        FIRE_FLOOR: (152, 123, 124),
        SAND: (135, 117, 0),
        SAND_FLOOR: (219, 196, 44),
        RUINS: (56, 42, 38),

    }

    def __init__(self, seed):
        random.seed(seed)
        self.array = [[0 for i in range(self.w)] for j in range(self.h)]
        self.generateWorld(8)
        self.drawMap()

    def getGeneratedNoiseMap(self, res):
        narray = [[0 for i in range(self.w)] for j in range(self.h)]
        p = perlin.PerlinNoiseFactory(2, octaves=4)
        for i in range(self.h):
            for j in range(self.w):
                value = p(i/res,j/res)
                narray[i][j] = int((value + 1) / 2 * 255 + 0.5)
                narray[i][j]/=255
        return narray

    def generateCaves(self, res):
        map = self.getGeneratedNoiseMap(res)
        for i in range(self.h):
            for j in range(self.w):
                self.array[i][j] = 1 if map[i][j] > 0.5 else 0

    def setBiom(self, biomsMap, start, end, value):
        for i in range(self.h):
            for j in range(self.w):
                if (biomsMap[i][j] >= start and biomsMap[i][j] < end):
                    self.array[i][j] = value if self.array[i][j] == 1 else value-1

    def generateBioms(self, res):
        #Generating BIOMS
        biomsMap = self.getGeneratedNoiseMap(res*20)
        self.drawTestImage(biomsMap, "bioms") #if NEED to DRAW NOISE MAP
        #Generating Ice
        self.setBiom(biomsMap, 0.445, 0.505, self.JUNGLE)
        self.setBiom(biomsMap, 0.52, 0.55, self.ICE)
        self.setBiom(biomsMap, 0.61, 0.66, self.JUNGLE)
        self.setBiom(biomsMap, 0.66, 0.72, self.SAND)
        self.setBiom(biomsMap, 0.0, 0.39, self.FIRE)

    def generateWorld(self, res):
        print("Generating world")
        #Generating dirt
        self.generateCaves(res)
        self.generateBioms(res)

    def drawTestImage(self, map, name):
        im = Image.new("RGB", (self.w, self.h), color="black")
        for i in range(self.h):
            for j in range(self.w):
                im.putpixel((j, i), int(map[j][i]*255))
        im.save(name+".png", "PNG")

    def drawMap(self):
        print("Drawing map")
        im = Image.new("RGB", (self.w, self.h), color="black")
        for i in range(self.h):
            for j in range(self.w):
                im.putpixel((j, i), self.BLOCK_COLORS[self.array[j][i]])
        im.save("test.png", "PNG")
        print("Map drawn")