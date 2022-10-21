import random
from numpy.ma import copy
from math import *
import numpy as np
from copy import deepcopy


class Cluster(object):

    def __init__(self, center):  # centar je radnom , u njega smijestamo podatke
        self.center = center
        self.data = []  # podaci koji pripadaju ovom klasteru

    def cluster_distance(self, x, y):
        d = sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
        return d

    def recalculate_center(self):
        # TODO 1: implementirati racunanje centra klastera
        # centar klastera se racuna kao prosecna vrednost svih podataka u klasteru

        old_center = deepcopy(self.center)

        new_center = [0 for i in range(len(self.center))]  # nula na svim koordinatama

        for data_point in self.data:
            for i in range(len(data_point)):
                new_center[i] += data_point[i]

        n = len(self.data)
        if n != 0:
            self.center = [x / n for x in new_center]
        x = self.cluster_distance(old_center, self.center)
        print("Pomjeraj : \t" + str(x))
        return x


class KMeans(object):

    def __init__(self, n_clusters, max_iter):
        """
        :param n_clusters: broj grupa (klastera)
        :param max_iter: maksimalan broj iteracija algoritma
        :return: None
        """
        self.data = None
        self.n_clusters = n_clusters  # 2
        self.max_iter = max_iter  # 100
        self.clusters = []

    def fit(self, data):
        self.data = data  # lista N-dimenzionalnih podataka
        # TODO 4: normalizovati podatke pre primene k-means
        dimension = len(self.data[0])
        min_data = np.array([float(inf) for i in range(dimension)])
        max_data = np.array([float(-inf) for i in range(dimension)])

        for i in range(len(min_data)):
            for value in self.data:
                if value[i] < min_data[i]:
                    min_data[i] = value[i]
                if value[i] > max_data[i]:
                    max_data[i] = value[i]

        print("Dimenzije min " + str(min_data))
        print("Dimenzije max " + str(max_data))
        print("Normalizacija podataka : ")

        for value in self.data:
            for i in range(len(min_data)):

                if type(value) == tuple:  # u ball_circle ‘tuple’ object does not support item assignment”
                    transformed = list(value)
                    transformed[i] = (value[i] - min_data[i]) / (max_data[i] - min_data[i])
                    value = tuple(transformed)
                else:
                    value[i] = (value[i] - min_data[i]) / (max_data[i] - min_data[i])
            #  print("\t"+str(value[i]))

        # TODO 1: implementirati K-means algoritam za klasterizaciju podataka
        # kada algoritam zavrsi, u self.clusters treba da bude "n_clusters" klastera (tipa Cluster)
        # random centri za svaki cluster
        # dimension = len(self.data[0])
        # print("Dimenzija : " + str(dimension))

        # TODO MY 1: ovo moze da se promijeni tako da ne biramo random nego na drugi nacin

        for i in range(self.n_clusters):
            #  new_cluster_point = [random.random() for i in range(dimension)]

            indices = random.randrange(np.array(self.data).shape[0])
            pt = self.data[np.array(indices)]
            self.clusters.append(Cluster(pt))

        #  self.clusters.append(Cluster(new_cluster_point))
        i = 0

        endValue = np.array([0 for i in range(self.n_clusters)])

        while i <= self.max_iter:
            print(endValue)

            if np.all((endValue == 1)):
                print("Loop ended.")
                break

            for cluster in self.clusters:
                cluster.data = []

            for element in self.data:
                cluster_index = self.predict(element)
                self.clusters[cluster_index].data.append(element)

            for cluster in self.clusters:

                if cluster.recalculate_center() == 0:
                    index = self.clusters.index(cluster)
                    if endValue[index] != 1:
                        print("Izbacujem cluster na index - u " + str(index))

                        endValue[index] = 1

                else:
                    pass
            print("Iteracija: " + str(i))
            i += 1

        # TODO (domaci): prosiriti K-means da stane ako se u iteraciji centri klastera nisu pomerili

    def predict(self, element):
        # TODO 1: implementirati odredjivanje kom klasteru odredjeni podatak pripada
        # podatak pripada onom klasteru cijem je centru najblizi (po euklidskoj udaljenosti)
        # kao rezultat vratiti indeks klastera kojem pripada
        min_distance = None
        cluster_index = None
        for index in range(len(self.clusters)):
            distance = self.euclidian_distance(element, self.clusters[index].center)
            if min_distance is None or distance < min_distance:
                min_distance = distance
                cluster_index = index

        return cluster_index

    def sum_squared_error(self):
        # TODO 3: implementirati izracunavanje sume kvadratne greske
        # SSE (sum of squared error), elbow metoda
        # unutar svakog klastera sumirati kvadrate rastojanja izmedju podataka i centra klastera
        sse = 0.0
        for cluster in self.clusters:
            for data in cluster.data:
                sse += (self.euclidian_distance(cluster.center, data)) ** 2

        return sse

    # x - element, y - center
    def euclidian_distance(self, x, y):

        distance = sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

        return distance.__round__(2)
