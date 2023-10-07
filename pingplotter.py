#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import threading
import time


class PingLatencyTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Latency Tracker")

        self.host_label = ttk.Label(root, text="Enter Host:")
        self.host_label.pack()
        self.host_entry = ttk.Entry(root)
        self.host_entry.pack()

        self.ping_button = ttk.Button(
            root, text="Start Ping", command=self.start_pinging
        )
        self.ping_button.pack()

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        self.ping_times = []
        self.ping_thread = None
        self.is_pinging = False

    def start_pinging(self):
        if not self.is_pinging:
            self.is_pinging = True
            self.host = self.host_entry.get()
            self.ping_times = []

            # Start a new thread to run the ping command
            self.ping_thread = threading.Thread(target=self.ping)
            self.ping_thread.start()

    def ping(self):
        while self.is_pinging:
            try:
                ping_output = subprocess.check_output(["ping", "-c", "1", self.host])
                ping_time = float(ping_output.decode().split("time=")[1].split(" ")[0])
                self.ping_times.append(ping_time)
                self.update_plot()
            except subprocess.CalledProcessError:
                print("Ping failed.")
            time.sleep(1)  # Ping every 1 second

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.ping_times, marker="o")
        self.ax.set_title(f"Ping Latency to {self.host}")
        self.ax.set_xlabel("Ping Count")
        self.ax.set_ylabel("Ping Time (ms)")
        self.canvas.draw()

    def stop_pinging(self):
        self.is_pinging = False
        if self.ping_thread:
            self.ping_thread.join()
        self.ping_thread = None


if __name__ == "__main__":
    root = tk.Tk()
    app = PingLatencyTracker(root)
    root.mainloop()
