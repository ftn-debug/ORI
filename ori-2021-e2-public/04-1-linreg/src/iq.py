from __future__ import print_function
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# TODO 4: implementirati primenu visestruke linearne regresije
# nad podacima iz datoteke "data/iq.tsv".
# Korisiti implementaciju linearne regresije u alatu scikit-learn
from linreg_simple import create_line

if __name__ == '__main__':
    data_x = []
    data_y = []
    data_first = []
    data_second = []
    data_third = []

    with open('./../data/iq.tsv', 'r') as file:
        for line in file:
            try:
                row = [float(num) for num in line.split()]  #inicijalno splituje po tabu i po razmaku
                data_y.append(row[0])
                data_x.append(row[1:])
                data_first.append(row[1])
                data_second.append(row[2])
                data_third.append(row[3])
            except:
                pass

    lr = LinearRegression().fit(data_x,data_y) #data_x moze biti visedimenzionalan ,fit - obucavanje
    #mozemo i predictovati
    # lr.predict(np.array([[3,5]])); zavidi od dimenzija x
    print(lr.predict(np.array([[34.00, 65.00, 110]])))

    slope = lr.coef_
    print(slope)
    intercept = lr.intercept_
    print(intercept)

    # Vidimo da masa mozga najvise utice
    # visina ima negativan trend
    # tezina ne utice mnogo
    # Valjda treba napraviti grafik za ovo
    s1= slope[0]
    s2= slope[1]
    s3= slope[2]

    line_y1 = create_line(data_first, s1, intercept)
    line_y2 = create_line(data_second, s2, intercept)
    line_y3 = create_line(data_third, s3, intercept)

    plt.plot(data_first, data_y, '.')
    plt.plot(data_first, line_y1, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(s1, intercept))
   # plt.show()

    plt.figure()
    plt.plot(data_second, data_y, '.')
    plt.plot(data_second, line_y2, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(s2, intercept))
   # plt.show()

    plt.figure()
    plt.plot(data_third, data_y, '.')
    plt.plot(data_third, line_y3, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(s3, intercept))
    plt.show()


def create_line(x, slope, intercept):
    y = [predict(xx, slope, intercept) for xx in x]  # y = f(x)
    return y

def predict(x, slope, intercept):
    # TODO 2: implementirati racunanje y na osnovu x i parametara linije

    return slope*x + intercept