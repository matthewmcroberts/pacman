from __future__ import annotations

from time import time_ns

from pacman_lib import *


class MyApp(Tk):

    def __init__(self, screenName=None, baseName=None, className="Tk",
                 useTk=True, sync=False, use=None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry("800x600")
        container = Frame(self)
        container.pack(fill="both", expand=True, side="top")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        splash = SplashScreen(container, self)
        splash.grid(row=0, column=0, sticky="news")
        instructions = InstructionScreen(container, self)
        instructions.grid(row=0, column=0, sticky="news")
        playgame = PacmanGameScreen(container, self)
        playgame.grid(row=0, column=0, sticky="news")
        gameover = GameOverScreen(container, self)
        gameover.grid(row=0, column=0, sticky="news")
        menu_screen = MenuScreen(container, self)
        menu_screen.grid(row=0, column=0, sticky="news")
        self.frames = {
            "splash": splash,
            "playgame": playgame,
            "instructions": instructions,
            "gameover": gameover,
            'menu': menu_screen
        }
        self.show_frame("splash")

    def show_frame(self, frame_name: str):
        frame = self.frames[frame_name]
        frame.tkraise()  # Puts frame on top


class AnimatedGameFrame(Frame):
    def __init__(
            self, master=None, delay_time: int = 8, canvas_width: int = 800, canvas_height: int = 600,
            canvas_bg: str = 'white', paused: bool = False):
        super().__init__(master)
        self.delay_time = delay_time
        self.drawables = []
        self.updateables = []
        self.current_time = time_ns() // 1_000_000
        self.delta_time = 0
        self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg=canvas_bg)
        self.canvas.pack()
        self._paused = paused
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def start(self):
        if self._paused:
            self._paused = False
            self.animate()

    def stop(self):
        self._paused = True

    @property
    def is_paused(self):
        return self._paused

    def update(self):
        last_time = self.current_time
        self.current_time = time_ns() // 1_000_000
        self.delta_time = self.current_time - last_time
        for u in self.updateables:
            u.update(self.delta_time)

    def draw(self):
        self.canvas.delete('all')
        for d in self.drawables:
            d.draw(self.canvas)

    def animate(self):
        root = self.winfo_toplevel()
        if not self._paused:
            self.update()
            self.draw()
            root.after(self.delay_time, self.animate)


class PacmanGameScreen(AnimatedGameFrame):
    def __init__(self, master=None, controller: MyApp = None, delay_time: int = 8,
                 canvas_width: int = 452,
                 canvas_height: int = 500, canvas_bg: str = 'white',
                 paused: bool = False):
        super().__init__(master, delay_time, canvas_width,
                         canvas_height, canvas_bg, paused)
        self.controller = controller
        self.load_assets()
        self.drawables = []
        self.updateables = []
        self.entities = []
        self.pills = []
        self.number_of_pills = 300
        self.blanks = []
        self.walls = []
        self.fruits = []
        self.game_over = False

        self.bg = Sprite(0, 0, canvas_width, canvas_height - 200, fill_color='#222222', image=self.bg_image)
        self.drawables.append(self.bg)

        self.pacman = AnimatedMovingSprite(self.pacman_images["Right"], 22, 22, direction=Direction.STOPPED,
                                           border_color="green")
        self.drawables.append(self.pacman)
        self.updateables.append(self.pacman)
        self.entities.append(self.pacman)

        self.red_monster = Monster([self.redghost_image], 222, 220, direction=Direction.UP,
                                   border_color="red")
        self.drawables.append(self.red_monster)
        self.updateables.append(self.red_monster)
        self.entities.append(self.red_monster)

        self.green_monster = Monster([self.greenghost_image], 222, 240, direction=Direction.UP,
                                     border_color="green")
        self.drawables.append(self.green_monster)
        self.updateables.append(self.green_monster)
        self.entities.append(self.green_monster)

        self.yellow_monster = Monster([self.yellowghost_image], 222, 220, direction=Direction.UP,
                                      border_color="yellow")
        self.drawables.append(self.yellow_monster)
        self.updateables.append(self.yellow_monster)
        self.entities.append(self.yellow_monster)

        self.pink_monster = Monster([self.pinkghost_image], 222, 240, direction=Direction.UP,
                                    border_color="pink")
        self.drawables.append(self.pink_monster)
        self.updateables.append(self.pink_monster)
        self.entities.append(self.pink_monster)

        ####Generating Map####
        i = 3
        k = 3
        for row in range(0, len(self.pacman_grid)):
            for col in range(0, len(self.pacman_grid[0])):
                if self.pacman_grid[row][col] == "pill":
                    s = Sprite(i + 5, k + 5, fill_color="white", border_width=1, width=4, height=4)
                    self.pills.append(s)
                elif self.pacman_grid[row][col] == "wall":
                    s = Sprite(i, k, border_color="red", border_width=0, width=16, height=16)
                    self.walls.append(s)
                elif self.pacman_grid[row][col] == "blank":
                    s = Sprite(i, k, border_color="red", border_width=0, width=16, height=16)
                    self.blanks.append(s)
                else:
                    s = Sprite(i, k, border_color="red", border_width=1, width=16, height=16)
                    self.fruits.append(s)
                self.drawables.append(s)
                i += 16
            k += 16
            i = 3
        #####################

        self.bind_keys()
        self.draw()
        self.animate()
        self.update()

    def bind_keys(self):
        self.root = self.winfo_toplevel()
        self.root.bind('<Left>', self.pacman_left)
        self.root.bind('<Right>', self.pacman_right)
        self.root.bind('<Up>', self.pacman_up)
        self.root.bind('<Down>', self.pacman_down)

    def pacman_right(self, evt):
        self.pacman.mover.direction = Direction.RIGHT
        self.pacman.animation.images = self.pacman_images["Right"]

    def pacman_left(self, evt):
        self.pacman.mover.direction = Direction.LEFT
        self.pacman.animation.images = self.pacman_images["Left"]

    def pacman_up(self, evt):
        self.pacman.mover.direction = Direction.UP
        self.pacman.animation.images = self.pacman_images["Up"]

    def pacman_down(self, evt):
        self.pacman.mover.direction = Direction.DOWN
        self.pacman.animation.images = self.pacman_images["Down"]

    def load_assets(self):
        self.bg_image = ImageHelper.get_sized_image('images/Originalpacmaze.png', 452, 500)

        up_image = ImageHelper.get_sized_image('images/pacup.png', 12, 12)
        down_image = ImageHelper.get_sized_image('images/pacdown.png', 12, 12)
        left_image = ImageHelper.get_sized_image('images/pacleft.png', 12, 12)
        right_image = ImageHelper.get_sized_image('images/pacright.png', 12, 12)
        closed_image = ImageHelper.get_sized_image('images/pacclosed.png', 12, 12)
        self.redghost_image = ImageHelper.get_sized_image("images/redghost.png", 12, 12)
        self.yellowghost_image = ImageHelper.get_sized_image("images/yellowghost.png", 12, 12)
        self.greenghost_image = ImageHelper.get_sized_image("images/greenghost.png", 12, 12)
        self.pinkghost_image = ImageHelper.get_sized_image("images/pinkghost.png", 12, 12)

        self.pacman_images = dict({
            "Left": [closed_image, left_image],
            "Right": [closed_image, right_image],
            "Up": [closed_image, up_image],
            "Down": [closed_image, down_image]})

        W = "wall"
        P = "pill"
        B = "blank"
        F = "fruit"

        # 10                           #20
        # 1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6  7  8
        self.pacman_grid = [[W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 1
                            [W, P, P, P, P, P, P, P, P, P, P, P, P, W, W, P, P, P, P, P, P, P, P, P, P, P, P, W],  # 2
                            [W, P, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, P, W],  # 3
                            [W, P, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, P, W],  # 4
                            [W, P, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, P, W],  # 5
                            [W, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, W],  # 6
                            [W, P, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, P, W],  # 7
                            [W, P, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, P, W],  # 8
                            [W, P, P, P, P, P, P, W, W, P, P, P, P, W, W, P, P, P, P, W, W, P, P, P, P, P, P, W],  # 9
                            [W, W, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, W, W],  # 10
                            [W, W, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, W, W],  # 11
                            [W, W, W, W, W, W, P, W, W, P, P, P, P, P, P, P, P, P, P, W, W, P, W, W, W, W, W, W],  # 12
                            [W, W, W, W, W, W, P, W, W, P, W, W, W, B, B, W, W, W, P, W, W, P, W, W, W, W, W, W],  # 13
                            [W, W, W, W, W, W, P, W, W, P, W, B, B, B, B, B, B, W, P, W, W, P, W, W, W, W, W, W],  # 14
                            [P, P, P, P, P, P, P, P, P, P, W, B, B, B, B, B, B, W, P, P, P, P, P, P, P, P, P, P],  # 15
                            [W, W, W, W, W, W, P, W, W, P, W, B, B, B, B, B, B, W, P, W, W, P, W, W, W, W, W, W],  # 16
                            [W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W],  # 17
                            [W, W, W, W, W, W, P, W, W, P, P, P, P, P, P, P, P, P, P, W, W, P, W, W, W, W, W, W],  # 18
                            [W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W],  # 19
                            [W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W],  # 20
                            [W, P, P, P, P, P, P, P, P, P, P, P, P, W, W, P, P, P, P, P, P, P, P, P, P, P, P, W],  # 21
                            [W, P, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, P, W],  # 22
                            [W, P, W, W, W, W, P, W, W, W, W, W, P, W, W, P, W, W, W, W, W, P, W, W, W, W, P, W],  # 23
                            [W, P, P, P, W, W, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, W, W, P, P, P, W],  # 24
                            [W, W, W, P, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, P, W, W, W],  # 25
                            [W, W, W, P, W, W, P, W, W, P, W, W, W, W, W, W, W, W, P, W, W, P, W, W, P, W, W, W],  # 26
                            [W, P, P, P, P, P, P, W, W, P, P, P, P, W, W, P, P, P, P, W, W, P, P, P, P, P, P, W],  # 27
                            [W, P, W, W, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, W, W, P, W],  # 28
                            [W, P, W, W, W, W, W, W, W, W, W, W, P, W, W, P, W, W, W, W, W, W, W, W, W, W, P, W],  # 29
                            [W, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, W],  # 30
                            [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]]  # 31

    def quit(self, evt=None):
        self.root.quit()

    def reset_game(self, evt=None):
        print('reset')
        self.load_assets()
        self.number_of_pills = 300
        i = 3
        k = 3
        for row in range(0, len(self.pacman_grid)):
            for col in range(0, len(self.pacman_grid[0])):
                if self.pacman_grid[row][col] == "pill":
                    s = Sprite(i + 5, k + 5, fill_color="white", border_width=1, width=4, height=4)
                    self.pills.append(s)
                elif self.pacman_grid[row][col] == "wall":
                    s = Sprite(i, k, border_color="red", border_width=0, width=16, height=16)
                    self.walls.append(s)
                elif self.pacman_grid[row][col] == "blank":
                    s = Sprite(i, k, border_color="red", border_width=0, width=16, height=16)
                    self.blanks.append(s)
                else:
                    s = Sprite(i, k, border_color="red", border_width=1, width=16, height=16)
                    self.fruits.append(s)
                self.drawables.append(s)
                i += 16
            k += 16
            i = 3
        self.pacman.sprite.x = 22
        self.pacman.sprite.y = 22
        self.red_monster.sprite.x = 222
        self.red_monster.sprite.y = 220
        self.green_monster.sprite.x = 222
        self.green_monster.sprite.y = 240
        self.yellow_monster.sprite.x = 222
        self.yellow_monster.sprite.y = 240
        self.pink_monster.sprite.x = 222
        self.pink_monster.sprite.y = 240

    def update(self):
        super().update()

        if self.number_of_pills == 0:
            self.stop()
            self.controller.show_frame("gameover")
            call_later(3, self.quit)

        for wall in self.walls:
            for index in range(0, len(self.entities)):
                if self.entities[index].sprite.intersects(wall.bbox()):
                    self.entities[index].mover.backup()
                    if type(self.entities[index]) == Monster:
                        self.entities[index].random_direction()

        for pill in self.pills:
            if self.pacman.sprite.intersects(pill.bbox()):
                for row in range(0, len(self.pacman_grid)):
                    for col in range(0, len(self.pacman_grid[0])):
                        if self.pacman_grid[row][col] == pill:
                            self.pacman_grid[row][col] = "blank"
                self.pacman.sprite.draw(self.canvas)

                pill.fill_color = ""
                pill.border_width = 0
                self.pills.remove(pill)
                self.number_of_pills -= 1

        for entity in self.entities:
            if entity is not self.pacman:
                if entity.sprite.intersects(self.pacman.sprite.bbox()):
                    self.stop()
                    self.controller.show_frame("gameover")
                    call_later(3, self.quit)


    def draw(self):
        super().draw()
        if self.number_of_pills <= 0:
            self.canvas.create_text(452 / 2, 500 / 2, text=f"Game Over", fill="red", font="Times 30 italic bold")


class SplashScreen(Frame):
    def __init__(self, container: Frame, controller: MyApp):
        super().__init__(container, bg='red')
        self.controller = controller
        self.canvas = Canvas(self, width=800, height=600, bg="yellow")
        self.canvas.place(relx=0, rely=0, anchor="nw")
        image = ImageHelper.get_sized_image("images/splashscreen.png", 800,
                                            600)

        self.bg_sprite = Sprite(0, 0, image=image)
        self.bg_sprite.draw(self.canvas)

        call_later_with_param(3, controller.show_frame, 'menu')


class MenuScreen(Frame):
    def __init__(self, container: Frame, controller: MyApp):
        super().__init__(container, bg='blue')

        button1 = Button(self, text='Play Game', command=lambda screen='playgame': controller.show_frame(screen),
                         font=('Comic Sans MS', 30))
        button2 = Button(self, text='Instructions', command=lambda screen='instructions': controller.show_frame(screen),
                         font=('Comic Sans MS', 30))
        button1.place(relx=0.5, rely=.3, anchor="center")
        button2.place(relx=0.5, rely=.5, anchor="center")
        label = Label(self, text='Menu Screen', font=('Comic Sans MS', 44))
        label.place(relx=0.5, rely=0.1, anchor="center")


class InstructionScreen(Frame):
    def __init__(self, container: Frame, controller: MyApp):
        super().__init__(container, bg='blue')
        label = Label(self, text='Collect all pills to win. If a monster hits you, you lose', font=('Comic Sans MS', 12))
        label.place(relx=0.5, rely=0.1, anchor="center")
        button1 = Button(self, text='Back', command=lambda screen='menu': controller.show_frame(screen),
                         font=('Comic Sans MS', 30))
        button1.place(relx=0.5, rely=.3, anchor="center")

class GameOverScreen(Frame):
    def __init__(self, container: Frame, controller: MyApp):
        super().__init__(container, bg='red')
        self.controller = controller
        self.canvas = Canvas(self, width=800, height=600, bg="yellow")
        self.canvas.place(relx=0, rely=0, anchor="nw")
        image = ImageHelper.get_sized_image("images/gameover.jpg", 800,
                                            600)

        self.bg_sprite = Sprite(0, 0, image=image)
        self.bg_sprite.draw(self.canvas)

