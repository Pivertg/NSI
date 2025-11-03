import pyxel
import constante
from classes import Menu, Jeu, Menu_pause, Parametre_jeu, Fin_de_jeu  # on importera les classes

class App:
    def __init__(self):
        pyxel.init(constante.LARGEUR_FENETRE, constante.HAUTEUR_FENETRE, title=constante.TITRE_FENETRE, fps=constante.FPS, quit_key=pyxel.KEY_NONE) # création de la fenêtre       
        # création des objets du jeu
        pyxel.mouse(True)   # pour afficher le curseur
        self.menu = Menu(self) # on récupére touetes les classe pour faire afficher les menu avec l'etat
        # self.parametres = Parametres(self)
        self.jeu = Jeu(self)
        self.menu_pause = Menu_pause(self)
        self.paramétre_jeu = Parametre_jeu(self)
        self.fin_de_jeu = Fin_de_jeu(self)
        # état initial
        self.etat = "menu" # comme sa on spone dans le menu 
        
        # lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self): # ici et en dousou on fait le changemnt d'etat pour faire le bonne affichage et la bonne logique dans chaque fenettre
        if self.etat == "menu":
            self.menu.update()
        elif self.etat == "jeu":
            pyxel.mouse(True) # activer ou déaciter l'apparation du curseur
            self.jeu.update()
        elif self.etat == "menu_pause":
            pyxel.mouse(True)
            self.menu_pause. update()
        # elif self.etat == "parametres":
        #     pyxel.mouse(True)
        #     self.parametres.update()
        elif self.etat == "quitter":
            pyxel.quit()
        elif self.etat == "Paramétre_jeu":
            pyxel.mouse(True)
            self.paramétre_jeu.update()
        elif self.etat == "Fin_de_jeu":
            pyxel.mouse(False)
            self.fin_de_jeu.update()
        # ici, on mettra la logique du jeu (déplacements, collisions, etc.)

    def draw(self):  # ici ducou c'est l'affichage des etat
        # ici, on dessinera les éléments à l’écran
        pyxel.cls(0)
        if self.etat == "menu":
            self.menu.afficher()
        elif self.etat == "jeu":
            self.jeu.afficher()
        elif self.etat == "menu_pause":
            self.menu_pause.afficher()
        # elif self.etat == "parametres":
        #     self.parametres.affichage()
        elif self.etat == "Paramétre_jeu":
            self.paramétre_jeu.afficher()
        elif self.etat == "Fin_de_jeu":
            self.fin_de_jeu.afficher()
if __name__ == "__main__": # on lence le jeux 
    App()
