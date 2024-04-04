"""
The turtle_adventure module maintains all classes related to the Turtle's
adventure game.
"""
from turtle import RawTurtle
from gamelib import Game, GameElement
import json
from datetime import datetime
import random

f = open('Level.json')
level_data = json.load(f)


class TurtleGameElement(GameElement):
    """
    An abstract class representing all game elemnets related to the Turtle's
    Adventure game
    """

    def __init__(self, game: "TurtleAdventureGame"):
        super().__init__(game)
        self.__game: "TurtleAdventureGame" = game

    @property
    def game(self) -> "TurtleAdventureGame":
        """
        Get reference to the associated TurtleAnvengerGame instance
        """
        return self.__game


class Waypoint(TurtleGameElement):
    """
    Represent the waypoint to which the player will move.
    """

    def __init__(self, game: "TurtleAdventureGame"):
        super().__init__(game)
        self.__id1: int
        self.__id2: int
        self.__active: bool = False

    def create(self) -> None:
        self.__id1 = self.canvas.create_line(0, 0, 0, 0, width=2, fill="green")
        self.__id2 = self.canvas.create_line(0, 0, 0, 0, width=2, fill="green")

    def delete(self) -> None:
        self.canvas.delete(self.__id1)
        self.canvas.delete(self.__id2)

    def update(self) -> None:
        # there is nothing to update because a waypoint is fixed
        pass

    def render(self) -> None:
        if self.is_active:
            self.canvas.itemconfigure(self.__id1, state="normal")
            self.canvas.itemconfigure(self.__id2, state="normal")
            self.canvas.tag_raise(self.__id1)
            self.canvas.tag_raise(self.__id2)
            self.canvas.coords(self.__id1, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
            self.canvas.coords(self.__id2, self.x - 10, self.y + 10, self.x + 10, self.y - 10)
        else:
            self.canvas.itemconfigure(self.__id1, state="hidden")
            self.canvas.itemconfigure(self.__id2, state="hidden")

    def activate(self, x: float, y: float) -> None:
        """
        Activate this waypoint with the specified location.
        """
        self.__active = True
        self.x = x
        self.y = y

    def deactivate(self) -> None:
        """
        Mark this waypoint as inactive.
        """
        self.__active = False

    @property
    def is_active(self) -> bool:
        """
        Get the flag indicating whether this waypoint is active.
        """
        return self.__active


class Home(TurtleGameElement):
    """
    Represent the player's home.
    """

    def __init__(self, game: "TurtleAdventureGame", pos: tuple[int, int], size: int):
        super().__init__(game)
        self.__id: int
        self.__size: int = size
        x, y = pos
        self.x = x
        self.y = y

    @property
    def size(self) -> int:
        """
        Get or set the size of Home
        """
        return self.__size

    @size.setter
    def size(self, val: int) -> None:
        self.__size = val

    def create(self) -> None:
        self.__id = self.canvas.create_rectangle(0, 0, 0, 0, outline="brown", width=2)

    def delete(self) -> None:
        self.canvas.delete(self.__id)

    def update(self) -> None:
        # there is nothing to update, unless home is allowed to moved
        pass

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2)

    def contains(self, x: float, y: float):
        """
        Check whether home contains the point (x, y).
        """
        x1, x2 = self.x - self.size / 2, self.x + self.size / 2
        y1, y2 = self.y - self.size / 2, self.y + self.size / 2
        return x1 <= x <= x2 and y1 <= y <= y2


class Player(TurtleGameElement):
    """
    Represent the main player, implemented using Python's turtle.
    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 turtle: RawTurtle,
                 speed: float = 5):
        super().__init__(game)
        self.__speed: float = speed
        self.__turtle: RawTurtle = turtle

    def create(self) -> None:
        turtle = RawTurtle(self.canvas)
        turtle.getscreen().tracer(False)  # disable turtle's built-in animation
        turtle.shape("turtle")
        turtle.color("green")
        turtle.penup()

        self.__turtle = turtle

    @property
    def speed(self) -> float:
        """
        Give the player's current speed.
        """
        return self.__speed

    @speed.setter
    def speed(self, val: float) -> None:
        self.__speed = val

    def delete(self) -> None:
        pass

    def update(self) -> None:
        # check if player has arrived home
        if self.game.home.contains(self.x, self.y):
            if self.game.level > 10:
                self.game.game_over_win()
            else:
                self.__turtle.goto(50, self.game.screen_height // 2)
                self.game.level += 1
                self.game.reset()

        turtle = self.__turtle
        waypoint = self.game.waypoint
        if self.game.waypoint.is_active:
            turtle.setheading(turtle.towards(waypoint.x, waypoint.y))
            turtle.forward(self.speed)
            if turtle.distance(waypoint.x, waypoint.y) < self.speed:
                waypoint.deactivate()

    def render(self) -> None:
        self.__turtle.goto(self.x, self.y)
        self.__turtle.getscreen().update()

    # override original property x's getter/setter to use turtle's methods
    # instead
    @property
    def x(self) -> float:
        return self.__turtle.xcor()

    @x.setter
    def x(self, val: float) -> None:
        self.__turtle.setx(val)

    # override original property y's getter/setter to use turtle's methods
    # instead
    @property
    def y(self) -> float:
        return self.__turtle.ycor()

    @y.setter
    def y(self, val: float) -> None:
        self.__turtle.sety(val)


class Enemy(TurtleGameElement):
    """
    Define an abstract enemy for the Turtle's adventure game
    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, speed=1):
        super().__init__(game)
        self.__size = size
        self.__color = color
        self.speed = speed

    @property
    def size(self) -> float:
        """
        Get the size of the enemy
        """
        return self.__size

    @property
    def color(self) -> str:
        """
        Get the color of the enemy
        """
        return self.__color

    def speed(self):
        return self.speed

    def hits_player(self):
        """
        Check whether the enemy is hitting the player
        """
        return (
                (self.x - self.size / 2 <= self.game.player.x <= self.x + self.size / 2)
                and
                (self.y - self.size / 2 <= self.game.player.y <= self.y + self.size / 2)
        )


# TODO
# * Define your enemy classes
# * Implement all methods required by the GameElement abstract class
# * Define enemy's update logic in the update() method
# * Check whether the player hits this enemy, then call the
#   self.game.game_over_lose() method in the TurtleAdventureGame class.
class DemoEnemy(Enemy):
    """
    Demo enemy
    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, speed=1):
        super().__init__(game, size, color, speed)
        self.__id = None

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill="red")

    def update(self) -> None:
        self.x += self.speed
        self.y += self.speed
        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2, )

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class RandomWalkEnemy(Enemy):
    """
    Random walk enemy
    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, speed):
        super().__init__(game, size, color, speed)
        self.__id = None
        self.__state_x = self.state_move_right
        self.__state_y = self.state_move_down

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def state_move_right(self):
        self.move_to(self.x + self.speed, self.y)
        if self.x > self.canvas.winfo_width():  # hit the right border
            self.__state_x = self.state_move_left
        # order affects speed of animation,
        # if put if in front the output will be slower

    def state_move_left(self):
        self.move_to(self.x - self.speed, self.y)
        if self.x < 0:  # hit the left border
            self.__state_x = self.state_move_right

    def state_move_up(self):
        self.move_to(self.x, self.y + self.speed)
        if self.y > self.canvas.winfo_height():  # hit the upper border
            self.__state_y = self.state_move_down

    def state_move_down(self):
        self.move_to(self.x, self.y - self.speed)
        if self.y < 0:  # hit the left border
            self.__state_y = self.state_move_up

    def update(self) -> None:
        self.__state_x()  # call as a function
        self.__state_y()
        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2, )

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class ChasingEnemy(Enemy):
    """
    Chasing enemy
    """

    # to get a smoother path, store data about player's location and delay to get a smoother output

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, speed):
        super().__init__(game, size, color, speed)
        self.__id = None
        if self.game.player.x < self.x:
            self.__state_x = self.state_move_right
        else:
            self.__state_x = self.state_move_left
        if self.game.player.y < self.y:
            self.__state_y = self.state_move_up
        else:
            self.__state_y = self.state_move_down

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def state_move_right(self):
        # self.move_to(self.x + self.speed, self.y)
        self.x += self.speed
        if self.x > self.game.player.x:  # hit the right border
            self.__state_x = self.state_move_left
        # order affects speed of animation,
        # if put if in front the output will be slower

    def state_move_left(self):
        # self.move_to(self.x - self.speed, self.y)
        self.x -= self.speed
        if self.x <= self.game.player.x:  # hit the left border
            self.__state_x = self.state_move_right

    def state_move_up(self):
        # self.move_to(self.x , self.y + self.speed)
        self.y += self.speed
        if self.y > self.game.player.y:  # hit the upper border
            self.__state_y = self.state_move_down

    def state_move_down(self):
        self.y -= self.speed
        # self.move_to(self.x, self.y - self.speed)
        if self.y <= self.game.player.y:  # hit the left border
            self.__state_y = self.state_move_up

    def update(self) -> None:
        self.__state_x()
        self.__state_y()

        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2, )

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class FencingEnemy(Enemy):
    """
    Fencing enemy
    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, offset, speed):
        super().__init__(game, size, color, speed)
        self.__id = None
        self.__move = None
        self.__offset = offset

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def right(self):
        self.x += self.speed

    def left(self):
        self.x -= self.speed

    def up(self):
        self.y += self.speed

    def down(self):
        self.y -= self.speed

    def move_till(self):
        if self.x == self.game.home.x + self.__offset \
                and self.y == self.game.home.y + self.__offset:
            self.__move = self.down

        if self.x == self.game.home.x + self.__offset \
                and self.y == self.game.home.y - self.__offset:
            self.__move = self.left

        if self.x == self.game.home.x - self.__offset \
                and self.y == self.game.home.y - self.__offset:
            self.__move = self.up

        if self.x == self.game.home.x - self.__offset \
                and self.y == self.game.home.y + self.__offset:
            self.__move = self.right
        self.__move()

    def update(self) -> None:
        self.move_till()
        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2, )

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class PowerTwoEnemy(Enemy):
    """
    My enemy (1)

    duplicate in numbers by set x amount of cooldown

    """

    def __init__(self,
                 game: "TurtleAdventureGame",
                 size: int,
                 color: str, cooldown, speed):
        super().__init__(game, size, color, speed)
        self.__id = None
        self.__time = datetime.now().timestamp()
        if self.game.player.x < self.x:
            self.__state_x = self.state_move_right
        else:
            self.__state_x = self.state_move_left
        if self.game.player.y < self.y:
            self.__state_y = self.state_move_up
        else:
            self.__state_y = self.state_move_down
        self.__cooldown = cooldown

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def state_move_right(self):
        # self.move_to(self.x + self.speed, self.y)
        self.x += self.speed
        if self.x > self.game.player.x:  # hit the right border
            self.__state_x = self.state_move_left
        # order affects speed of animation,
        # if put if in front the output will be slower

    def state_move_left(self):
        # self.move_to(self.x - self.speed, self.y)
        self.x -= self.speed
        if self.x <= self.game.player.x:  # hit the left border
            self.__state_x = self.state_move_right

    def state_move_up(self):
        # self.move_to(self.x , self.y + self.speed)
        self.y += self.speed
        if self.y > self.game.player.y:  # hit the upper border
            self.__state_y = self.state_move_down

    def state_move_down(self):
        self.y -= self.speed
        # self.move_to(self.x, self.y - self.speed)
        if self.y <= self.game.player.y:  # hit the left border
            self.__state_y = self.state_move_up

    def update(self) -> None:
        self.__state_x()
        self.__state_y()
        if (datetime.now().timestamp() - self.__time) >= self.__cooldown:
            new_enemy = PowerTwoEnemy(self.game, self.size, self.color, self.__cooldown, self.speed)
            # I wanted it to be directly behind the original enemy, but good enough
            if self.game.player.x - self.x < 0:
                new_enemy.x = self.x + 50
            elif self.game.player.x - self.x == 0:
                new_enemy.x = self.x
            else:
                new_enemy.x = self.x - 50
            if self.game.player.y - self.y < 0:
                new_enemy.y = self.y + 50
            elif self.game.player.y - self.y == 0:
                new_enemy.x = self.y
            else:
                new_enemy.y = self.y - 50
            self.game.add_element(new_enemy)
            self.__time = datetime.now().timestamp()
        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2, )

    def delete(self) -> None:
        self.canvas.delete(self.__id)

    # +detect collision with other enemies


# TODO
# Complete the EnemyGenerator class by inserting code to generate enemies
# based on the given game level; call TurtleAdventureGame's add_enemy() method
# to add enemies to the game at certain points in time.
#
# Hint: the 'game' parameter is a tkinter's frame, so it's after()
# method can be used to schedule some future events.

class EnemyGenerator:
    """
    An EnemyGenerator instance is responsible for creating enemies of various
    kinds and scheduling them to appear at certain points in time.
    """

    def __init__(self, game: "TurtleAdventureGame", level: int):
        self.__game: TurtleAdventureGame = game
        self.__level: int = level

        # example
        self.__game.after(100, self.create_enemy)

    @property
    def game(self) -> "TurtleAdventureGame":
        """
        Get reference to the associated TurtleAdventerGame instance
        """
        return self.__game

    @property
    def level(self) -> int:
        """
        Get the game level
        """
        return self.__level

    def create_enemy(self) -> None:
        """
        Create a new enemy, possibly based on the game level
        """

        level = level_data[str(self.__level)]
        for j in level:
            enemy = j['Enemy']
            speed = j['speed']
            spawn = j['spawn']
            for i in range(spawn):
                if enemy == "RandomWalkEnemy":
                    new_enemy = RandomWalkEnemy(self.__game, 20, "red", speed)
                    x = random.randint(0, self.game.canvas.winfo_width())
                    y = random.randint(0, self.game.canvas.winfo_height())
                    while x in range(int(self.game.player.x - 100), int(self.game.player.x + 100)) \
                            and y in range(int(self.game.player.y - 100), int(self.game.player.y + 100)):
                        x = random.randint(0, self.game.canvas.winfo_width())
                        y = random.randint(0, self.game.canvas.winfo_height())
                    new_enemy.x = x
                    new_enemy.y = y

                elif enemy == "ChasingEnemy":
                    new_enemy = ChasingEnemy(self.__game, 20, "red", speed)
                    x = random.randint(0, self.game.canvas.winfo_width())
                    y = random.randint(0, self.game.canvas.winfo_height())
                    while x in range(int(self.game.player.x - 100), int(self.game.player.x + 100)) \
                            and y in range(int(self.game.player.y - 100), int(self.game.player.y + 100)):
                        x = random.randint(0, self.game.canvas.winfo_width())
                        y = random.randint(0, self.game.canvas.winfo_height())
                    new_enemy.x = x
                    new_enemy.y = y

                elif enemy == "FencingEnemy":
                    offset = j['offset']
                    new_enemy = FencingEnemy(self.__game, 10, "red", offset, speed)
                    x = random.randint(self.game.home.x - offset, self.game.home.x + offset)
                    if x == self.game.home.x - offset or x == self.game.home.x + offset:
                        y = random.randint(self.game.home.y - offset, self.game.home.y + offset)
                    else:
                        y = random.choice([self.game.home.y - offset,self.game.home.y + offset])
                    new_enemy.x = self.game.home.x + offset
                    new_enemy.y = self.game.home.y + offset

                elif enemy == "PowerTwoEnemy":
                    cooldown = j['cooldown']
                    new_enemy = PowerTwoEnemy(self.__game, 20, "red", cooldown, speed)
                    x = random.randint(0, self.game.canvas.winfo_width())
                    y = random.randint(0, self.game.canvas.winfo_height())
                    while x in range(int(self.game.player.x - 100), int(self.game.player.x + 100)) \
                            and y in range(int(self.game.player.y - 100), int(self.game.player.y + 100)):
                        x = random.randint(0, self.game.canvas.winfo_width())
                        y = random.randint(0, self.game.canvas.winfo_height())
                    new_enemy.x = x
                    new_enemy.y = y
                self.game.add_element(new_enemy)
                self.game.enemies.append(new_enemy)


class TurtleAdventureGame(Game):  # pylint: disable=too-many-ancestors
    """
    The main class for Turtle's Adventure.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, parent, screen_width: int, screen_height: int, level: int = 1):
        self.level: int = level
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.waypoint: Waypoint
        self.player: Player
        self.home: Home
        self.enemies: list[Enemy] = []
        self.enemy_generator: EnemyGenerator
        super().__init__(parent)

    def init_game(self):
        self.canvas.config(width=self.screen_width, height=self.screen_height)
        turtle = RawTurtle(self.canvas)
        # set turtle screen's origin to the top-left corner
        turtle.screen.setworldcoordinates(0, self.screen_height - 1, self.screen_width - 1, 0)

        self.waypoint = Waypoint(self)
        self.add_element(self.waypoint)
        self.home = Home(self, (self.screen_width - 100, self.screen_height // 2), 20)
        self.add_element(self.home)
        self.player = Player(self, turtle)
        self.add_element(self.player)
        self.canvas.bind("<Button-1>", lambda e: self.waypoint.activate(e.x, e.y))

        self.enemy_generator = EnemyGenerator(self, level=self.level)

        self.player.x = 50
        self.player.y = self.screen_height // 2


    def add_enemy(self, enemy: Enemy) -> None:
        """
        Add a new enemy into the current game
        """
        self.enemies.append(enemy)
        self.add_element(enemy)

    def game_over_win(self) -> None:
        """
        Called when the player wins the game and stop the game
        """
        self.stop()
        font = ("Arial", 36, "bold")
        self.canvas.create_text(self.screen_width / 2,
                                self.screen_height / 2,
                                text="You Win",
                                font=font,
                                fill="green")

    def game_over_lose(self) -> None:
        """
        Called when the player loses the game and stop the game
        """
        self.stop()
        font = ("Arial", 36, "bold")
        self.canvas.create_text(self.screen_width / 2,
                                self.screen_height / 2,
                                text="You Lose",
                                font=font,
                                fill="red")

    def reset(self):
        for enemy in self.enemies:
            enemy.delete()
        self.enemy_generator = EnemyGenerator(self, level=self.level)
        self.waypoint.deactivate()

f.close()
