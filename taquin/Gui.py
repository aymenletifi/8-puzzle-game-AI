import tkinter as tk
import _thread
import time
from PIL import ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from Utils import h1, h2, astar, solvable, get_shuffled
from Etat import Etat

class Gui(tk.Frame):
    def __init__(self, images, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("470x540")
        self.images = [ImageTk.PhotoImage(img) for img in images]
        self.create_widgets()
        self.m_thread = None

    def create_widgets(self):
        self.title = tk.Frame(self.master, width=450, height=50, pady=3)
        self.title.grid(row=1, sticky="ew")
        self.data = tk.Frame(self.master, width=450, height=60, pady=3)
        self.data.grid(row=2, sticky="ew")
        self.fbuttons = tk.Frame(self.master, width=450, height=50, pady=3)
        self.fbuttons.grid(row=0, sticky="ew")


        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.status_label = tk.Label(self.title, text="")
        self.graph = tk.Button(self.fbuttons, text="Solve Puzzle", command=self.solve_puzzle)
        self.graph.grid(row=0, column=0)
        self.graph = tk.Button(self.fbuttons, text="Compare Graphs", command=self.show_graphs)
        self.graph.grid(row=0, column=1)

        self.slots = []
        for i in range(9):
            self.slots.append(tk.Label(self.data, image=self.images[i]))
            self.slots[i].grid(row=i // 3, column=i % 3)
            self.slots[i].image = self.images[0]

        self.status_label.config(font=("Arial", 18))
        self.status_label.pack(side=tk.TOP)

    def set_status(self, text):
        self.status_label.text = text
        self.status_label.config(text=text)

    def set_data(self, data):
        for i, item in enumerate(data):
            self.slots[i].configure(image=self.images[item])
            self.slots[i].image = self.images[item]
    
    def solve_puzzle(self):
        self.m_thread = _thread.start_new_thread(self._solve_puzzle)
    def _solve_puzzle(self):
        final = list(range(9))
        init = [1, 6, 3, 7, 0, 2, 8, 5, 4]


        self.set_status("Generating Puzzle")
        i = 0
        while (i < 5 or not solvable(init)):
            init = get_shuffled()
            time.sleep(.3)
            self.set_data(init)
            i += 1

        self.set_status("Solving Puzzle")
        time.sleep(1)

        etat_initial = Etat(init, h2)
        etat_final = Etat(final, h2)
        print("uuid: ", etat_initial.uuid)

        t_start = time.perf_counter()
        (iters, _, path) = astar(etat_initial, etat_final)
        s = time.perf_counter() - t_start

        self.set_status(f"Solved in {iters} iterations ({s:.4f}s)")
        for item in path:
            time.sleep(.4)
            self.set_data(item.array)
        self.set_status(f"Done in {len(path)} steps!")

    def show_graphs(self):
        self.set_status("Simulating 20 Puzzles")
        self.m_thread = _thread.start_new_thread(self._show_graphs)

    def _show_graphs(self):
        h1_iters = []
        h1_total = []
        h2_iters = []
        h2_total = []

        for _ in range(20):
            final = list(range(9))
            init = get_shuffled()

            while (not solvable(init)):
                init = get_shuffled()

            etat_initial_h1 = Etat(init, h1)
            etat_final_h1 = Etat(final, h1)

            etat_initial_h2 = Etat(init, h2)
            etat_final_h2 = Etat(final, h2)

            (iters, total, _) = astar(etat_initial_h1, etat_final_h1)
            h1_iters.append(iters)
            h1_total.append(total)

            (iters, total, _) = astar(etat_initial_h2, etat_final_h2)
            h2_iters.append(iters)
            h2_total.append(total)
        
        h1_df = pd.DataFrame({"nbre_iter": h1_iters, "nbre_total": h1_total})
        h2_df = pd.DataFrame({"nbre_iter": h2_iters, "nbre_total": h2_total})

        ax = plt.gca()
        h1_df.plot(kind="scatter", x="nbre_total", y="nbre_iter", color="blue", ax=ax, label="h1")
        h2_df.plot(kind="scatter", x="nbre_total", y="nbre_iter", color="red", ax=ax, label="h2")
        plt.xlabel("Total Nodes")
        plt.ylabel("Iterations")
        plt.show()
