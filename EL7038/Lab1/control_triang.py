#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 14:56:44 2018

@author: gabriel orellana
"""

import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz
import matplotlib.pyplot as plt


error = ctrl.Antecedent(np.arange(-1, 1.05, 0.05), 'error')
delta = ctrl.Antecedent(np.arange(-1, 1.05, 0.05), 'delta')
temp = ctrl.Consequent(np.arange(-200, 201, 1), 'temp')

names = ['nb', 'ns', 'ze', 'ps', 'pb']

error['nb'] = fuzz.trapmf(error.universe, [-1, -1, -0.6, -0.4])
error['ns'] = fuzz.trapmf(error.universe, [-0.8, -0.7, -0.3, 0])
error['ze'] = fuzz.trapmf(error.universe, [-0.3, -0.1, 0.1, 0.3])
error['ps'] = fuzz.trapmf(error.universe, [0.0, 0.3, 0.6, 0.8])
error['pb'] = fuzz.trapmf(error.universe, [0.7, 0.9, 1, 1])

delta['nb'] = fuzz.trapmf(delta.universe, [-1, -1, -0.6, -0.4])
delta['ns'] = fuzz.trapmf(delta.universe, [-0.8, -0.7, -0.3, 0])
delta['ze'] = fuzz.trapmf(delta.universe, [-0.3, -0.1, 0.1, 0.3])
delta['ps'] = fuzz.trapmf(delta.universe, [0.0, 0.3, 0.6, 0.8])
delta['pb'] = fuzz.trapmf(delta.universe, [0.7, 0.9, 1, 1])

temp['nb'] = fuzz.trapmf(temp.universe, [-200, -200, -40, -30])
temp['ns'] = fuzz.trapmf(temp.universe, [-50, -20, -15, 0])
temp['ze'] = fuzz.trapmf(temp.universe, [-10, -0, 0, 10])
temp['ps'] = fuzz.trapmf(temp.universe, [-5, 5, 40, 50])
temp['pb'] = fuzz.trapmf(temp.universe, [40, 50, 200, 200])

# Parte 1
temp.view()
plt.show()

error.view()
plt.show()

delta.view()
plt.show()

rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
                              (error['ns'] & delta['nb']) |
                              (error['nb'] & delta['ns'])),
                  consequent=temp['nb'], label='rule nb')

rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
                              (error['nb'] & delta['ps']) |
                              (error['ns'] & delta['ns']) |
                              (error['ns'] & delta['ze']) |
                              (error['ze'] & delta['ns']) |
                              (error['ze'] & delta['nb']) |
                              (error['ps'] & delta['nb'])),
                  consequent=temp['ns'], label='rule ns')

rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
                              (error['ns'] & delta['ps']) |
                              (error['ze'] & delta['ze']) |
                              (error['ps'] & delta['ns']) |
                              (error['pb'] & delta['nb'])),
                  consequent=temp['ze'], label='rule ze')

rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
                              (error['ze'] & delta['pb']) |
                              (error['ze'] & delta['ps']) |
                              (error['ps'] & delta['ps']) |
                              (error['ps'] & delta['ze']) |
                              (error['pb'] & delta['ze']) |
                              (error['pb'] & delta['ns'])),
                  consequent=temp['ps'], label='rule ps')

rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
                              (error['pb'] & delta['pb']) |
                              (error['pb'] & delta['ps'])),
                  consequent=temp['pb'], label='rule pb')


system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])

sim = ctrl.ControlSystemSimulation(system)

po = 140    
pi = 0

tt = np.zeros(100)
tt[0] = pi

for i in range(1,100):
    
    sim.input['error'] = (po-tt[i-1])/200.0
    if i==1:
        sim.input['delta'] = 0
    else:
        sim.input['delta'] = (tt[i-1]-tt[i-2])/200.0

    sim.compute()

    tt[i] = tt[i-1]+int(sim.output['temp'])

#temp.view(sim=sim)
plt.plot(range(len(tt)), tt)
plt.show()


#temp.defuzzify_method









