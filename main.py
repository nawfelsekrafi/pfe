import data
import tours
# import map
import ui


if __name__ == "__main__":

    organ_name = 'intellect'

    bus_location = [33.851847795093995, 10.093554315264997]

    students = data.get_students_data()
    data.download_students_avatars(students)
    data.download_organization_logo(organ_name)
    small_tours = tours.from_big_list_to_small_tours(students, data.get_today())
    print(small_tours)
    ui.interface(bus_location, small_tours)



"""
try:
except :
    print("verify your internet connection.")


select (key ) : value go_8 or go_10 or back_12 or back_16

    sorted_tour = tours.convert_to_nearest_neighbor(bus_location,small_tours[value])
    map.map_representation(bus_location,sorted_tour)
    recognition.run(sorted_tour)
"""