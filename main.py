import tkinter as tk

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
DINO_WIDTH = 60
DINO_HEIGHT = 80
LEG_WIDTH = 15
LEG_HEIGHT = 20
HEAD_RADIUS = 20
GROUND_LEVEL = WINDOW_HEIGHT - 100
JUMP_HEIGHT = 150
JUMP_SPEED = 10  # Pixels per frame
ANIMATION_SPEED = 100  # Milliseconds per frame

# Dinosaur class
class Dinosaur:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 50
        self.y = GROUND_LEVEL
        self.dino_color = "green"
        self.leg_toggle = False
        self.jump_active = False
        self.jump_direction = -1  # -1 for up, 1 for down
        self.jump_offset = 0

        # Create dinosaur parts
        self.body = canvas.create_rectangle(
            self.x, self.y - DINO_HEIGHT,
            self.x + DINO_WIDTH, self.y,
            fill=self.dino_color
        )
        self.head = canvas.create_oval(
            self.x + DINO_WIDTH - HEAD_RADIUS * 2, self.y - DINO_HEIGHT - HEAD_RADIUS * 2,
            self.x + DINO_WIDTH, self.y - DINO_HEIGHT,
            fill=self.dino_color
        )
        self.leg_left = canvas.create_rectangle(
            self.x + 5, self.y,
            self.x + 5 + LEG_WIDTH, self.y + LEG_HEIGHT,
            fill=self.dino_color
        )
        self.leg_right = canvas.create_rectangle(
            self.x + DINO_WIDTH - LEG_WIDTH - 5, self.y,
            self.x + DINO_WIDTH - 5, self.y + LEG_HEIGHT,
            fill=self.dino_color
        )

    def animate_legs(self):
        # Simulate leg movement by toggling position
        if self.leg_toggle:
            self.canvas.move(self.leg_left, 5, 0)
            self.canvas.move(self.leg_right, -5, 0)
        else:
            self.canvas.move(self.leg_left, -5, 0)
            self.canvas.move(self.leg_right, 5, 0)
        self.leg_toggle = not self.leg_toggle

    def jump(self):
        if self.jump_active:
            # Move the dinosaur up or down based on jump direction
            self.jump_offset += JUMP_SPEED * self.jump_direction
            self.canvas.move(self.body, 0, JUMP_SPEED * self.jump_direction)
            self.canvas.move(self.head, 0, JUMP_SPEED * self.jump_direction)
            self.canvas.move(self.leg_left, 0, JUMP_SPEED * self.jump_direction)
            self.canvas.move(self.leg_right, 0, JUMP_SPEED * self.jump_direction)

            # Reverse direction at the peak or stop at the ground
            if self.jump_offset <= -JUMP_HEIGHT:
                self.jump_direction = 1
            elif self.jump_offset >= 0:
                self.jump_active = False
                self.jump_direction = -1
                self.jump_offset = 0

    def initiate_jump(self):
        if not self.jump_active:
            self.jump_active = True

# Main application
class DinosaurGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dinosaur Game")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        # Create canvas
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="skyblue")
        self.canvas.pack()

        # Draw ground
        self.canvas.create_rectangle(0, GROUND_LEVEL, WINDOW_WIDTH, WINDOW_HEIGHT, fill="brown")

        # Create dinosaur
        self.dinosaur = Dinosaur(self.canvas)

        # Bind space key for jumping
        self.bind("<space>", lambda event: self.dinosaur.initiate_jump())

        # Start animations
        self.animate()

    def animate(self):
        self.dinosaur.animate_legs()
        self.dinosaur.jump()
        self.after(ANIMATION_SPEED, self.animate)

# Run the game
if __name__ == "__main__":
    game = DinosaurGame()
    game.mainloop()
