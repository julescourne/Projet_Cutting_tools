from tkinter import Toplevel, Label


class MenuAide:
    """Classe qui gère la vue de la fenêtre Aide"""

    def __init__(self, parent):
        """Constructeur de la fenêtre Aide

        Parameters
        ----------
        parent : frame
            La frame parent

        """
        top = self.top = Toplevel(parent)
        self.label_aide = Label(top, text="Pour effectuer la racine carrée de la variable X, il faut taper sqrt(X) \n \n "
                                     "Pour effectuer le carré de la variable Y, il faut taper Y**2 \n \n "
                                     "Pour effectuer la multiplication de la variable Z par un nombre il faut taper nombre*Z ou Z*nombre \n \n "
                                     "Pour effectuer le logarithme en base n de la variable X, il faut taper log(X, n) \n \n "
                                     "Pour effectuer la puissance n de la variable X, il faut taper pow(X, n) \n \n "
                                     "Pour effectuer l'exponentielle de la variable X, il faut taper exp(X)", font=("Arial", 12))
        self.label_aide.pack()
