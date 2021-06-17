from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import count
import tours
import map
import recognition


class ImageLabel(Label):

    def load(self, im):


        if isinstance(im, str):
            im = Image.open(im)

        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
                pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()


    def unload(self):
        self.config(image="")


        self.frames = None


    def next_frame(self):
        if self.frames:
            self.loc += 1


        self.loc %= len(self.frames)
        self.config(image=self.frames[self.loc])
        self.after(self.delay, self.next_frame)

def interface(bus_location,small_tours):
    choice = ''
    finalChoice = ''
    found = False
    sorted_tour = {}

    def sel():
        selection = str(var.get())
        global choice
        choice = selection
    root = Tk()
    root.title("School Bus")
    root.geometry("2000x500")
    root.iconphoto(False, PhotoImage(file='./assets/school-bus.png'))

    lbl = ImageLabel(root)
    lbl.load('./assets/loading.gif')
    lbl.pack()

    user_name = Label(root,
                      text = "Hi, Please select a tour: ").pack()

    var = IntVar()
    R1 = Radiobutton(root, text="tour 1   08:00   ==>", variable=var, value=1,
                     command=sel)
    R1.pack(anchor=W)

    R2 = Radiobutton(root, text="tour 2   10:00   ==>", variable=var, value=2,
                     command=sel)
    R2.pack(anchor=W)

    R3 = Radiobutton(root, text="tour 3   12:00   <==", variable=var, value=3,
                     command=sel)
    R3.pack(anchor=W)

    R4 = Radiobutton(root, text="tour 4   16:00   <==", variable=var, value=4,
                     command=sel)
    R4.pack(anchor=W)

    label = Label(root)
    label.pack()

    def sur():
        global choice
        global finalChoice
        answer = messagebox.askquestion("verify", "Are you sure?")
        if (answer == 'yes'):
             if (choice == '1'):
                finalChoice = 'go_8'
             elif (choice == '2'):
                finalChoice = 'go_10'
             elif (choice == '3'):
                finalChoice = 'back_12'
             elif (choice == '4'):
                finalChoice = 'back_16'

             for i in small_tours:
                 global found
                 if i == finalChoice:
                     global found
                     global sorted_tour
                     found = True
                     sorted_tour = tours.convert_to_nearest_neighbor(bus_location, small_tours[finalChoice])
                     map.map_representation(sorted_tour, bus_location)

                     try:
                        recognition.run(sorted_tour)
                     except :
                         print("Open the camera Please")
                     break
                 found = False
             if found == False:
                 print('We have no student for this Time. Bye !')

        if (answer == 'no'):
            print(answer)

    B = Button(root, text ="Next", command = sur)

    B.pack()

    root.mainloop()

