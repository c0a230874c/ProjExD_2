import os
import pygame as pg
import random as ran
import sys
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5), 
         pg.K_DOWN:(0, +5), 
         pg.K_RIGHT:(+5, 0), 
         pg.K_LEFT:(-5, 0),
         }  # 練習１
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとん,バクダンのrect
    戻り値:真理値タプル(横判定, 縦判定)
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def accs(ac, vx, vy) -> list[int,int,int]:
    """
    バクダンの速度を変更する関数
    引数:加速度, 上下速度, 左右速度
    戻り値:加速度, 上下速度, 左右速度
    """
    ac = abs(ac)
    if ac < 11:
        ac += 1
        if vx < 0:
            ac *= -1
        vx += ac
        ac = abs(ac)
        if vy < 0:
            ac *= -1
        vy += ac
    print(ac, vx, vy)
    return ac, vx, vy


def large(r):
    if r < 12:
        r += 1
    bb_img = pg.Surface((20 * r, 20 * r)) #空のSurface
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
    bb_rct = bb_img.get_rect()
    bb_rct.center = ran.randint(0, WIDTH), ran.randint(0, HEIGHT)
    print(r)
    return r


def game_over(screen: pg.Surface):
    """
    ゲームオーバー画面を表示させる
    引数:pg.Surface
    """
    screen_gameover = pg.Surface((WIDTH, HEIGHT))
    screen_gameover_rct = (0, 0, WIDTH, HEIGHT)
    pg.draw.rect(screen_gameover, (0, 0, 0), screen_gameover_rct)
    screen_gameover.set_alpha(160)

    kk_img_2 = pg.image.load("fig/8.png")
    fonto = pg.font.Font(None, 120)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    fonto.set_bold(True)
    
    screen.blit(screen_gameover, [0, 0])
    txt_rct = [WIDTH/3 - 30, HEIGHT/2 - 20]
    screen.blit(txt, txt_rct)
    screen.blit(kk_img_2, [txt_rct[0] - 50, txt_rct[1]])
    screen.blit(kk_img_2, [txt_rct[0] + 460, txt_rct[1]])
    pg.display.update()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurface
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = ran.randint(0, WIDTH), ran.randint(0, HEIGHT)


    clock = pg.time.Clock()
    tmr = 0
    r = 0
    ac = 0
    vx = +3
    vy = +3 #バクダンの移動量
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #当たったら終了
            game_over(screen)
            time.sleep(3)
            return
        
        if tmr % 500 == 1:
            print("hi")
            ac, vx, vy = accs(ac, vx, vy)
            r = large(r)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] #横、縦
        
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  #横座標
                sum_mv[1] += tpl[1]  #縦座標
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #画面外に行かないようにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #バクダンバウンド
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
       
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
