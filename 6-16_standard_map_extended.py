#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.

from math import sin, pi
from SetParameter import SetParameter
from array import array
import matplotlib.pylab as plt
import mayavi.mlab as mlab
import numpy as np

# --- init ---
counter = 0
colors = ['blue', 'green', 'red', 'purple', 'black']
ntransient = 100
nplot = 1000
nmax = ntransient + nplot
max_p = 0
min_p = 0
k0 = 0
dk = 0.001

# --- prepare figure and axes ---
fig = plt.figure()


def static():
    global counter
    assignment()

    color = colors[counter]
    counter += 1
    if counter >= len(colors):
        counter = counter - len(colors)

    ary_k = np.arange(k0, kmax + dk, dk)
    k = 0.1
    caluculate(theta, ang_mom, k)
    plot_static(color)


def assignment():
    """ Assign the values to variables and plot the map."""
    global theta, ang_mom, kmax
    theta = float(window.entry[0].get())
    ang_mom = float(window.entry[1].get())
    kmax = float(window.entry[2].get())


def caluculate(q, p, k):
    """ Show an standard map."""
    global max_p, min_p, ary_q, ary_p
    # --- Caluculating ---
    ary_q = array('d')
    ary_p = array('d')
    ary_q.append(q)
    ary_p.append(p)

    for i in range(nmax + 1):
        _q = ary_q[i] + ary_p[i]
        # 0 <= theta <= 2*pi
        while _q > 2 * pi:
            _q = _q - 2 * pi
        while _q < 0.:
            _q = _q + 2 * pi
        ary_q.append(_q)
        ary_p.append(ary_p[i] + k * sin(ary_q[i] + ary_p[i]))


def plot_static(color):
    global max_p, min_p, ary_q, ary_p
    # --- Set labels and ticks. ---
#    ax.set_xlabel(r'$k$', fontsize=16)
#    ax.set_ylabel(r'$\theta$', fontsize=16)
#    ax.set_zlabel(r'$p_{\theta}$', fontsize=16)
#    plt.title('Standard map')
#    unit   = 0.5
#    q_tick = np.arange(0, 2.0+unit, unit)
#    q_label = [r"$0$",r"$\frac{1}{2}\pi$",r"$\pi$",r"$\frac{3}{2}\pi$",r"$2\pi$"]
#    ax.set_ylim(0, 2*pi)
#    ax.set_yticks(q_tick*pi)
#    ax.set_yticklabels(q_label, fontsize=18)
#    ax.set_xlim(0, kmax)
#    if max(ary_p[ntransient:]) > max_p:
#        max_p = max(ary_p[ntransient:])
#    if min(ary_p[ntransient:]) < min_p:
#        min_p = min(ary_p[ntransient:])
#    margin =  (max_p-min_p)*0.05
#    ax.set_zlim(min_p-margin, max_p+margin)

    # --- Plot the standard map. ---
    mlab.points3d([0.1, ] * (nmax - ntransient + 1),
                  ary_q[ntransient:], ary_p[ntransient:])

    plt.show()

if __name__ == '__main__':

    window = SetParameter()
    default_params = [{'theta': 1.5}, {'p': 0.2}, {'kmax': 0.1}]
    commands = [{'OK': static}]
    window.show_setting_window(default_params, commands)
