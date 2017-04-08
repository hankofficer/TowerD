"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from commondef import *
from scene import Scene
from entity import Entity
from tdComponents import CmptCoordinate, CmptEnemy, CmptTower
import pygame


class scene(Scene):
    def __init__(self):
        super(scene, self).__init__()
        self._mode = "idle"
        self.waypoints = [
            (100, 200), (190, 310), (300, 400), (400,
                                                 450), (600, 500), (1000, 550), (1200, 600)
        ]
        self.candidate = None
        self._spawnTimer = 0
        self._spawnInterval = 2
        self._spawnCount = 0
        self._maxSpawn = 5
        self.score = 0
        self.myfont = None

    def objectAdd(self, obj):
        obj.init()
        self._objList.append(obj)

    def objectRemove(self, obj):
        obj.cleanup()
        obj.enable = False
        self._objList.remove(obj)

    def modeSet(self, str):
        self._mode = str
        print("Change to mode: {}".format(self._mode))

    def modeGet(self):
        return self._mode

    def init(self):
        self.myfont = pygame.font.SysFont("arialms", 18)

    def eventHandle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if self.modeGet() == "buildTower":
                    self.modeSet("idle")
                    self.objectDelete(self.candidate)
                elif self.modeGet() == "idle":
                    self.modeSet("buildTower")
                    self.candidate = Tower(self)
                    self.candidate["CmptTower"].selected = True
                    self.objectAdd(self.candidate)
            elif event.key == pygame.K_ESCAPE:
                if self.modeGet() == "buildTower":
                    self.objectRemove(self.candidate)
                self.modeSet("idle")
            elif event.key == pygame.K_RETURN:
                self.modeSet("wave")
                print("start a wave")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse.Left:
            if self.modeGet() == "buildTower":
                self.modeSet("idle")
                self.candidate["CmptTower"].selected = False
                self.candidate = None

    def update(self, dt):
        if self.candidate:
            mPos = pygame.mouse.get_pos()
            self.candidate["CmptCoordinate"].x = mPos[0]
            self.candidate["CmptCoordinate"].y = mPos[1]

        if self.modeGet() == "wave":
            self._spawnTimer += dt
            if self._spawnTimer > self._spawnInterval:
                self._spawnTimer = 0
                if self._spawnCount < self._maxSpawn:
                    e = Enemy(self)
                    for wp in self.waypoints:
                        e["CmptEnemy"].waypoints.append(wp)
                    self.objectAdd(e)
                    self._spawnCount += 1

        for obj in self._objList:
            if not obj.enable:
                continue
            obj.update(dt)
            if "CmptEnemy" in obj.components:
                if len(obj["CmptEnemy"].waypoints) == 0 and \
                    obj["CmptEnemy"].currentDst == None:
                    print("-- Reached")
                    self.score -= 5
                    self.objectRemove(obj)
                elif obj["CmptEnemy"].hp <= 0:
                    print("-- Killed")
                    self.score += 1
                    self.objectRemove(obj)
                    

    def render(self, screen):
        screen.fill((30, 20, 50))

        pygame.draw.lines(screen, (100, 100, 100), False, self.waypoints)

        for obj in self._objList:
            if not obj.enable:
                continue
            obj.render(screen)

        if self.modeGet() == "wave":
            hint = u"如果打完了就關閉遊戲，目前只有這樣而已。"
        else:
            hint = "Press 1 to build towers, Enter to start a wave."
        label = self.myfont.render(hint, True, (255, 255, 255))
        screen.blit(label, (20, 20))
        label = self.myfont.render(u"☀ 分數: {}".format(
            self.score), True, (255, 255, 255))
        screen.blit(label, (20, 40))


class Enemy(Entity):
    def __init__(self, scene):
        super(Enemy, self).__init__(scene)
        self.components = {
            CmptCoordinate.__name__: CmptCoordinate(self),
            CmptEnemy.__name__: CmptEnemy(self)
        }


class Tower(Entity):
    def __init__(self, scene):
        super(Tower, self).__init__(scene)
        self.components = {
            CmptCoordinate.__name__: CmptCoordinate(self),
            CmptTower.__name__: CmptTower(self)
        }
