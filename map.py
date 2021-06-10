import folium
import webbrowser


def map_representation(dic, bus_location):
    # Create map object
    m = folium.Map(location=[33.851847795093995, 10.093554315264997], zoom_start=16)

    # bus location marker
    logoIcon = folium.features.CustomIcon('./assets/school-bus.png', icon_size=(30, 30))
    folium.Marker([bus_location[0], bus_location[1]], tooltip='Station', icon=logoIcon).add_to(m)

    # organization location marker
    organ_location = [33.851874241694915, 10.093395053944665]
    logoIcon_o = folium.features.CustomIcon('./images/organ_logo/intellect.jpg', icon_size=(30, 30))
    folium.Marker([organ_location[0], organ_location[1]], tooltip='Intellect Academy', icon=logoIcon_o).add_to(m)

    # Students locations markers

    for i in dic:
        # data formatting
        # rang
        index = i
        # name
        name = dic[i][0]
        # address
        latitude = dic[i][1][0]
        longitude = dic[i][1][1]
        # phone_number for getting students img
        image_name = str(dic[i][2]) + ".jpg"

        logoIcon = folium.features.CustomIcon('./images/students_avatars/' + image_name, icon_size=(30, 30))
        tooltip = str(index) + " " + name
        folium.Marker([latitude, longitude],
                      tooltip=tooltip,
                      icon=logoIcon).add_to(m)

    # Generate map
    m.save('map.html')

    # Open Map in the browser
    webbrowser.open('file://' + './home/nawfel/PycharmProjects/faceRecognition/map.html')
