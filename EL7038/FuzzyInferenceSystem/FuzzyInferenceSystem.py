"""
This program implements a fuzzy interface, including computation of membership,
fuzzy operations and plotting of membership sets.

It's necessary to count with numpy and matplotlib libraries.
"""

__author__ = 'Juan Pablo Futalef'
__email__ = "jpfutalef@gmail.com"

import numpy as np
import matplotlib.pyplot as plt


def trap_membership_degree(a, set_points):
    """
    Calculates membership degree of input according to trapezoidal function
    characterized by a size 4 array.
    :param a: number to evaluate in fuzzy set
    :param set_points: size 4 array with trapezoid definitions
    :return: membership degree of a
    Note: If points representing start and end of same support are equal, the membership degree is assumed to be one.
    For example [2,2,3,4], as both first and second values are 2, the membership degree of 2 is 1.
    """
    if len(set_points) > 4 or len(set_points) < 4:
        """Argument given is not a size 4 array."""
        raise NameError('nonTrapezoidalSet')
    else:
        if a < set_points[0] or a > set_points[3]:
            """Outside trapezoid case"""
            return 0
        elif a < set_points[1]:
            """Left support case"""
            d = set_points[1] - set_points[0]
            if d == 0:
                """Both values are equal"""
                return 1
            else:
                return (a - set_points[0]) / d
        elif a > set_points[2]:
            """Right support case"""
            d = set_points[2] - set_points[3]
            if d == 0:
                """both values are equal"""
                return 1
            else:
                return (a - set_points[3]) / d
        else:
            """Value is in core"""
            return 1


def trap_fuzzy_fun(u, set_points):
    """
    Allows to calculate membership values of input respect to trapezoidal function
    :param u: input vector
    :param set_points: size 4 array vector with trapezoid definitions
    :return: array vector with membership degrees vales for every input in u
    """
    return np.array([trap_membership_degree(i, set_points) for i in u])


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


# Define trapezoidal functions by size 4 arrays
A = np.array([-1.0, -1.0, -.9, -.2])
B = np.array([-.6, -.5, .0, .1])
C = np.array([-.3, .0, .2, .3])
D = np.array([.1, .2, .3, .8])
E = np.array([.4, .6, 1, 1])

# Define X axis values
x = np.linspace(-1, 1, 41)

# Create array containing sets definitions (size 4 arrays) an iterate trough them
sets = [A, B, C, D, E]
S = []
for i in sets:
    """
    Appends every fuzzy membership set in S. It gives S[0] as A set, S[1] as B set, and so on.
    Also, add graphs to plot object.
    """
    s = trap_fuzzy_fun(x, i)
    S.append(s)
    plt.plot(x, s)

# Plot membership functions and save result to file
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.title('Membership functions')
plt.legend(['A', 'B', 'C', 'D'])
plt.savefig('membershipFuns.png')
#plt.show()
plt.close()


# Operacion 1
op1 = union(S[3], intersection(S[0], S[2]))
plt.subplot(2, 2, 1)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op1)
plt.title('Operación 1')


# Operacion 2
op2 = intersection(compliment(intersection(S[0], S[1])), intersection(S[3], S[4]))
plt.subplot(2, 2, 2)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op2)
plt.title('Operación 2')

# Operacion 3
op3 = intersection(compliment(S[3]), union(S[1], S[0]))
plt.subplot(2, 2, 3)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op3)
plt.title('Operación 3')

# Operacion 4
op4 = compliment(union(S[0], S[1]))
plt.subplot(2, 2, 4)
plt.xlabel('Input value')
plt.ylabel('Membership degree')
plt.plot(x, op4)
plt.title('Operación 4')

# Adjust plot layout for good fit and save to file
plt.tight_layout()
plt.savefig('operationResults.png')
#plt.show()
plt.close()

# Export to csv file sets and operations
setsCSV = np.transpose(np.array([x, S[0], S[1], S[2], S[3], S[4]]))
operationsCSV = np.transpose(np.array([x, op1, op2, op3, op4]))
np.savetxt('valuesSets.csv', setsCSV, delimiter=" ", fmt='%1.3f')
np.savetxt("valuesOperations.csv", operationsCSV, delimiter=" ", fmt='%1.3f')
