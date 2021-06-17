import math
from datetime import date


def from_big_list_to_small_tours(students, day):
    today = date.today()
    w = today.isocalendar()[1]


    result = {}
    go_8 = []
    go_10 = []

    back_12 = []
    back_16 = []
    for s in students:
        for j in s["weeks_of_study"]:
            if str(j["n"]) == str(w):
                for i in j["days"]:
                    if i["n"] == day:
                        # remplir les sous-tabs d'aller
                        if '8:00' in i["go"]:
                            go_8.append(s)
                            d = {"go_8": go_8}
                            result.update(d)

                        if '10:00' in i["go"]:
                            go_10.append(s)
                            d = {"go_10": go_10}
                            result.update(d)
                        # remplir les sous-tabs de retour
                        if '12:00' in i["back"]:
                            back_12.append(s)
                            d = {"back_12": back_12}
                            result.update(d)

                        if '16:00' in i["back"]:
                            back_16.append(s)
                            d = {"back_16": back_16}
                            result.update(d)

    return result


def convert_to_nearest_neighbor(bus_location, students):
    tab = {}
    for s in students:
        # distance between tow points : d=√((x_2-x_1)²+(y_2-y_1)²)
        distance = math.sqrt(
            (s["home_location"][0] - bus_location[0]) ** 2 + (s["home_location"][1] - bus_location[1]) ** 2)
        a = [s["name"], s["home_location"], s["phone_number"]]
        tab[distance] = a

    # sorting tab
    tab = sorted(tab.items())
    # formatting returned data and adding index
    final_tab = {}
    index = 1
    for i in tab:
        d = {index: i[1]}
        final_tab.update(d)
        index+=1
    print(final_tab)
    return final_tab


