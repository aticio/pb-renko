# flake8: noqa
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class PbRenko:
    """Renko initialization class
    """
    def __init__(self, percent, data):
        self.percent = percent
        self.data = data
        self.bricks = []
        self.low_wick = 0
        self.high_wick = 0
    
    def create_pbrenko(self):
        gap = float(self.data[0]) * self.percent / 100
        # print("gap:", gap, "d:", self.data[0])
        for i, d in enumerate(self.data):
            if i == 0:
                if len(self.bricks) == 0:
                    self.bricks.append({"type":"first", "open":float(d), "close":float(d)})
            else:
                if self.bricks[-1]["type"] == "up":
                    if d > self.bricks[-1]["close"]:
                        delta = d - self.bricks[-1]["close"]
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            if self.low_wick == 0:
                                self.add_bricks("up", fcount, gap)
                            else:
                                self.add_bricks("up", fcount, gap, self.low_wick)
                            gap = d * self.percent / 100
                            self.low_wick = 0
                            self.high_wick = 0
                        else:
                            if d > self.high_wick:
                                self.high_wick = d
                    elif d < self.bricks[-1]["open"]:
                        delta = self.bricks[-1]["open"] - d
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            if self.high_wick == 0:
                                self.add_bricks("down", fcount, gap)
                            else:
                                self.add_bricks("down", fcount, gap, self.high_wick)
                            gap = d * self.percent / 100
                            self.high_wick = 0
                            self.low_wick = 0
                        else:
                            if self.low_wick == 0 or d < self.low_wick:
                                self.low_wick = d
                    # print("gap:", gap, "d:", d)
                    # print(self.bricks)
                elif self.bricks[-1]["type"] == "down":
                    if d < self.bricks[-1]["close"]:
                        delta = self.bricks[-1]["close"] - d
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            if self.high_wick == 0:
                                self.add_bricks("down", fcount, gap)
                            else:
                                self.add_bricks("down", fcount, gap, self.high_wick)
                            self.high_wick = 0
                            self.low_wick = 0
                            gap = d * self.percent / 100
                        else:
                            if self.low_wick == 0 or d < self.low_wick:
                                self.low_wick = d
                    elif d > self.bricks[-1]["open"]:
                        delta = d - self.bricks[-1]["open"]
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            if self.low_wick == 0:
                                self.add_bricks("up", fcount, gap)
                            else:
                                self.add_bricks("up", fcount, gap, self.low_wick)
                            self.low_wick = 0
                            self.high_wick = 0
                            gap = d * self.percent / 100
                        else:
                            if d > self.high_wick:
                                self.high_wick = d
                    # print(self.bricks)
                    # print("gap:", gap, "d:", d)
                else:
                    if d > self.bricks[-1]["close"]:
                        delta = d - self.bricks[-1]["close"]
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            self.add_bricks("up", fcount, gap)
                            gap = d * self.percent / 100
                    if d < self.bricks[-1]["close"]:
                        delta = self.bricks[-1]["close"] - d
                        fcount = math.floor(delta / gap)
                        if fcount != 0:
                            self.add_bricks("down", fcount, gap)
                            gap = d * self.percent / 100
                    # print(self.bricks)
                    # print("gap:", gap, "d:", d)


    def add_bricks(self, type, count, brick_size, wick=0):
        """Adds brick(s) to the bricks list
        :param type: type of brick (up or down)
        :type type: string
        :param count: number of bricks to add
        :type count: int
        :param brick_size: brick size
        :type brick_size: float
        """
        for i in range(count):
            if type == "up":
                if self.bricks[-1]["type"] == "up" or self.bricks[-1]["type"] == "first":
                    if wick == 0:
                        self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] + brick_size)})
                    else:
                        if i == 0:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] + brick_size), "low": wick})
                        else:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] + brick_size)})
                elif self.bricks[-1]["type"] == "down":
                    if wick == 0:
                        self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] + brick_size)})
                    else:
                        if i == 0:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] + brick_size), "low": wick})
                        else:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] + brick_size)})
            elif type == "down":
                if self.bricks[-1]["type"] == "up":
                    if wick == 0:
                        self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] - brick_size)})
                    else:
                        if i == 0:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] - brick_size), "high": wick})
                        else:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["open"], "close": (self.bricks[-1]["open"] - brick_size)})
                elif self.bricks[-1]["type"] == "down" or self.bricks[-1]["type"] == "first":
                    if wick == 0:
                        self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] - brick_size)})
                    else:
                        if i == 0:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] - brick_size), "high": wick})
                        else:
                            self.bricks.append({"type": type, "open": self.bricks[-1]["close"], "close": (self.bricks[-1]["close"] - brick_size)})


    def draw_chart(self):
        min_val = self.bricks[0]["close"]
        largest_brick_size = 0
        for b in self.bricks:
            brick_size = abs(b["close"] - b["open"])
            if brick_size > largest_brick_size:
                largest_brick_size = brick_size
            
            if b["close"] < min_val:
                min_val = b["close"]

        brick_width = largest_brick_size / 2
        y_max = 0
        fig, ax = plt.subplots()

        count = 1
        for b in self.bricks:
            y = 0
            color = ""
            if b["type"] == "up":
                y = b["open"]
                color = "green"
            elif b["type"] == "down":
                y = b["close"]
                color = "red"
            else:
                color = "gray"
                y = b["close"]

            if y > y_max:
                y_max = y

            brick_size = (b["close"] * self.percent / 100)
            r = Rectangle((count * brick_width, y), brick_width, brick_size)
            r.set_color(color)

            ax.add_patch(r)
            count = count + 1

        ax.set_xlim(0, count * brick_width)
        ax.set_ylim(min_val - brick_width, y_max + (y_max * 0.02))
        ax.set_axisbelow(True)
        ax.get_xaxis().set_visible(False)

        ticks = np.arange(min_val - brick_width, y_max + (y_max * 0.02), brick_width * 2)
        plt.yticks(ticks)
        plt.grid(linestyle='--', color="#ccd8c0")
        plt.savefig("chart.png")
