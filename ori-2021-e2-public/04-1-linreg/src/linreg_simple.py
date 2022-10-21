import random
import matplotlib.pyplot as plt


def linear_regression(x, y):#lista x,i y
    slope = 0.0  # nagib linije
    intercept = 0.0  # tacka preseka na y-osi
    # TODO 1: implementirati linearnu regresiju
    #yi and xi
    n = len(x)
    x_avg = sum(x)/float(n)
    y_avg = sum(y)/float(n)

    #k
    upper_sum = 0.0
    lower_sum = 0.0

    for xi,yi in zip(x,y):
        upper_sum += (xi - x_avg)*(yi - y_avg)
        lower_sum += (xi - x_avg)**2
    slope = upper_sum/lower_sum
    #n
    intercept_sum = 0.0
    for xi, yi in zip(x, y):
       intercept_sum +=yi - slope * xi

    intercept = intercept_sum / n

    return slope, intercept


def predict(x, slope, intercept):
    # TODO 2: implementirati racunanje y na osnovu x i parametara linije

    return slope*x + intercept


def create_line(x, slope, intercept):
    y = [predict(xx, slope, intercept) for xx in x] #y = f(x)
    return y


if __name__ == '__main__':
    x = range(50)  # celobrojni interval [0,50]
    random.seed(1337)  # da rezultati mogu da se reprodukuju
    y = [(i + random.randint(-5, 5)) for i in x]  # y = x (+- nasumicni sum)

    slope, intercept = linear_regression(x, y)

    line_y = create_line(x, slope, intercept)

    plt.plot(x, y, '.')
    plt.plot(x, line_y, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(slope, intercept))
    plt.show()
