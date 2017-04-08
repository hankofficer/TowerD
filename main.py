"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
#!/usr/bin/env python

import sys
import pygame

from data.levels import level1
from commondef import *

"""
The game is based on Entity-Component-System concept.
"""
from scene import sceneHandler


class TowerDApp:
    def __init__(self):
        self._gameTitle = "TowerD"
        self._windowSize = (1280, 720)
        self._windowFlags = pygame.DOUBLEBUF
        self._running = True
        self._screen = None
        self._sceneHandler = None

    def init(self):
        pygame.init()
        pygame.display.set_caption(self._gameTitle)

        self._screen = pygame.display.set_mode(
            self._windowSize, self._windowFlags)
        self._running = True
        self._sceneHandler = sceneHandler()
        self._sceneHandler.switchScene(level1.scene())

        return rc.Success

    def eventHandle(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self._sceneHandler.eventHandle(event)

    def update(self, dt):
        self._sceneHandler.update(dt)

    def render(self, screen):
        self._sceneHandler.render(screen)

        # buffer swap
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()

    def execute(self):
        if self.init() != rc.Success:
            self._running = False
            return

        lastTick = 0
        while(self._running):
            currTick = pygame.time.get_ticks()
            dt = (currTick - lastTick) / 1000.0
            lastTick = currTick

            for event in pygame.event.get():
                self.eventHandle(event)
            self.update(dt)
            self.render(self._screen)

        self.cleanup()


if __name__ == "__main__":
    gameApp = TowerDApp()
    gameApp.execute()
