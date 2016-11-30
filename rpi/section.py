#!/usr/bin/env python


DIRECTIONS = ('forward', 'backward')



class Switch(Section):
    pass


class Section(object):
    
    def __init__(self, name, length, pin_forward, pin_backward, pin_pres_forward, pin_back_forward):
        self.name = name
        self.pin_move_forward = pin_forward
        self.pin_move_backward = pin_backward
        self.pin_pres_forward = pin_pres_forward
        self.pin_pres_backward = pin_pres_backward 
        self.length = length
        self.connections = set()

    @staticmethod
    def _check_direction(direction):
        if direction not in DIRECTIONS:
            raise SectionDirectionError

    def move(self, direction, speed):
        pass

    def get_presense(self):
        direction = None
        presense = False
        if self.pin_pres_forward:
            presense = True
            direction = 'forward'
        elif self.pin_pres_backward:
            presence = True
            direction = 'backward'
        return presence, direction


class SectionDirectionError(Exception):
    pass
