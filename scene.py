"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from commondef import *


class Scene:
    def __init__(self):
        self._objList = []

    def init(self):
        assert 0, "init is not implemented"

    def eventHandle(self, event):
        assert 0, "eventHandle is not implemented"

    def update(self, dt):
        assert 0, "update is not implemented"

    def render(self, screen):
        assert 0, "render is not implemented"


class sceneHandler:
    def __init__(self):
        self._currScene = None

    def switchScene(self, scene):
        self._currScene = scene
        if self._currScene != None:
            self._currScene.init()

    def eventHandle(self, event):
        if self._currScene != None:
            self._currScene.eventHandle(event)

    def update(self, dt):
        if self._currScene != None:
            self._currScene.update(dt)

    def render(self, screen):
        if self._currScene != None:
            self._currScene.render(screen)
