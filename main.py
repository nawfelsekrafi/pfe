import data
import tours
import ui


if __name__ == "__main__":

    organ_name = 'intellect'

    bus_location = [33.851847795093995, 10.093554315264997]

    students = data.get_students_data()
    data.download_students_avatars(students)
    data.download_organization_logo(organ_name)
    small_tours = tours.from_big_list_to_small_tours(students, data.get_today())
    ui.interface(bus_location, small_tours)