import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkcalendar import Calendar
from datetime import datetime




from modules.output_operator import OutputOperator
from modules.file_operator import FileOperator

from modules.event import Event

from modules.gui_utility import get_today
from modules.gui_utility import make_string_printable
from modules.gui_utility import return_event_title

from modules.colors import Colors
# Logging
import logging
import modules.setup_logger

logger = logging.getLogger("GUI")

import configparser
config = configparser.ConfigParser()
config.read("config/config.ini")

class Manager:
    def __init__(self, root, container):
        """
        Ez a class köti össze az összes gui objektumot, és a datacontainer, hogy tudjanak
        kommunikálni egymással, valamint azért, hogy kommunikálás egyhelyen legyen.
        :param root: az alap
        :param container: datacontainer hivatkozás
        """
        self.gui = root  # itt még ez nem a megfelelől, mivel összevannak kötve, az elején még nem létezik a gui (main.py), később lesz átírva
        self.container = container
        self.chosen = "ALL"
        self.root = root

    def update_list_date(self, date):
        """
        Frissíti a listázás elemeit a megadott dátumra vonatkozóan, az
        adatokat a datacontainerből nyeri ki
        :param date: datetime objektum
        :return:
        """
        events = self.container.get_specific_date_data(date)
        logger.debug(events)
        self.gui.list_frame.update_items(events)

    def update_list_all_date(self):
        """
        Kiíratja az összes dátumot növekvő sorrendben, 3. feladat listázás
        :return:
        """
        self.gui.list_frame.update_items(show_all=True)

    def delete_old_dates(self):
        """
        Kitörli azokat a dátumokat, amelyek az aktuális dátumnál régebbiek
        :return:
        """
        dates = self.container.get_all_data()

        # Megszámolja mennyi elemet töröltünk ki
        counter = 0

        for date in dates:
            if date < get_today():
                self.gui.side_frame.cal.calevent_remove(date=date)
                counter += 1

        logger.debug(f"{counter} elem törölve lett a listából")

    def change_chosen_frame(self, frame):
        """
        Átváltja a kezelőfelületet egy másik framere, a többit, ami nek kell eltünteti
        :param frame: egy specifikus frame, amire váltunk
        :return:
        """

        self.chosen = frame
        self.gui.side_frame.reset_labels()
        if frame != "ADD":
            self.side_frame_add_deactivate()
        else:
            self.side_frame_add_activate()

    def side_frame_add_activate(self):
        logger.debug("side frame adding pane ACTIVATED")
        self.gui.side_frame.activate_add_frames()

    def side_frame_add_deactivate(self):
        logger.debug("side frame adding pane DEACTIVATED")
        self.gui.side_frame.deactivate_add_frames()


class TopFrame():
    def __init__(self, parent, manager):
        """
        Ez a panel foglalja magában a felső gombokat, amik segítségével kitudjuk választani,
        hogy mit is akarunk tenni: hozzáadás,listázás,keresés,...
        :param parent:
        :param manager:
        """
        self.parent = parent
        self.manager = manager

        self.frame = tk.Frame(parent, width=900, height=30, bg=Colors.CREAM, relief=tk.SOLID,borderwidth=2)
        self.frame.place(x=0, y=0)

        self.init_buttons()

        self.buttons = [self.Add, self.Today, self.Search, self.All, self.Delete]
        self.buttons_dic = {"ADD": self.Add,
                            "TODAY": self.Today,
                            "SEARCH": self.Search,
                            "ALL": self.All,
                            "DELETE": self.Delete, }

    def init_buttons(self):
        """
        Egy egységes függvényben létrehozza a gombokat
        :return:
        """
        self.button_width = 120
        self.button_height = 30
        self.Today = tk.Button(self.frame, relief=tk.RAISED, text='Mai nap', command=lambda: self.change_func("TODAY"))
        self.Today.place(x=0, y=0, height=self.button_height, width=self.button_width)

        self.Add = tk.Button(self.frame, relief=tk.RAISED, text='Felvitel', command=lambda: self.change_func("ADD"))
        self.Add.place(x=self.button_width, y=0, height=self.button_height, width=self.button_width)

        self.Search = tk.Button(self.frame, relief=tk.RAISED, text='Keresés',
                                command=lambda: self.change_func("SEARCH"))
        self.Search.place(x=2 * self.button_width, y=0, height=self.button_height, width=self.button_width)

        self.All = tk.Button(self.frame, relief=tk.RAISED, text='Listázás', command=lambda: self.change_func("ALL"))
        self.All.place(x=3 * self.button_width, y=0, height=self.button_height, width=self.button_width)

        self.Delete = tk.Button(self.frame, relief=tk.RAISED, text='Törlés', command=lambda: self.change_func("DELETE"))
        self.Delete.place(x=4 * self.button_width, y=0, height=self.button_height, width=self.button_width)

        logging.info("A felső gombok létrejöttek")

    def change_func(self, mode):
        """
        a gombok különböző funkciói közti váltást biztosítja,
        :param mode:
        :return:
        """

        self.reset_buttons()
        self.buttons_dic[mode].configure(relief=tk.FLAT)

        self.manager.change_chosen_frame(mode)

        if mode == "TODAY":
            self.manager.update_list_date(get_today())
            self.manager.gui.side_frame.cal.selection_set(get_today())

        if mode == "ALL":
            self.manager.update_list_all_date()
            return

        if mode == "DELETE":
            answer = askyesno("Törlés", " Biztos szeretné törölni a régi eseményeket?")
            print("ANSWER",answer)
            if answer:
                FileOperator.delete_old_events(config["DATA"]["path"])
                self.manager.container.delete_old_events()
                self.manager.gui.list_frame.update_items(show_all=True)

    def reset_buttons(self):
        """
        Minden gombot alap állapotba tesz
        :return:
        """
        for button in self.buttons:
            button.configure(relief=tk.RAISED)

    def close_frame(self):
        self.frame.destroy()


class SideFrame():
    def __init__(self, parent, manager):
        """
        Ez a panel foglalja magába a naptárat, valamint a hozzáadáshoz
        szükséges input helyeket
        :param parent:
        :param manager:
        """
        self.SIDE_FRAME_WIDTH = 300
        self.SIDE_FRAME_HEIGHT = 520
        self.parent = parent
        self.manager = manager

        self.frame = tk.Frame(parent, width=self.SIDE_FRAME_WIDTH, height=self.SIDE_FRAME_HEIGHT, bg=Colors.CREAM,
                              borderwidth=3, relief="solid")
        self.frame.place(x=10, y=40)

        self.init_calendar()
        self.init_timeframe()
        self.init_search_frame()
        self.init_button()
        self.init_labels()

        #self.activate_add_frames()

    def init_calendar(self):
        today = get_today()
        self.cal = Calendar(self.frame, selectmode='day',
                            year=today.year, month=today.month,
                            day=today.day,background=Colors.BORDER_BROWN,
                            headersforeground=Colors.CALENDAR_WHITE,headersbackground = Colors.CALENDAR_BORDER_GREEN,
                            normalbackground = Colors.CALENDAR_LIGHT_GREEN,weekendbackground = Colors.CALENDAR_MID_GREEN,
                            bordercolor = "black",othermonthbackground=Colors.CALENDAR_OTHERMONTH,othermonthwebackground=Colors.CALENDAR_OTHERMONTHWEEKEND,
                            othermonthforeground = "black",othermonthweforeground = 'black',weekendforeground="black")

        self.cal.tag_config("Event", background=Colors.CALENDAR_RED, foreground='yellow')

        self.cal.bind("<<CalendarSelected>>", self.get_calendar_update)

        all_date = self.manager.container.get_all_data()

        # Azokat a napokat, amelyeken van valamilyen esemény bepirosítsa
        for date in all_date:
            self.cal.calevent_create(date, "Esemeny", "Event")

        self.cal.place(x=0, y=0, width=295, height=200)

        logger.info("A naptár létrejött")

    def init_timeframe(self):
        label_background = Colors.YELLOW

        self.time_frame = tk.Frame(self.frame, width=self.SIDE_FRAME_WIDTH - 5, height=60, bg=label_background, borderwidth=0,
                                   relief="solid")

        self.start_label = tk.Label(self.time_frame, text="Kezdés",background = label_background)
        self.end_label = tk.Label(self.time_frame, text="Vége",background = label_background)
        self.semicolon1 = tk.Label(self.time_frame, text=":",background = label_background)
        self.semicolon2 = tk.Label(self.time_frame, text=":",background = label_background)
        self.between = tk.Label(self.time_frame, text="--",background = label_background)
        self.start_hour = tk.Spinbox(self.time_frame, from_=0, to=23)
        self.start_minute = tk.Spinbox(self.time_frame, from_=0, to=59)
        self.end_hour = tk.Spinbox(self.time_frame, from_=0, to=23)
        self.end_minute = tk.Spinbox(self.time_frame, from_=0, to=59)

        logger.info("Az kezdő- és végidő megadása létrejött")

    def init_search_frame(self):

        self.search_frame = tk.Frame(self.frame, width=self.SIDE_FRAME_WIDTH - 5, height=150, bg=Colors.YELLOWISH, borderwidth=2,
                                     relief='solid')

        # Korlátozza a szöveges leírás hosszát úgy, hogy ha több mint x karakter, akkor a gomb nem használható


        self.desc_entry = tk.Text(self.search_frame, width=34, height=8)

        logger.info("A kereső panel létrejött")

    def init_button(self):

        self.addbutton = tk.Button(self.frame, text="Add event", command=self.add_event)
        self.desc_entry.bind("<KeyRelease>", self.configure_add_button)

        logger.info("a hozzáadás gomb létrejött")

    def init_labels(self):

        self.invalidTime = tk.Label(self.frame, text="Time input is invalid",fg = Colors.CALENDAR_RED,highlightthickness=4, highlightbackground=Colors.CALENDAR_RED,bg = Colors.BONE)
        self.timeIsInUse = tk.Label(self.frame, text="Time is in use",fg = Colors.CALENDAR_RED,highlightthickness=4, highlightbackground=Colors.CALENDAR_RED,bg = Colors.BONE)
        self.descIsTooLong = tk.Label(self.frame, text="Description text is too long",fg = Colors.CALENDAR_RED,highlightthickness=4, highlightbackground=Colors.CALENDAR_RED,bg = Colors.BONE)
        self.success = tk.Label(self.frame, text="Event was successfully added",fg = Colors.CALENDAR_MID_GREEN,highlightthickness=4, highlightbackground=Colors.CALENDAR_MID_GREEN,bg = Colors.BONE)

        self.labels = [self.invalidTime, self.timeIsInUse, self.descIsTooLong, self.success]

        logger.info("A visszajelzések létrejöttek")

    def activate_add_frames(self):

        self.search_frame.place(x=0, y=260)
        self.time_frame.place(x=0, y=200)
        # side frames timeframe labels
        self.start_label.place(x=20, y=5)
        self.end_label.place(x=170, y=5)
        self.semicolon1.place(x=60, y=25)
        self.semicolon2.place(x=211, y=25)
        self.between.place(x=130, y=25)

        self.start_hour.place(x=20, y=25, width=40, )
        self.start_minute.place(x=70, y=25, width=40)
        self.end_hour.place(x=170, y=25, width=40)
        self.end_minute.place(x=220, y=25, width=40)

        # Desc entry
        self.desc_entry.place(x=6, y=5)

        # Add button
        self.addbutton.place(x=100, y=420, width=80, height=30)

    def deactivate_add_frames(self):
        self.search_frame.place_forget()
        self.time_frame.place_forget()

        self.start_label.place_forget()
        self.end_label.place_forget()
        self.semicolon1.place_forget()
        self.semicolon2.place_forget()
        self.between.place_forget()

        self.start_hour.place_forget()
        self.start_minute.place_forget()
        self.end_hour.place_forget()
        self.end_minute.place_forget()

        # Desc entry
        self.desc_entry.place_forget()

        # Add button
        self.addbutton.place_forget()

    def reset_labels(self):
        """
        Eltünteti az összes visszajelzést
        """
        for label in self.labels:
            label.place_forget()

    def add_event(self):
        """
        Leellenörzi a beírt adatokat és ha helyesek, akkor elmenti őket az adatbázisba
        :return:
        """
        # reset labels
        self.reset_labels()

        # Beolvassa az szöveges leírást
        description = self.desc_entry.get("1.0", 'end-1c')

        # Ha valamelyik időpont nem megfelelő fajtáju(integer), akkor hibátjelezzen ki
        try:
            start_hour = int(self.start_hour.get())
            start_minute = int(self.start_minute.get())
            end_hour = int(self.end_hour.get())
            end_minute = int(self.end_minute.get())
        except ValueError:
            self.invalidTime.place(x=80, y=463)
            logger.error("Nem megfelelő idő van megadva")
            return

        format = "%m/%d/%y"
        date = datetime.strptime(self.cal.get_date(), format)

        # Leellenőrzi a megfelelő feltételeket
        if start_hour < 0 or start_hour > 23 or end_hour > 23 or end_hour < 0:
            self.invalidTime.place(x=80, y=463)
            return

        # Létrehoz egy esemény objektumot
        event = Event(date, datetime(1900, 1, 1, start_hour, start_minute), datetime(1900, 1, 1, end_hour, end_minute),
                      description)

        # A végzés nem előzi-e meg a kezdést
        if not event.check_time():
            self.invalidTime.place(x=80, y=463)
            return
        # Használva van-e
        if not self.manager.container.search_if_start_time_is_free(event):
            self.timeIsInUse.place(x=80, y=463)
            return

        # Mentse el az eseményt
        self.manager.container.insert_binary(event)

        export = OutputOperator.format_event_to_output(event)
        logger.debug(f"A fileba mentés: {export}")
        FileOperator.append_file(config["DATA"]["path"], export)

        # Bepirosítsa azt napot, amelyen az esemény van
        self.cal.calevent_create(date, "Esemeny", "Event")
        self.manager.update_list_date(date)

        self.success.place(x=65, y=463)
        logger.info(f"Sikeresen hozzáadva {date} {event}")

    def configure_add_button(self, event):
        """
        A szöveges leírás hossza alapján működik vagy nem működik a gomb
        :param event:
        :return:
        """
        content = event.widget.get(1.0, "end-1c")

        if len(content) > int(config["DEFAULT"]["description_length"]):
            state = "disabled"
            self.addbutton.configure(relief="sunken")
        else:
            state = "active"
            self.addbutton.configure(relief="raised")

        self.addbutton.configure(state=state)



    def get_calendar_update(self, e):
        """
        Amikor rányomunk egy új dátumra, akkor elmentjük, hogy mire nyomott
        :param e:
        :return:
        """
        format = "%m/%d/%y"
        date = datetime.strptime(self.cal.get_date(), format)
        logging.debug(date)

        if self.manager.chosen == "SEARCH" or self.manager.chosen == "ALL":
            self.manager.gui.top_frame.reset_buttons()
            self.manager.update_list_date(date)

            if self.manager.chosen == 'ALL':
                self.manager.change_chosen_frame("SEARCH")


            return

        if self.manager.chosen == "ADD":
            self.manager.update_list_date(date)
            return date

    def close_frame(self):
        self.frame.destroy()


class ListFrame:
    def __init__(self, parent, manager):
        """
        Ez a panel foglalkozik az események listázásával, vagy az összest, vagy egy specifikus dátumra
        :param parent:
        :param manager:
        """
        self.FRAME_WIDTH = 570
        self.FRAME_HEIGHT = 525

        self.parent = parent
        self.manager = manager

        self.frame = tk.Frame(parent, width=self.FRAME_WIDTH, height=self.FRAME_HEIGHT, borderwidth=3,
                              relief="solid")

        self.frame.place(x=320, y=40)


        self.style = ttk.Style()
        self.init_tree()

    def init_tree(self):

        self.tree = ttk.Treeview(self.frame)


        self.style.configure("Treeview.Heading", rowheight=5)
        self.style.configure("Treeview",  fieldbackground=Colors.CREAM,rowheight=70)


        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.place(x=self.FRAME_WIDTH - 22, y=0, height=self.FRAME_HEIGHT, width=15)

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.tag_configure('oddrow', background=Colors.ROW_DARK_GREEN , font='Helvetica 15 bold')
        self.tree.tag_configure('evenrow', background=Colors.ROW_LIGHT_GREEN)
        self.tree.heading("# 0", text="Események")

        self.update_items(show_all=True)

        self.tree.place(x=0, y=0, width=self.FRAME_WIDTH - 20, height=520)

    def update_items(self, items=None, show_all=False):
        """
        Frissíti a lista megjelenítését a lekérés szerint:
            show_all == True
                Minden adatot kiír a datacontainerből
            show_all == False
                Csak az items-ből írja ki az adatokat
        :param items:
        :param show_all:
        :return:
        """
        self.tree.delete(*self.tree.get_children())

        if items == None:
            items = self.manager.container.get_specific_date_data(get_today())

        logger.info("A kilistázott események dátumai: ")
        if show_all:

            items = self.manager.container.get_all_data()

            for d in sorted(items.keys()):  # gets the events in a sorted manner

                for event in self.manager.container.get_specific_date_data(d):
                    text = d.strftime("%d-%m-%Y") + "   " + return_event_title(event)

                    logger.info(f"DATE: {text}")

                    self.tree.insert('', 'end', text, tag="T", text=text, tags=('oddrow',))
                    self.tree.insert(text, 'end', f"CH-{text}", text=make_string_printable(event.description),
                                     tags=('evenrow',))
                    self.tree.item(text, open=True)
        else:
            for event in items:
                self.tree.insert('', 'end', return_event_title(event), tag="T", text=return_event_title(event),
                                 tags=('oddrow',))
                self.tree.insert(return_event_title(event), 'end', f"CH-{return_event_title(event)}",
                                 text=make_string_printable(event.description), tags=('evenrow',))
                self.tree.item(return_event_title(event), open=True)

                logger.info(f"DATE: {event.date}")

class MainApplication(tk.Frame):
    def __init__(self, parent, manager, container, *args, **kwargs):
        """
        Az össszes panelt összefogja
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.manager = manager
        self.container = container

        background = tk.Frame(parent,bg = Colors.BROWN,width= 1000, height = 1000)
        background.place(x=0,y=0)
        self.top_frame = TopFrame(parent, manager)
        self.side_frame = SideFrame(parent, manager)
        self.list_frame = ListFrame(parent, manager)


