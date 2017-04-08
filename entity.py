"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from commondef import *


class Entity:
    def __init__(self, scene):
        self.scene = scene
        self.name = None
        self.enable = True
        self.components = {}

    def __getitem__(self, cmpt):
        return self.components[cmpt]

    def __setitem__(self, cmpt, val):
        self.components[cmpt] = val

    def init(self):
        for cmptName, cmpt in self.components.items():
            cmpt.init()

    def update(self, dt):
        for cmptName, cmpt in self.components.items():
            cmpt.update(dt)

    def render(self, screen):
        for cmptName, cmpt in self.components.items():
            cmpt.render(screen)

    def cleanup(self):
        pass


class Component:
    def __init__(self, entity):
        self.entity = entity

    def init(self):
        assert 0, "init not implemented"

    def update(self, dt):
        assert 0, "update not implemented"

    def render(self, screen):
        assert 0, "render not implemented"
