from __future__ import print_function

from copy import deepcopy

from sklearn.datasets import load_iris
import numpy as np

import matplotlib.pyplot as plt

from src.kmeans import KMeans, inf

if __name__ == '__main__':

    # iris_data = load_iris()
    # print(iris_data)
    # iris_data = iris_data.data[:, 1:3]
    # print(iris_data)
    stroke_data = []
    new_data = []
    with open('./../data/dataset.csv') as file:
        for line in file:
            data = line.split(',')

            try:

                if data[1] == 'Male':
                    p1 = float(0)
                elif data[1] == 'Female':
                    p1 = float(1)
                else:
                    p1 = float(0.5)

                p2 = float(data[2])
                p3 = float(data[3])
                p4 = float(data[8])
                if data[9] == 'N/A':
                    it = 0
                    suma = 0
                    for date in new_data:
                        suma += date[4]
                        it += 1
                    p5 = float(suma / it)
                else:
                    p5 = float(data[9])
                p6 = float(data[11])

                new_data.append([p1, p2, p3, p4, p5])
                stroke_data.append(p6)

            except:
                pass


def normalise_dataset(dataset):
    dimension = len(dataset[0])
    min_data = np.array([float(inf) for i in range(dimension)])
    max_data = np.array([float(-inf) for i in range(dimension)])

    for i in range(len(min_data)):
        for value in dataset:

            if value[i] < min_data[i]:
                min_data[i] = value[i]
            if value[i] > max_data[i]:
                max_data[i] = value[i]

    print("\t Dimenzije min " + str(min_data))
    print("\t Dimenzije max " + str(max_data))
    print("Normalizacija podataka : ")

    for value in dataset:
        for i in range(len(min_data)):

            if type(value) == tuple:  # u ball_circle ‘tuple’ object does not support item assignment”
                transformed = list(value)
                transformed[i] = (value[i] - min_data[i]) / (max_data[i] - min_data[i])
                value = tuple(transformed)
            else:
                value[i] = (value[i] - min_data[i]) / (max_data[i] - min_data[i])
    return dataset


new_data = normalise_dataset(new_data)
new_data_copy = deepcopy(new_data)

print("New data==================================================")
#print(new_data)
print("New data copy ==================================================")
#print(new_data_copy)


# TODO 2: K-means  data setu
kmeans = KMeans(n_clusters=3, max_iter=100)
kmeans.fit(new_data)
print("Stroke data:")
print(stroke_data)
print("--Ende-")

# TODO 3: Kreiram novi dataset koji ima stroke parametar



def find_data(Ddata):
    index_element = new_data_copy.index(Ddata)
    if stroke_data[index_element] == 1:
        return True
    else:
        return False


for idx, cluster in enumerate(kmeans.clusters):
    print("IDX: " + str(idx))
    print("Cluster: " + str(cluster))
    print(len(cluster.data))
   # for data in cluster.data:
    #    print(data)
    print("-------------------------------------ENDE --------------------------------------")

    stroke_patients = 0
    not_stroke_patients = 0

    for data in cluster.data:
        if find_data(data):
            stroke_patients += 1
        else:
            not_stroke_patients += 1

    print("Stroke patients: " + str(stroke_patients))
    print("Not Stroke patients: " + str(not_stroke_patients))
    ratio = stroke_patients.__round__() / not_stroke_patients.__round__()
    ratio2 = 1 - ratio
    percentage = "{:2%}".format(ratio)
    percentage2 = "{:2%}".format(ratio2)
    print("Stroke patients percentage: " + str(percentage))
    print("Non-Stroke patients percentage: " + str(percentage2))

# --- ODREDJIVANJE OPTIMALNOG K --- #


sum_squared_errors = []
for n_clusters in range(2, 10):
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100)
    kmeans.fit(new_data)
    sse = kmeans.sum_squared_error()
    sum_squared_errors.append(sse)

plt.plot(sum_squared_errors)
plt.xlabel('#k of clusters')
plt.ylabel('SSE')
plt.show()
