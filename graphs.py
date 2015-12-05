import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from flask import send_file
import cStringIO

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np

def serve_graph(sensor1=None, sensor2=None, sensor3=None):
    ram_file = cStringIO.StringIO()
    # plt.plot([1, 2, 3, 4])
    plt.ylabel('Jytky/s')
    plt.xlabel('Herra Soini')
    if sensor1:
        plt.plot(sensor1)
    if sensor2:
        plt.plot(sensor2)
    if sensor3:
        plt.plot(sensor3)

    plt.savefig(ram_file, format='png')
    ram_file.seek(0)
    return send_file(ram_file, mimetype='image/png')


def serve_3d_graph(sensor1=None, sensor2=None, sensor3=None):
    ram_file = cStringIO.StringIO()
    region = np.s_[5:50, 5:50]
    #x, y, z = x[region], y[region], z[region]
    """
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    # rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(sensor1, sensor2, sensor3, rstride=1, cstride=1,  # facecolors=rgb,
                           linewidth=1, antialiased=False, shade=False)

    """
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(sensor1, sensor2, sensor3, rstride=1, cstride=1, cmap=cm.YlGnBu_r)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = np.linspace(0, 1, 100)
    y = np.sin(x * 2 * np.pi) / 2 + 0.5
    #ax.plot(x, y, zs=0, zdir='z', label='zs=0, zdir=z')

    """
    colors = ('r', 'g', 'b', 'k')
    for c in colors:
        # x = np.random.sample(20)
        x = sensor1
        # y = np.random.sample(20)
        y = sensor3
        ax.scatter(x, y, 0, zdir='y', c=c)

    """
    #ax.legend()

    ax.plot_wireframe(sensor1, sensor2, sensor3)
    ax.set_xlim3d(0, 10)
    ax.set_ylim3d(0, 10)
    ax.set_zlim3d(0, 10)

    print x
    print y

    plt.savefig(ram_file, format='png')
    ram_file.seek(0)
    return send_file(ram_file, mimetype='image/png')