"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from commondef import *
from entity import Component

import math
import pygame


class CmptCoordinate(Component):
    def __init__(self, entity):
        super(CmptCoordinate, self).__init__(entity)
        self.x = 0
        self.y = 0

    def init(self):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass


class CmptEnemy(Component):
    def __init__(self, entity):
        super(CmptEnemy, self).__init__(entity)
        self.waypoints = []
        self._maxVelocity = 100
        self.currentDst = None

        self.maxHp = 100
        self.hp = 100
        self.selected = False

    def init(self):
        self.entity["CmptCoordinate"].x = self.waypoints[0][0]
        self.entity["CmptCoordinate"].y = self.waypoints[0][1]

    def update(self, dt):
        x = self.entity["CmptCoordinate"].x
        y = self.entity["CmptCoordinate"].y
        vx = vy = 0

        if self.currentDst != None:
            dx = self.currentDst[0] - x
            dy = self.currentDst[1] - y
            dlen = math.sqrt(dx * dx + dy * dy)

            if dlen < 5:
                vx = vy = 0
                self.currentDst = None
            else:
                vx = self._maxVelocity * dx / dlen
                vy = self._maxVelocity * dy / dlen
        elif len(self.waypoints) > 0:
            self.currentDst = self.waypoints[0]
            self.waypoints.pop(0)

        self.entity["CmptCoordinate"].x += vx * dt
        self.entity["CmptCoordinate"].y += vy * dt

    def render(self, screen):
        x = self.entity["CmptCoordinate"].x
        y = self.entity["CmptCoordinate"].y
        w = 10
        pygame.draw.rect(screen, (255, 255, 100),
                         (x - w / 2, y - w / 2, w, w), 1)

        # hp bar
        if self.selected or True:  # TODO
            barHeight = 3
            barLen = 30 * self.hp / self.maxHp
            barOffsetY = 15
            pygame.draw.rect(screen, (0, 255, 0), (x - barLen / 2,
                                                   y - barOffsetY - barHeight / 2, barLen, barHeight), 0)


class CmptTower(Component):
    def __init__(self, entity):
        super(CmptTower, self).__init__(entity)
        self.selected = False
        self.ready = False
        self._lightTimer = 0
        self._range = 150
        self._cooldown = 1
        self._cooldownTimer = -1  # -1 mean ready
        self.target = None
        self._attack = 10

    def isInRange(self, x, y):
        mx = self.entity["CmptCoordinate"].x
        my = self.entity["CmptCoordinate"].y
        dx = x - mx
        dy = y - my
        dlen = math.sqrt(dx * dx + dy * dy)

        if dlen < self._range:
            return True
        return False

    def init(self):
        pass

    def update(self, dt):
        if self.selected:
            return

        self._lightTimer += dt

        if self._lightTimer > 1:
            self._lightTimer = 0

        if self._cooldownTimer >= 0:
            self._cooldownTimer += dt
            if self._cooldownTimer > self._cooldown:
                self._cooldownTimer = -1

        if self.target == None:
            for obj in self.entity.scene._objList:
                if "CmptEnemy" in obj.components:
                    self.target = obj
                    break

        if self.target != None:
            tx = self.target["CmptCoordinate"].x
            ty = self.target["CmptCoordinate"].y
            thp = self.target["CmptEnemy"].hp

            if self.target.enable and self.isInRange(tx, ty) and thp > 0:
                if self._cooldownTimer < 0:
                    thp -= self._attack
                    self._cooldownTimer = 0
                    self.target["CmptEnemy"].hp = thp
            else:
                self.target = None

    def render(self, screen):
        x = self.entity["CmptCoordinate"].x
        y = self.entity["CmptCoordinate"].y
        w = 15
        dcolor = int(
            155 + 100 * (math.sin(math.pi * 2 * self._lightTimer) + 1) / 2)

        pygame.draw.circle(screen, (100, 100, 100), (x, y), self._range, 1)

        if self.selected:
            pygame.draw.rect(screen, (255, dcolor, dcolor),
                             (x - w / 2, y - w / 2, w, w), 2)
        else:
            pygame.draw.rect(screen, (255, dcolor, dcolor),
                             (x - w / 2, y - w / 2, w, w), 0)

        # shoot a beam on target
        if self.target != None and self._cooldownTimer < 0.2:
            tx = self.target["CmptCoordinate"].x
            ty = self.target["CmptCoordinate"].y
            pygame.draw.line(screen, (255, 255, 0), (x, y), (tx, ty), 4)
