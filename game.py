import random
import sys

import pygame

pygame.init()

WIDTH = 320
HEIGHT = 240
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

clock = pygame.time.Clock()

ROAD_1 = (40, 40, 40, 40)
ROAD_2 = (80, 40, 40, 40)
ROAD_BOUNDS = (40, 40, 80, 40)

for road in (ROAD_1, ROAD_2):
    pygame.draw.rect(screen, BLACK, road)

CAR = (40, 55, 20, 10)
CAR_FORWARD_SPEED = 1
CAR_REVERSE_SPEED = .2
CAR_TURN_SPEED = 1


class Car(object):
    CAR_TURN_SPEED = 1
    ACCELERATION_SPEED = 1
    DECELERATION_SPEED = 2
    DECAY_SPEED = .5
    MAX_SPEED = 10

    def __init__(self, position, size, color, orientation=0.0):
        self._position = position
        self._last_position = position
        self.size = size
        self.color = color
        self._orientation = 0.0
        self._bounds = self._calculate_bounds()
        self._speed = 0

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return u'Car <{position}, {size}, {bounds}>'.format(
            position=self.position,
            size=self.size,
            bounds=self._bounds,
        )

    @property
    def position(self):
        return self._position

    def update_position(self, position):
        print('setting last_position to {position}'.format(position=self._position))
        self._last_position = self._position
        self._position = position

    @property
    def orientation(self):
        return self._orientation

    @property
    def speed(self):
        return self._speed

    @property
    def bounds(self):
        return self._calculate_bounds()

    def _calculate_bounds(self, position=None):
        if position is None:
            print('using this position in _calculate_bounds {0}'.format(position))
            position = self.position
        # ignoring orientation for now
        top_left = (
            position[0] - (self.size[0] / 2),
            position[1] + (self.size[1] / 2),
        )
        top_right = (
            position[0] + (self.size[0] / 2),
            position[1] + (self.size[1] / 2),
        )
        bottom_left = (
            position[0] - (self.size[0] / 2),
            position[1] - (self.size[1] / 2),
        )
        bottom_right = (
            position[0] + (self.size[0] / 2),
            position[1] - (self.size[1] / 2),
        )

        bounding_lines = (
            top_left,
            top_right,
            bottom_right,
            bottom_left,
        )

        return bounding_lines

    def turn(self, direction):
        if direction == 'LEFT':
            self._orientation -= CAR_TURN_SPEED
        elif direction == 'RIGHT':
            self._orientation += CAR_TURN_SPEED

        if self._orientation < 0 or self._orientation >= 360:
            self._orientation = 0

    def draw(self):
        print('last position for drawing bg: {0}'.format(self._last_position))
        print('drawing background at bounds {bounds}'.format(bounds=self._calculate_bounds(position=self._last_position)))
        pygame.draw.polygon(
            screen,
            WHITE,
            self._calculate_bounds(position=self._last_position),
        )
        print('drawing new car at bounds {bounds}'.format(bounds=self.bounds))
        pygame.draw.polygon(
            screen,
            self.color,
            self.bounds,
        )

    def accelerate(self):
        if self._speed < self.MAX_SPEED:
            self._speed += self.ACCELERATION_SPEED

    def decelerate(self):
        if abs(self._speed) < self.MAX_SPEED:
            self._speed -= self.ACCELERATION_SPEED

    def decay_speed(self):
        if self._speed > 0:
            self._speed -= self.DECAY_SPEED
        elif self._speed < 0:
            self._speed += self.DECAY_SPEED

    def update(self):
        # update with heading/orientation, for now just go right/left
        self.update_position((
            (self.position[0] + self._speed),
            self.position[1],
        ))

car = Car(position=[100, 100], size=(40, 40), color=BLUE)

# in the future, during the game loop we'll evaluate all cars
focused_car = car

while True:
    focused_car.update()
    focused_car.draw()
    print(focused_car)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('matched quit event')
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        focused_car.accelerate()
        print('accelerating car')
    elif keys[pygame.K_s]:
        focused_car.decelerate()
        print('decelerating car')
    else:
        focused_car.decay_speed()
    pygame.display.flip()
    print('---- frame drawn ----')
    clock.tick(60)
