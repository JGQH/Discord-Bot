from PIL import Image
from player import Player
from discord import File
from io import BytesIO

class Drawer():
    def __init__(self):
        pass

    @staticmethod
    def loadImgs(size:int):
        black_tile = Image.open("resources/black_tile.png", 'r')
        white_tile = Image.open("resources/white_tile.png", 'r')

        board_size = (32 * size, 32 * size)
        board_img = Image.new('RGBA', board_size, (0, 0, 0, 0))

        is_black = True
        for y in range(size):
            for x in range(size):
                box = (32 * x, 32 * y)

                if(is_black):
                    board_img.paste(black_tile, box)
                else:
                    board_img.paste(white_tile, box)
                
                is_black = not is_black
            
            if((size % 2) == 0):
                is_black = not is_black

        Drawer.board_img = board_img
        Drawer.board_size = board_size
        
        player_img = Image.open("resources/player_img.png", 'r')
        Drawer.player_img = player_img

        enemy_img = Image.open("resources/enemy_img.png", 'r')
        Drawer.enemy_img = enemy_img

        pointer_img = Image.open("resources/pointer_img.png", 'r')
        Drawer.pointer_img = pointer_img

        Drawer.hps_imgs = [
            Image.open("resources/1hp_img.png", 'r'),
            Image.open("resources/2hp_img.png", 'r'),
            Image.open("resources/3hp_img.png", 'r')
        ]

    @staticmethod
    def renderBoard(players:dict, player_name:str):
        board = Drawer.board_img.copy()
        for name in players:
            player:Player = players[name]
            box = (32 * player.x, 32 * player.y)

            #Player img
            if (player_name == name):
                board.paste(Drawer.player_img, box, mask=Drawer.player_img)

                #Pointer
                pointer_img = Drawer.pointer_img.rotate(player.rotation - 45)
                board.paste(pointer_img, box, mask=pointer_img)
            else:
                board.paste(Drawer.enemy_img, box, mask=Drawer.enemy_img)

            #Remaining hp
            hp_img = Drawer.hps_imgs[player.hp - 1]
            board.paste(hp_img, box, mask=hp_img)
        
        holder = BytesIO()
        board.save(holder, format='PNG')
        holder.seek(0)
        return File(fp=holder, filename='board.png')