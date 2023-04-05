import numpy as np

list_effort = [8.15, 9.25, -2.25, 10, 5.56, 98.2]
list_temps = [0.123, 0.1258, 0.1259, 0.129, 1.52, 1.59]


def get_mean(list_effort, list_temps, segment):
    """
    Calcul la moyenne des efforts pour une seconde. Permet d'avoir une courbe lisible en vue du grand
    nombre de données.
    :param list_effort: liste des valeurs des efforts
    :param list_temps: liste des valeurs du temps
    :return: liste moyennes des efforts, liste de chaque secondes
    """
    temps = np.array(list_temps)
    effort = np.array(list_effort)

    if segment == 'second':
        int_temps = temps.astype(int)
        unique_temps, indices = np.unique(int_temps, return_inverse=True)
        effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
    elif segment == 'decisecond':
        int_temps = (temps * 10).astype(int)
        unique_temps, indices = np.unique(int_temps, return_inverse=True)
        unique_temps = unique_temps / 10
        effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
    elif segment == 'centisecond':
        int_temps = (temps * 100).astype(int)
        unique_temps, indices = np.unique(int_temps, return_inverse=True)
        unique_temps = unique_temps / 100
        effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
    elif segment == 'millisecond':
        int_temps = (temps * 1000).astype(int)
        unique_temps, indices = np.unique(int_temps, return_inverse=True)
        unique_temps = unique_temps / 1000
        effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
    return effort_mean.tolist(), unique_temps.tolist()


print(get_mean(list_effort, list_temps, 'millisecond'))
