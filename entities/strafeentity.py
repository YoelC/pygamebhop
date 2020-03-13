import pygame
from math import sqrt, atan2, sin, cos


def rotate_center(surface, angle, pos):
    to_draw = pygame.transform.rotate(surface, angle)
    new_rect = to_draw.get_rect(center=surface.get_rect(topleft=(pos[0], pos[1])).center)
    return to_draw, new_rect


class StrafeEntity:
    width = 15
    height = 40

    ground_accel = 0.5
    air_accel = 0.5
    max_ground_speed = 3
    max_air_speed = 0.2
    friction = 0.2

    def __init__(self, pos):
        self.pos = pygame.math.Vector2()
        self.pos.xy = pos
        self.vel = pygame.math.Vector2()
        self.vel.xy = 0, 0
        self.angle = 90
        self.on_ground = True
        self.jump_count = 0
        self.max_jump_count = 40

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0))

    def check_jump(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.jump_count >= self.max_jump_count:
            self.jump_count = 0

    def get_wishvel(self):
        w = pygame.key.get_pressed()[pygame.K_w]
        d = pygame.key.get_pressed()[pygame.K_d]
        a = pygame.key.get_pressed()[pygame.K_a]
        s = pygame.key.get_pressed()[pygame.K_s]

        # First calculate movement vector without angle
        wishvel = pygame.math.Vector2()
        wishvel.xy = d - a, w - s

        # Then rotate
        wishvel = wishvel.rotate(self.angle - 90)
        return wishvel

    def accelerate(self, accelerate, max_velocity):
        wishvel = self.get_wishvel()
        proj_vel = self.vel.dot(wishvel)
        print(self.vel.angle_to(wishvel))

        accel_vel = accelerate

        if accel_vel + proj_vel > max_velocity:
            accel_vel = max_velocity - proj_vel

        correct_vel = self.vel + wishvel * accel_vel

        """
        if pygame.key.get_pressed()[pygame.K_w]:
            print(f"Wishvel: {wishvel}")
            print(f"Proj Vel: {proj_vel}")
            print(f"accel_vel: {accel_vel}")
            print(f"correct_vel: {correct_vel}")
            print("______")
        """

        return correct_vel

    def move_air(self):
        return self.accelerate(self.air_accel, self.max_air_speed)

    def move_ground(self):
        speed = self.vel.magnitude()
        if round(speed, 2) != 0:
            drop = speed * self.friction
            self.vel *= max(speed - drop, 0) / speed

        return self.accelerate(self.ground_accel, self.max_ground_speed)

    def move(self):
        if self.jump_count < self.max_jump_count:
            self.on_ground = False
            self.surface.fill((0, 255, 0))
            self.jump_count += 1
        else:
            self.surface.fill((255, 0, 0))
            self.on_ground = True

        self.vel = self.move_ground() if self.on_ground else self.move_air()

        self.pos.x += self.vel.x
        self.pos.y -= self.vel.y

    def draw(self, win):
        to_draw, new_rect = rotate_center(self.surface, self.angle + 90, self.pos)
        win.blit(to_draw, new_rect)