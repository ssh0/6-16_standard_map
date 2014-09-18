#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.

from math import sin, pi
from SetParameter import SetParameter
from array import array
import matplotlib.pylab as plt
import numpy as np
import sys

# --- init ---
counter = 0
colors = ['blue', 'green', 'red', 'purple', 'black']
ntransient = 1000
nplot = 10000
nmax = ntransient + nplot
max_p = 0
min_p = 0

# --- prepare figure and axes ---
fig = plt.figure(figsize=(12, 6), dpi=80)
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.14)
plt.subplots_adjust(right=0.68)
ax.grid()


def static():
    global counter
    assignment()

    color = colors[counter]
    counter += 1
    if counter >= len(colors):
        counter = counter - len(colors)

    plot_static(theta, ang_mom, color)


def assignment():
    """ Assign the values to variables and plot the map.
    """
    global theta, ang_mom, k, color
    theta = float(window.entry[0].get())
    ang_mom = float(window.entry[1].get())
    k = float(window.entry[2].get())


def plot_static(q, p, color):
    """ Show an standard map.
    """
    global max_p, min_p
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

    # --- Set labels and ticks. ---
    plt.xlabel(r'$\theta$', fontsize=16)
    plt.ylabel(r'$p_{\theta}$', fontsize=16)
    plt.title('Standard map')
    unit = 0.5
    q_tick = np.arange(0, 2.0 + unit, unit)
    q_label = [
        r"$0$", r"$\frac{1}{2}\pi$", r"$\pi$", r"$\frac{3}{2}\pi$", r"$2\pi$"]
    ax.set_xticks(q_tick * pi)
    ax.set_xticklabels(q_label, fontsize=18)
    if max(ary_p[ntransient:]) > max_p:
        max_p = max(ary_p[ntransient:])
    if min(ary_p[ntransient:]) < min_p:
        min_p = min(ary_p[ntransient:])
    margin = (max_p - min_p) * 0.05
    plt.ylim(min_p - margin, max_p + margin)

    # --- Plot the standard map. ---
    plt.scatter(ary_q[ntransient:], ary_p[ntransient:],
                s=2.0, marker='o', color=color,
                label=r'$\theta_{0}=$' + str(theta) + ' : '
                + r'$p_{0}=$' + str(ang_mom) + ' : '
                + r'$k=$' + repr(k)
                )
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', borderaxespad=0)

    plt.show()

if __name__ == '__main__':

    window = SetParameter()
    default_params = [{'theta': 1.5}, {'p': 0.2}, {'k': 0.1}]
    commands = [{'run': static}, {'quit': sys.exit}]
    window.show_setting_window(default_params, commands)
