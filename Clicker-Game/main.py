from tkinter import *

window = Tk()
window.minsize(1200, 500)
window.title("Clicker Game")

# general setup
default_font = ("Calibri", 15, "normal")
clicks = 0
click_power = 1
cps = 0

# click power upgrade variables
click_upgrade1_stats = {
    "cost": 15,
    "times bought": 0,
    "click power given": 1,
    "can buy": True,
}

click_upgrade2_stats = {
    "cost": 150,
    "times bought": 0,
    "click power given": 5,
    "can buy": True,
}

# cps upgrade variables
cps_upgrade1_stats = {
    "cost": 100,
    "times bought": 0,
    "cps given": 0.1,
    "can buy": True,
}


class Upgrade:

    def __init__(self, x, y, stats, place_condition, increment_cost, type):
        self.button = None
        global cps, clicks, click_power
        self.x = x
        self.y = y
        self.stats = stats
        self.type = type

        self.cost = stats["cost"]
        self.times_bought = stats["times bought"]
        self.reward_given = stats[f"{self.type} given"]
        self.can_buy = stats["can buy"]
        self.increment_amount = increment_cost

        self.place_condition = place_condition

        self.create_button()

    def get_upgrade(self):
        global clicks
        if clicks < self.cost:
            return not_enough_clicks()
        if self.can_buy:
            self.times_bought += 1
            if self.times_bought == 10:
                self.cost *= 5
                self.reward_given *= 2
                self.config_button("prestige")
                self.increment_amount = (((self.increment_amount - 1) / 2) + 1)
            elif self.times_bought == 11:
                self.cost = int(self.cost / 5)
                clicks -= self.cost
                self.apply_reward()
                self.cost = int(self.cost * self.increment_amount)
                self.config_button("normal")
            elif self.times_bought == 20:
                self.cost *= 10
                self.reward_given *= 10
                self.config_button("ascend")
                self.increment_amount = (((self.increment_amount - 1) / 3) + 1)
            elif self.times_bought == 21:
                self.cost = int(self.cost / 10)
                clicks -= self.cost
                self.apply_reward()
                self.cost = int(self.cost * self.increment_amount)
                self.config_button("normal")
            elif self.times_bought == 30:
                self.apply_reward(multiplier=5)
                self.config_button("max")
                self.can_buy = False
                return
            else:
                clicks -= self.cost
                self.apply_reward()
                self.cost = int(self.cost * self.increment_amount)
                self.config_button("normal")
        else:
            return cannot_buy()

        update_stats()

    def create_button(self):
        self.button = Button(text=f"+{self.reward_given} {self.type.title()}\nCost: {self.cost}", command=self.get_upgrade)

    def apply_reward(self, multiplier=1):
        global cps, click_power
        if self.type == "cps":
            cps += (self.reward_given * multiplier)
        elif self.type == "click power":
            click_power += (self.reward_given * multiplier)
        else:
            return TypeError("Please input a valid type (check __init__ method in upgrade class)")

    def config_button(self, type):
        if type == "prestige":
            self.button.config(text=f"MAX UPGRADES BOUGHT\nPRESTIGE COST: {self.cost}")
        elif type == "ascend":
            self.button.config(text=f"MAX UPGRADES BOUGHT\nASCEND COST: {self.cost}")
        elif type == "max":
            self.button.config(text=f"MAX UPGRADES BOUGHT\nCANNOT BUY ANYMORE")
        elif type == "normal":
            self.button.config(text=f"+{self.reward_given} {self.type.title()}\nCost: {self.cost}")
        else:
            return TypeError("Please input a valid button config type. (check \"config_button\" method "
                             "in upgrade class")

    def place_button(self):
        if eval(self.place_condition):
            self.button.place(x=self.x, y=self.y)


def not_enough_clicks():
    new_label = Label(text="NOT ENOUGH CLICKS", font=("Calibri", 80, "bold"))
    new_label.place(x=125, y=180)
    new_label.after(1000, new_label.destroy)


def cannot_buy():
    new_label = Label(text="CANNOT BUY", font=("Calibri", 60, "bold"))
    new_label.place(x=350, y=180)
    new_label.after(1000, new_label.destroy)


def increase_score(*_):
    global clicks
    clicks += click_power

    clicks *= 99

    click_upgrade1.place_button()
    click_upgrade2.place_button()

    cps_upgrade1.place_button()

    update_stats()


def update_stats(**_):
    verb = "Click" if clicks == 1 else "Clicks"
    click_display.config(text=f"{round(clicks, 1)} {verb}")
    verb = "Click" if click_power == 1 else "Clicks"
    click_power_display.config(text=f"{click_power} {verb} per Button Click")
    cps_display.config(text=f"Clicks per Second: {round(cps, 1)}")


def cps_score_add():
    global clicks, cps
    clicks += cps
    update_stats()
    click_display.after(1000, cps_score_add)


# title text
title_label = Label(text="Clicker Game", font=("Calibri", 30, "bold"))
title_label.grid(column=1, columnspan=2, row=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(1, weight=1)

# click display
click_display = Label(text=f"{clicks} Clicks", font=default_font)
click_display.grid(column=2, row=2)
window.grid_rowconfigure(2, weight=0, pad=70)

# button to click
clicker = Button(text="Click Me", command=increase_score, height=3, width=10, bg="red")
clicker.grid(column=2, row=3)
window.grid_rowconfigure(3, pad=200)

# click power display
click_power_display = Label(text=f"{click_power} Click per Button Click", font=default_font)
click_power_display.place(x=495, y=150)

# cps display
cps_display = Label(text=f"Clicks per Second: {cps}", font=default_font)
cps_display.place(x=510, y=120)

# click power upgrades
click_upgrade1 = Upgrade(x=200, y=50, stats=click_upgrade1_stats, place_condition="clicks >= 15", increment_cost=1.15,
                         type="click power")
click_upgrade2 = Upgrade(x=200, y=100, stats=click_upgrade2_stats, place_condition="clicks >= 150", increment_cost=1.45,
                         type="click power")

# cps upgrades
cps_upgrade1 = Upgrade(x=1000, y=50, stats=cps_upgrade1_stats, place_condition="clicks >= 100", increment_cost=1.30,
                       type="cps")

cps_score_add()

window.mainloop()
