"""
This program allows treatment of fuzzy sets, including computation of membership,
fuzzy operations and plotting of membership sets.
"""

__author__ = 'Juan Pablo Futalef'
__email__ = "jpfutalef@gmail.com"

import numpy as np
import matplotlib.pyplot as plt


def trap_fuzzy_interface(a, set_points):
    """
    Calculates membership degree of input according to trapezoidal set characterized by an array
    :param a: number to evaluate in fuzzy set
    :param set_points: size 4 array with trapezoid definitions
    :return: membership degree of a
    """
    if len(set_points) > 4 or len(set_points) < 4:
        raise NameError('nonTrapezoidalSet')
    else:
        if a < set_points[0] or a > set_points[3]:
            return 0
        elif a < set_points[1]:
            d = set_points[1] - set_points[0]
            if d == 0:
                return 1
            else:
                return (a - set_points[0]) / d
        elif a > set_points[2]:
            d = set_points[2] - set_points[3]
            if d == 0:
                return 1
            else:
                return (a - set_points[3]) / d
        else:
            return 1


def trap_fuzzy_fun(u, set_points):
    """
    Allows to calculate membership function according to input array and trapezoidal size 4 array
    :param u: input vector
    :param set_points: size 4 array vector with trapezoid definitions
    :return: array vector with membership degrees vales for every input in u
    """
    return np.array([trap_fuzzy_interface(i, set_points) for i in u])


def intersection(a, b):
    """
    Intersects a and b sets using T norm as minimum. a and b should be same length arrays.
    :param a: array containing first set
    :param b: array containing second set
    :return: intersection of both a and b sets.
    """
    return np.array([min(x) for x in list(zip(a, b))])


def union(a, b):
    """
    Intersects a and b sets using T norm as maximum. a and b should be same length arrays.
    :param a: array containing first set
    :param b: array containing second set
    :return: union of both a and b sets.
    """
    return np.array([max(x) for x in list(zip(a, b))])


def compliment(a):
    """
    Creates compliment set of a trough 1-a[i] operation of each element.
    :param a: target set
    :return: compliment of set
    """
    return np.array([1 - x for x in a])


# Define trapezoidal sets by core and support
A = np.array([-1.0, -1.0, -.9, -.2])
B = np.array([-.6, -.5, .0, .1])
C = np.array([-.3, .0, .2, .3])
D = np.array([.1, .2, .3, .8])
E = np.array([.4, .6, 1, 1])

# Create sets
x = np.linspace(-1, 1, 200)
sets = [A, B, C, D, E]
S = []
for i in sets:
    """
    Appends every fuzzy membership set in S. It gives S[0] as A set, S[1] as B set, and so on.
    """
    s = trap_fuzzy_fun(x, i)
    plt.plot(x, s)
    S.append(s)

plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.show()

# 1
op1 = union(S[3], intersection(S[0], S[2]))
plt.subplot(2, 2, 1)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op1)


# 2
op2 = intersection(compliment(intersection(S[0], S[1])), intersection(S[3], S[4]))
plt.subplot(2, 2, 2)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op2)

# 3
op3 = intersection(compliment(S[3]), union(S[1], S[0]))
plt.subplot(2, 2, 3)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op3)

# 4
op4 = compliment(union(S[0], S[1]))
plt.subplot(2, 2, 4)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op4)

plt.show()
