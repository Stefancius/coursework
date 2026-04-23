

import sys
import os
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from robots.ecosystem.factory import ecofactory
from robots.ecosystem.ecosystem import distance

def bot_charge_threshold(bot): #decide the threshiold battery when the bot must ggo to charge 
    if bot.kind == "Robot":
        return 0.18
    elif bot.kind== "Droid":
        return 0.22
    elif bot.kind == "Drone":
        return 0.30
    return 0.20

def nearst_charger(bot, chargers): #return closest charge to bot 
    best =None
    best_dist= float("inf")
    for charger in chargers:
        d = distance(bot.coordinates, charger.coordinates)
        if d < best_dist:
            best_dist= d
            best = charger
    return best

def pick_pizza_for_bot(bot, pizzas): #find the best pizza for a bot to deliver
    best= None
    best_dist = float("inf")

    for pizza in pizzas:
        if pizza.status != "ready": #pizza must be ready 
            continue
        if pizza.weight > bot.max_payload: #mathes weight limit for bot
            continue

        d = distance(bot.coordinates, pizza.coordinates)
        if d < best_dist: #showtest distance between bot and pizza
            best_dist =d
            best =pizza

    return best

def optimised_version():
    es = ecofactory(
        robots=3,
        droids=3,
        drones= 3,
        chargers= ([20, 20], [60, 20]),
        pizzas=9
    )

    es.display(show=0)
    es.messages_on = False
    es.debug =False
    es.duration= 50

    home = [0, 0, 0]

    while es.active:
        chargers = es.chargers()

        for bot in es.bots():
            threshold = bot_charge_threshold(bot)
            soc_ratio = bot.soc / bot.max_soc

            if soc_ratio < threshold and bot.station is None:
                charger = nearst_charger(bot, chargers)
                if charger is not None:
                    bot.charge(charger)

            elif bot.activity == "idle":
                pizza = pick_pizza_for_bot(bot, es.deliverables())
                if pizza is not None:
                    bot.deliver(pizza)
                elif not bot.destination and bot.coordinates != home:
                    bot.target_destination = home

            if bot.target_destination:
                bot.move()

        es.update()

    return es

def kpis(es, label): #calculate and print measuremants for the simulation 
    bot_registers = list(es.registry(kind_class="Bot").values())

    units = sum(r["units_delivered"] for r in bot_registers)
    weight = sum(r["weight_delivered"] for r in bot_registers)
    total_distance = sum(r["distance"] for r in bot_registers)
    energy = sum(r["energy"] for r in bot_registers)
    broken_bots = sum(1 for r in bot_registers if r["status"] == "broken")

    print(f"\n--- {label} ---")
    print(f"Total pizzas delivered : {units}")
    print(f"Total weight delivered : {weight}")
    print(f"Total distance         : {total_distance:.2f}")
    print(f"Total energy           : {energy:.2f}")
    print(f"Broken bots            : {broken_bots}")










def plot_kpis(es): #I was not able to figure out why i could not open
     #interactuve ecosystem display so i decided to add some graphs to visualise the reults
     #the code still works properly and does whats i inted it to do

    print("plot_kpis is running") #make sure it runs 
    bots = list(es.registry(kind_class="Bot").values())

    names = [b["name"] for b in bots]
    units = [b["units_delivered"] for b in bots]
    distance_vals = [b["distance"] for b in bots]
    energy_vals = [b["energy"] for b in bots]

    plt.figure()
    plt.bar(names, units)
    plt.title("Pizas Delivred per Bot")
    plt.xlabel(" Bot")
    plt.ylabel("Units delivers ")
    plt.tight_layout()
    plt.savefig("pizzas_per_bot.png")

    plt.figure()
    plt.bar(names, distance_vals)
    plt.title("Distance Travelled per Bot")
    plt.xlabel("Bot ")
    plt.ylabel("Distance ")
    plt.tight_layout()
    plt.savefig("distance_per_bot.png")

    plt.figure()
    plt.bar(names, energy_vals)
    plt.title("Eneregy used per Bot")
    plt.xlabel(" Bot")
    plt.ylabel("Energgy ")
    plt.tight_layout()
    plt.savefig("energy_per_bot.png ")

    print("Saved plots as pizzas_per_bot.png, distance_per_bot.png, energy_per_bot.png")


if __name__ == "__main__":
    es = optimised_version()
    kpis(es, "Optimised Run")
    plot_kpis(es)

