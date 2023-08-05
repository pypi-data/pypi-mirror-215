"""
Esta es el modulo que incluye la clase
de reproduccion de musica
"""


class Player:
    """
    Esta clase crea un reproductor
    de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio como parametro

        Prameters:
        song (str): Este es un String con el Path de la cancion

        Returns:
        int: devuelve 1 si reprouce con exito, en caso de fracaso devuelve 0
        """
        print("Reproduciendo cancion")

    def stop(self):
        print("Stopping...")
