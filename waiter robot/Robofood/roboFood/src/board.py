"""GUI."""
import tkinter as tk
from PIL import Image, ImageTk
class Board:
    """GUI Class."""
    def __init__(self, env, stats, x=0 , y=0) -> None:

        self.perf = stats
        self.canva_size = {
            "width": int(1000 / env.col),
            "height": int(500 / env.line),
        }
        self.window = tk.Tk()
        self.window.title("Waiter robot - A*" )
        self.window.iconbitmap(f"../data/robot_waiter_icon.ico")

        frame = tk.Frame(
            self.window,
            bg="grey",
            height=self.canva_size["height"] * env.col,
            width=self.canva_size["width"] * env.line,
        )
        frame.pack(side=tk.LEFT)

        perf_frame = tk.Frame(self.window)
        perf_frame.pack(side=tk.RIGHT)

        stats_lbl = tk.Label(
            perf_frame, text="statistics", font=("Helvetica", 18, "bold"), width=20
        )
        stats_lbl.pack()

        self.stats = {
            "energy_consumed": None,
            "tables_delivered": None,
            "path":"("+str(y)+","+str(x)+")",
        }

        for label in self.stats:
            self.stats[label] = tk.Label(
                perf_frame, text=f"{label} : {self.perf.stats[label]:}"
            )
            self.stats[label].pack()

        total_stats_lbl = tk.Label(
            perf_frame, text="Total statistics", font=("Helvetica", 18, "bold")
        )
        total_stats_lbl.pack()

        self.total_stats = {
            "total_tables_delivered": None,
            "total_energy_consumed": None,
            "total_distance": None,
            "path":None,
        }

        for label in self.total_stats:
            self.total_stats[label] = tk.Label(
                perf_frame, text=f"{label} : {self.perf.total_stats[label]:}"
            )
            self.total_stats[label].pack()

        self.image = {"blank": None, "table": None,  "robot": None}

        for name in self.image:
            self.image[name] = self.load(
                name,
                int(self.canva_size["width"] / 2),
                int(self.canva_size["height"] / 2),
            )

        self.board = [
            [{"table": None,  "robot": None} for _ in range(env.line)]
            for _ in range(env.col)
        ]

        for x in range(env.col):
            for y in range(env.line):
                grid_canv = tk.Canvas(
                    frame,
                    height=self.canva_size["height"],
                    width=self.canva_size["width"],
                    bg="white",
                )
                grid_canv.grid(row=y, column=x, padx=2.5, pady=2.5)

                self.board[x][y]["table"] = tk.Canvas(
                    grid_canv,
                    bg="white",
                    height=self.canva_size["height"] / 2,
                    width=self.canva_size["width"] / 2,
                )
                self.board[x][y]["table"].grid(row=0, column=0)
                self.board[x][y]["table"].create_image(
                    self.canva_size["width"] / 4,
                    self.canva_size["height"] / 4,
                    image=self.image["blank"],
                )
                self.board[x][y]["table"].image = self.image["blank"]

                self.board[x][y]["robot"] = tk.Canvas(
                    grid_canv,
                    bg="white",
                    height=self.canva_size["height"] / 2,
                    width=self.canva_size["width"] / 2,
                )
                self.board[x][y]["robot"].grid(row=1, column=0, columnspan=2)
                self.board[x][y]["robot"].create_image(
                    self.canva_size["width"] / 4,
                    self.canva_size["height"] / 4,
                    image=self.image["blank"],
                )
                self.board[x][y]["robot"].image = self.image["blank"]

    @staticmethod
    def load(name, width_size, height_size) -> ImageTk:
        """Load an image."""
        img = Image.open(f"../data/{name}.webp")
        img = img.resize((width_size, height_size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def display_objet(self, x, y, objet):
        """Displays the image."""
        self.board[x][y][objet].create_image(
            self.canva_size["width"] / 4,
            self.canva_size["height"] / 4,
            image=self.image[objet],
        )
        self.board[x][y][objet].image = self.image[objet]

    def hide_objet(self, objet, x, y):
        """Hide image."""
        self.board[x][y][objet].create_image(
            self.canva_size["width"] / 4,
            self.canva_size["height"] / 4,
            image=self.image["blank"],
        )
        self.board[x][y][objet].image = self.image["blank"]

    def update_stats(self):
        """Update the stats."""
        for label in self.stats:
            self.stats[label].configure(text=f"{label} : {self.perf.stats[label]:}")

        for label in self.total_stats:
            self.total_stats[label].configure(
                text=f"{label} : {self.perf.total_stats[label]:}"
            )
    def display(self):
        """Launch the GUI."""
        self.window.mainloop()
