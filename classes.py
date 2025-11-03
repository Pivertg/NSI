import pyxel
import time
import constante
import random

# Bal
    
class Bal:
    def __init__(self, jeu):
        self.x=constante.LARGEUR_FENETRE/2 #position de la bal en x et y
        self.y=constante.HAUTEUR_FENETRE/2 #position de la bal en y
        self.couleur= constante.BAL_COULEUR #couleur de la bal
        self.taille= constante.BAL_TAILLE #taille de la bal
        self.rayon= constante.BAL_RAYON #rayon de la bal
        self.dx= random.choice([-1, 1]) #vitesse en x
        self.dy= random.uniform(-2, 2)#vitesse en y
        self.temps_ecoule =0
        self.start_time = time.time() # le timer
        self.jeu = jeu # on récopéré les variable de la classe jeu pour le score
        self.jeu.score_gauche = 0
        self.jeu.score_droite = 0


    def deplacer(self): # tout les déplasement de la bal

        self.timeur()

        self.x += self.dx
        self.y += self.dy

        if self.y <= 3:
            self.dy = -self.dy

        if self.y >= constante.HAUTEUR_FENETRE - 3:
            self.dy = -self.dy

        if self.x <= 0:
            self.jeu.score_gauche += 1 # +1 pour la coter gauche
            self.temps_ecoule =0
            self.reset()

        if self.x >= constante.LARGEUR_FENETRE:
            self.jeu.score_droite += 1 # + 1 pour le coter droit
            self.temps_ecoule =0 # on remette le timer a 0 
            self.reset()

        # ======= COLLISION AVEC LA RAQUETTE GAUCHE =======
        if (self.x - self.rayon <= self.jeu.raquette_gauche.x + self.jeu.raquette_gauche.largeur and
            self.y >= self.jeu.raquette_gauche.y and
            self.y <= self.jeu.raquette_gauche.y + self.jeu.raquette_gauche.hauteur):

            # Position relative du point d'impact sur la raquette (de -1 à 1)
            position_relative = ((self.y - self.jeu.raquette_gauche.y) / self.jeu.raquette_gauche.hauteur) * 2 - 1

            # Ajuste la direction horizontale
            self.dx = abs(self.dx)

            # Ajuste la direction verticale en fonction de l’impact
            self.dy = position_relative * 3  # plus le nombre est grand, plus la balle part en diagonale

            # Replace la balle juste à côté de la raquette pour éviter qu’elle reste bloquée dedans
            self.x = self.jeu.raquette_gauche.x + self.jeu.raquette_gauche.largeur + self.rayon


        # ======= COLLISION AVEC LA RAQUETTE DROITE =======
        if (self.x + self.rayon >= self.jeu.raquette_droite.x and
            self.y >= self.jeu.raquette_droite.y and
            self.y <= self.jeu.raquette_droite.y + self.jeu.raquette_droite.hauteur):

            # Position relative du point d'impact sur la raquette (de -1 à 1)
            position_relative = ((self.y - self.jeu.raquette_droite.y) / self.jeu.raquette_droite.hauteur) * 2 - 1

            # Ajuste la direction horizontale
            self.dx = -abs(self.dx)

            # Ajuste la direction verticale
            self.dy = position_relative * 3

            # Replace la balle juste à côté de la raquette
            self.x = self.jeu.raquette_droite.x - self.rayon


    def timeur(self):
        # Temps écoulé depuis le dernier reset
        self.temps_ecoule = time.time() - self.start_time

        # Si 5 secondes se sont écoulées → accélérer
        if self.temps_ecoule >= 1:
            if self.dx > 0:
                self.dx += 0.1
            else:
                self.dx -= 0.1
            self.start_time = time.time()  # Réinitialiser le timer
        
    def reset(self): # on rememt la bal au centre
        self.x=constante.LARGEUR_FENETRE/2
        self.y=constante.HAUTEUR_FENETRE/2
        self.dx = random.choice([-1, 1])
        self.dy = random.uniform(-2, 2)
        

    def afficher(self): #affichage de la bal
        pyxel.circ(round(self.x), round(self.y), self.rayon, 7) # c'est la dissine de la bal avec comme argument x , y , rayon , couleur
    
#Raquette

class Raquette:
    def __init__(self, x, app): #initialisatoin des variable
        self.x = x # position horizontale de la raquette
        self.y = constante.RAQUETTE_Y_INIT  # position verticale initiale
        self.hauteur = constante.RAQUETTE_HAUTEUR  # hauteur de la raquette
        self.largeur = constante.RAQUETTE_LARGEUR   # largeur de la raquette
        self.app = app
        #self.skin = None # skin de la raquette peut étre a coder

    def haut(self): # déplacement vers le haut
        if self.y <= constante.RAQUETTE_Y_MIN:
            self.y = constante.RAQUETTE_Y_MIN
        else:
            self.y -= constante.RAQUETTE_VITESSE
    def bas(self): # déplacement vers le bas

        if self.y >= constante.RAQUETTE_Y_MAX + constante.RAQUETTE_HAUTEUR:
            self.y = constante.RAQUETTE_Y_MAX + constante.RAQUETTE_HAUTEUR
        else:
            self.y += constante.RAQUETTE_VITESSE

    def afficher(self): # affichage de des raquette
        pyxel.rect(self.x , self.y, self.largeur, self.hauteur, 7) # affichage de la raquette gauche

class Menu_pause:
    def __init__(self, app):
        self.app = app # on récupére l'etat de l'application pour faire le changement d'etat

    def afficher(self):
        # self.app.jeu.afficher() # pour afficher le jeu en arrier plans
        pyxel.text(5, 5, "PAUSE", 7)
        pyxel.text(5, 5, "Si vous voulez recommencer la partie faite supp\n sinon faite", 7)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.app.etat = "jeu"
        elif pyxel.btnp(pyxel.KEY_ESCAPE):
            self.app.etat = "menu"
        elif pyxel.btnp(pyxel.KEY_DELETE):
            self.app.etat = "Paramétre_jeu"
        
class Parametre_jeu:  # paramètres du jeu
    def __init__(self, app):
        self.app = app
        self.points_max = 5  # nombre de points pour gagner (par défaut)
        self.jeu = Jeu(self)
        self.bal = Bal(self)

    def afficher(self): # tout l'affichage
        pyxel.text(5, 5, "Paramètres du jeu", 7)
        pyxel.text(5, 20, "Appuyez sur ESPACE pour lancer la partie", 7)
        pyxel.text(5, 35, "Appuyez sur ESC pour revenir au menu", 7)
        pyxel.text(5, 55, f"Points pour gagner : {self.points_max}", 7)
        pyxel.text(5, 70, "(Flèches gauche/droite pour modifier)", 6)

    def update(self):
        self.bal.reset()
        self.app.jeu.score_gauche = 0
        self.app.jeu.score_droite = 0
        self.app.jeu.raquette_gauche.y = constante.RAQUETTE_Y_INIT
        self.app.jeu.raquette_droite.y = constante.RAQUETTE_Y_INIT
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.app.etat = "menu"
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.app.jeu.points_max = self.points_max  # on envoie la valeur au jeu
            self.app.etat = "jeu"
        elif pyxel.btnp(pyxel.KEY_LEFT):
            if self.points_max > 1:
                self.points_max -= 1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.points_max += 1

class Fin_de_jeu:
    def __init__(self, app):
        self.parametre_jeu = Parametre_jeu (self)
        self.app = app

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
           self.app.etat = "menu"

    def afficher (self):
        if self.app.jeu.score_gauche <= self.app.jeu.score_droite :
            pyxel.text(constante.HAUTEUR_FENETRE/4, constante.LARGEUR_FENETRE/4, "le coter gauche a gagnier", 7)
        else:
            pyxel.text(constante.HAUTEUR_FENETRE/4, constante.LARGEUR_FENETRE/4, "le coter droit a gagnier", 7)

class Jeu: # la logique du jeu fotionnement des point exct
    def __init__(self, app):
        self.score_gauche = 0 # si on quitte sa remette a 0
        self.score_droite = 0
        self.bal = Bal(self)
        self.raquette_gauche = Raquette(constante.RAQUETTE_ESPACE_X, app)
        self.raquette_droite = Raquette(constante.LARGEUR_FENETRE - constante.RAQUETTE_ESPACE_X - constante.RAQUETTE_LARGEUR, app)
        self.app = app
        self.conteur = 0
    def afficher(self):
        self.bal.afficher()
        self.raquette_gauche.afficher()
        self.raquette_droite.afficher()
        pyxel.text(50, 10, str(self.score_gauche), 7) #affichage du score gauche
        pyxel.rect(constante.LARGEUR_FENETRE/2, 0, 1, constante.HAUTEUR_FENETRE, 7)
        pyxel.text(150, 10, str(self.score_droite), 7) #affichage du score droite

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
           self.app.etat = "menu_pause"

        if pyxel.btn(pyxel.KEY_UP): # on fait bouver le requette en haut et si sa position est egale a 10 elle reste a 10 mais voir si c'est les boenn 
            self.raquette_droite.haut()
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.raquette_droite.bas()
        if pyxel.btn(pyxel.KEY_Z):
            self.raquette_gauche.haut()
        elif pyxel.btn(pyxel.KEY_S):
            self.raquette_gauche.bas()
        
        self.bal.deplacer()
        
         # Vérifier si un joueur a gagné
        if self.score_gauche >= self.app.paramétre_jeu.points_max or self.score_droite >= self.app.paramétre_jeu.points_max:
            self.app.etat = "Fin_de_jeu"  # retour au menu (tu peux créer un écran "victoire" si tu veux)



        # #code de triche ne fontieonne pas
        # if pyxel.btnp(pyxel.KEY_UP):
        #     self.conteur +=1
        #     self.timer = time.time()
        #     if self.timer >= 1.5:
        #         self.conteur=0
        # elif self.conteur ==3:
        #     self.raquette_droite.hauteur +=2
        # if pyxel.btnp(pyxel.KEY_Z):
        #     self.conteur +=1
        #     self.timer = time.time()
        #     if self.timer >= 1.5:
        #         self.conteur=0
        # elif self.conteur ==3:
        #     self.raquette_gauche.hauteur +=2

# pas d'idée pour les parmétre
# class Parametres:   
#     def __init__(self, app):
#         self.difficulte = "normal"  # niveau de difficulté (facile, normal, difficile)
#         self.couleur_fond = 0  # couleur de fond de l’écran
#         self.couleur_raquette = 7  # couleur des raquettes
#         self.couleur_balle = 7  # couleur de la balle
#         self.app = app
#         self.touche1 = "z"
#         self.touche2 = "s"
#         self.touche3 = "↑"
#         self.touche4 = "↓"
#     def affichage(self):
#         pass
        
#     def update(self):
#         if pyxel.btnp(pyxel.KEY_ESCAPE): # pour le changemet d'etat
#             self.app.etat = "menu"

# Menu
class Menu:
    def __init__(self, app):
        self.texte =  None # texte du menu
        self.couleur = constante.MENU_COULEUR  # couleur du texte
        self.x = None  # position x du texte 
        self.y = None  # position y du texte
        self.selection = 0  # option sélectionnée dans le menu
        self.app = app

    def afficher(self):
        self.texte = "> Appuyez sur ESPACE pour jouer <" #texte afficher
        self.couleur = 7
        self.x = constante.LARGEUR_FENETRE/4- 10  # on prand les constant de l'affichage et le mette ou on veux ducoup si on change la talle de le fenaitre se chenge autmatiquement
        self.y = constante.HAUTEUR_FENETRE/2
        pyxel.text(self.x, self.y, self.texte, self.couleur) #module pyxel qui premet d'afficher du texte a l'écran "pyxel.text(x,y,texte,couleur)"
        # self.x = constante.HAUTEUR_FENETRE-10 # cette fois c'est pour l'affiage des paramétre
        # self.y = constante.LARGEUR_FENETRE-constante.LARGEUR_FENETRE+10
        # self.texte= "P pour paramére" 
        # pyxel.text(self.x, self.y, self.texte, self.couleur)

    def update(self): # affiachege de dépare 
        if pyxel.btnp(pyxel.KEY_SPACE): # gestion des etat si ont appuit sur espace ducopu sa va passer dans les paramétre du jeu
            self.app.etat = "Paramétre_jeu"
        elif pyxel.btnp(pyxel.KEY_ESCAPE): # encore un chagement d'etat mais pour quitter cette fois
            self.app.etat = "quitter"
        # elif pyxel.btnp(pyxel.KEY_P): # si p est appuiller >> paramétre
        #     self.app.etat = "parametres"

        