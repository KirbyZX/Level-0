import pygame
import math as maths
                    #attacks              speed hp  graphic     
enemies={"rifleman":[[["bullet", 6.3, 1]], 2.1, 24, "rifleman", ]}
                     #atk type,speed,cooldown

#Hey Lucas, k is for knowledge - you can change that if you want to.
#Also, please make a bullets variable (a list of all bullet positions and velocities).
#enemies will also need an attacks list. So that we can have different types.
#Do enemy.attacks() or something. Make each attack a list of type and other attributes (e.g: bullet speed)
#They also each need a facing variable. I can provide a function for the angle of their facing direction.
#They need a lot of individual attributes, like hp, and possibly courage if you can be bothered.

def ai(enemy, player, k):
    """ Basic A.I. for enemies """
    ep=[enemy.rect.x, enemy.rect.y]
    pp=[player.rect.x, player.rect.y]
    op=200
    att=enemies[enemy.type()]#attributes
    
    if (ep[0]**2-pp[0]**2)+(ep[1]**2-pp[1]**2)>op**2:
        enemy.go_left()
    elif (ep[0]**2-pp[0]**2)+(ep[1]**2-pp[1]**2)<dp**2:
        enemy.go_right()
    else:
        enemy.stop()
    
    for atk in att[0]:
        if "bullet" in atk and time.time()%atk[2]+enemy.cooldown():
            ua=maths.atan((midpos[1]-pop[1])//(midpos[0]-pop[0]))
            addpx =atk[1]*maths.cos(us)
            addpy=atk[1]*maths.sin(ua)
            bullets+=[[enemy.rect.x, enemy.rect.y, addpx, addpy]]


    enemy.rect.x+=att[1]
    platform_hit_list = pygame.sprite.spritecollide(enemy, enemy.level.platform_list, False)
    enemy.rect.x -= att[1]
    if len(platform_hit_list) > 0:
        enemy.jump()

    enemy.rect.x -= att[1]
    platform_hit_list = pygame.sprite.spritecollide(enemy, enemy.level.platform_list, False)
    enemy.rect.x += att[1]#wat
    if len(platform_hit_list) > 0:
        enemy.jump()
