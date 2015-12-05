import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from flask import send_file
import cStringIO


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