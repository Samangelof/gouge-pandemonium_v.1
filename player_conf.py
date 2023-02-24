import arcade
import math


# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

SPRITE_SCALING_PLAYER = .3
SPRITE_SCALING_ENEMY = .3


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]




class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 0

        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = SPRITE_SCALING_PLAYER
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = "image/Top_Down_Survivor/rifle/move/"
        self.idle_texture_pair = load_texture_pair(f"{main_path}survivor-move_rifle_0.png")

        self.walk_textures = []
        for i in range(20):
            texture = load_texture_pair(f"{main_path}survivor-move_rifle_{i}.png")
            self.walk_textures.append(texture)


    def update(self):
        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


    def rotate_around_point(self, point: arcade.Point, degrees: float):
        self.angle += degrees
        self.position = arcade.rotate_point(
            self.center_x, self.center_y,
            point[0], point[1], degrees)
        
        
    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING



        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 19 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]




class EnemyCharacter(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)