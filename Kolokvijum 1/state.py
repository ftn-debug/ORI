from __future__ import division
import copy
from abc import *


class State(object):
    """
    Apstraktna klasa koja opisuje stanje pretrage.
    """

    @abstractmethod
    def __init__(self, board, start_counter=None, parent=None, position=None, goal_position=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :param position: pozicija stanja
        :param goal_position: pozicija krajnjeg stanja
        :param start_counter : indikator koliko dugo smo u zoni senzora
        :return:
        """
        self.board = board

        self.counter = None
        self.start_counter = None
        self.area = False
        self.blue_boxes = None


        self.parent = parent  # roditeljsko stanje
        if self.parent is None:  # ako nema roditeljsko stanje, onda je ovo inicijalno stanje
            self.goal_position = board.find_position(self.get_agent_goal_code())
            self.position = board.find_position(self.get_agent_code())  # pronadji pocetnu poziciju
            self.blue_boxes = board.find_position_list('b')
            self.sensors = board.find_position_list('y')
            self.counter = 0
            self.start_counter = 0



        else:     # ako ima roditeljsko stanje, samo sacuvaj vrednosti parametara
            self.goal_position = goal_position
            self.position = position
            self.blue_boxes = copy.deepcopy(parent.blue_boxes)
            self.sensors = copy.deepcopy(parent.sensors)
            self.counter = copy.deepcopy(parent.counter)
            self.area = parent.area
            self.start_counter = copy.deepcopy(parent.start_counter)


        self.depth = parent.depth + 1 if parent is not None else 1  # povecaj dubinu/nivo pretrage

    def get_next_states(self):
        next_states = []
        new_positions = self.get_legal_positions()  # dobavi moguce (legalne) sledece pozicije iz trenutne pozicije
        # napravi listu mogucih sledecih stanja na osnovu mogucih sledecih pozicija
        for new_position in new_positions:
            next_state = self.__class__(self.board, self.start_counter, self, new_position, self.goal_position)
            next_states.append(next_state)
        return next_states

    @abstractmethod
    def get_agent_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agenta na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_agent_goal_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agentovog cilja na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_legal_positions(self):
        """
        Apstraktna metoda koja treba da vrati moguce (legalne) sledece pozicije na osnovu trenutne pozicije.
        :return: list
        """
        pass

    @abstractmethod
    def is_final_state(self):
        """
        Apstraktna metoda koja treba da vrati da li je treuntno stanje zapravo zavrsno stanje.
        :return: bool
        """
        pass

    @abstractmethod
    def unique_hash(self):
        """
        Apstraktna metoda koja treba da vrati string koji je JEDINSTVEN za ovo stanje
        (u odnosu na ostala stanja).
        :return: str
        """
        pass

    @abstractmethod
    def get_cost(self):
        """
        Apstraktna metoda koja treba da vrati procenu cene
        (vrednost heuristicke funkcije) za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass

    @abstractmethod
    def get_current_cost(self):
        """
        Apstraktna metoda koja treba da vrati stvarnu trenutnu cenu za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass


class RobotState(State):

    def __init__(self, board, start_counter=None, parent=None, position=None, goal_position=None):
        super(self.__class__, self).__init__(board, start_counter, parent, position, goal_position)
        # posle pozivanja super konstruktora, mogu se dodavati "custom" stvari vezani za stanje

        # TODO 6: prosiriti stanje sa informacijom da li je robot pokupio kutiju
        #self.area = self.in_area()
        self.new_objective()
        #self.in_area()


    def in_area(self):
        for var in self.sensors:
            x_p = self.position[0]
            y_p = self.position[1]
            x_s = var[0]  # 0
            y_s = var[1]  # 0
            d = ((x_p - x_s) ** 2 + (y_p - y_s) ** 2) ** 0.5
            if d <= 3:
               return True # a ako ni jedan nije < 3 onda ostaje area = false i counter se vrati na 0
                # ako je area true ,counter se povecava za jedan
        return False

    def new_objective(self):
        if self.counter <= 1:
            self.goal_position = self.blue_boxes[0]
        else:
            self.goal_position = self.board.find_position('g')

    def get_agent_code(self):
        return 'r'

    def get_agent_goal_code(self):

        return 'g'

    def get_legal_positions(self):
        # d_rows (delta rows), d_cols (delta columns)
        # moguci smerovi kretanja robota (desno, levo, dole, gore)
        d_rows = [0, 0, 1, -1, 1, 1, -1, -1]
        d_cols = [1, -1, 0, 0, -1, 1, 1, -1]

        row, col = self.position  # trenutno pozicija
        new_positions = []

        # This is all about the parent
        # it will change goal for its children
        # it will change counter for its children
        if self.position in self.blue_boxes:
            self.blue_boxes.remove(self.position)
            self.counter += 1
            self.new_objective()

        # This also looks whether parent was in range
        # if it was we will halt for one iteration
        # the children will inherit iterations and will continue if necessary
        self.area = self.in_area()
        if self.area == False:
            self.start_counter = 0      #always override start_counter
        else:
            self.start_counter+=1

        if self.start_counter % 2 == 1:
            new_positions.append((row, col))
        else:
            for d_row, d_col in zip(d_rows, d_cols):  # za sve moguce smerove
                new_row = row + d_row  # nova pozicija po redu
                new_col = col + d_col  # nova pozicija po koloni
                # ako nova pozicija nije van table i ako nije zid ('w'), ubaci u listu legalnih pozicija
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols \
                        and self.board.data[new_row][new_col] != 'w':
                    new_positions.append((new_row, new_col))

        return new_positions

    def is_final_state(self):
            return self.position == self.board.find_position('g') and self.counter == 2


    def unique_hash(self):
        return str(self.position) + str(self.blue_boxes) + str(self.sensors)

    def get_cost(self):
        x_p = self.position[0]
        y_p = self.position[1]
        x_f = self.goal_position[0]
        y_f = self.goal_position[1]

        return ((x_p - x_f) ** 2 + (y_p - y_f) ** 2) ** 0.5

    def get_current_cost(self):
        return self.depth

    def avoid_sensors(self):
        suma = 0
        if self.counter !=2:
            for var in self.sensors:

                x_p = self.position[0]
                y_p = self.position[1]
                x_f = var[0]
                y_f = var[1]
                d = (((x_p - x_f) ** 2 + (y_p - y_f) ** 2) ** 0.5)
                if d != 0.0:
                    suma += 3.0 / d
        else:
            print('Pokupio sam dvaaa'+ str(self.counter))

        return suma
