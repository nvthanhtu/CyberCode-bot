from asyncio.windows_events import NULL
from cv2 import threshold
import cv2 as cv
import numpy as np
import utility
import time
from PIL import ImageGrab

area1 = (600,100,1400,1200)
area2 = (400,100,1100,1200)
printscreen = NULL
threshold=0.9
max_tried_img = 5
max_tried_main_loop =3
nb_enemies_killed = 0
nb_loot_droped = 0
start_time = 0
level_mob = 4

def main():
    global max_tried_main_loop
    global nb_enemies_killed
    global nb_loot_droped
    global start_time 
    global level_mob
    level_mob_img_1 = cv.imread('Image/Level_'+str(level_mob)+'.png', cv.IMREAD_UNCHANGED)
    level_mob_img_2 = cv.imread('Image/Level_'+str(level_mob-1)+'.png', cv.IMREAD_UNCHANGED)
    nearby_enemy_img = cv.imread('Image/Nearby_Enemy.png', cv.IMREAD_UNCHANGED)
    primary_weapon_img = cv.imread('Image/Primary_Weapon.PNG', cv.IMREAD_UNCHANGED)
    take_all_img = cv.imread('Image/Take_all.PNG', cv.IMREAD_UNCHANGED)
    
    #area
    area = area1
    
    #load_wait_time
    load_wait_time_mob = 0.5
    load_wait_time_primary_weap = 1.5
    interval_between_shot = 0.75
    load_wait_time_loot = 0.75
    load_wait_time_after_loot = 1.5
    failed = 0
    
    start_time= time.time()
    while True:
        enemy_killed = False
        if failed > max_tried_main_loop:
            return
        
        print("Total time run: {}".format(int(time.time()-start_time)))
        print("Killed %s mob"% nb_enemies_killed)
        print("Looted %s times"% nb_loot_droped)
        if nb_enemies_killed > 0:
            print("Average time to kill mob: {}".format(int((time.time()-start_time)/nb_enemies_killed)))
            print("Loot %: {:.2f}".format(float(nb_loot_droped/nb_enemies_killed)))
        try: 
            printscreen =  np.array(ImageGrab.grab(bbox=area))
            #click on nearby enemy
            print ("Looking for nearby enemy...")
            clicked_nearby = click_on_template(nearby_enemy_img, printscreen,area)
            
            if not clicked_nearby:
                print ("Can't find Neaby_enemy btn...")
            
            #loading
            time.sleep(load_wait_time_mob)
            
            #choose a target by level (do as least 2 levels)
            print ("Choosing enemy's level...")
            printscreen =  np.array(ImageGrab.grab(bbox=area))
            clicked_mob_1 = click_on_template(level_mob_img_1, printscreen,area, True)
            
            if not clicked_mob_1:
                print("Failed to find mob_1, looking for mob_2...")
                clicked_mob_2 = click_on_template(level_mob_img_2, printscreen,area, True)
                
            #if we cant find any mob => exit    
            if not clicked_mob_1 and not clicked_mob_2:
                print("Failed to find mob...")
            
            #loading
            time.sleep(load_wait_time_primary_weap)
            
            #click on the primary weap until there is no more primary weapon
            print ("Looking for primary weapon...")
            printscreen =  np.array(ImageGrab.grab(bbox=area))    
            clicked_primary_weap = click_on_template(primary_weapon_img, printscreen,area)
            max_shot = 30
            shot = 1
            if not clicked_primary_weap:
                print("Can't find primary weap...")
            
            else:
                while clicked_primary_weap and shot < max_shot:
                    printscreen =  np.array(ImageGrab.grab(bbox=area))    
                    clicked_primary_weap = click_on_template(primary_weapon_img, printscreen,area)
                    shot += 1
                    print("Shooting...")
                    time.sleep(interval_between_shot)
                    
                print("Enemy died...")
                nb_enemies_killed += 1
                enemy_killed = True
            
            #loading
            time.sleep(load_wait_time_loot)
            
            # check for takeall image (to get loot)
            print("Looting...")
            are_there_loot = click_on_template(take_all_img, printscreen,area)
            if are_there_loot:
                nb_loot_droped += 1
                print("Looted...")
            
            if not enemy_killed:
                failed +=1
                time.sleep(5)
            
            if enemy_killed and failed < 3:
                failed = 0
            #loading
            time.sleep(load_wait_time_after_loot)
        except KeyboardInterrupt:
            break
    
        
def click_on_template(template, screenshot, area, colorScale = False):
    
    if not colorScale:
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    else:
        template = cv.cvtColor(template, cv.COLOR_BGR2RGB)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
    tried = 0
    while True:
        image_found = False
        if tried < max_tried_img: 
            try: 
                tried += 1
                result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)
                image_found = True
            except cv.error as e:
                print(e)
                
            if image_found:
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
                if max_val >= threshold:
                    template_w = template.shape[1]
                    template_h = template.shape[0]
                    
                    #take into account offset when screaning
                    click_position_x = int(max_loc[0] + template_w/2 + area[0])
                    click_position_y = int(max_loc[1] + template_h/2 + area[1])
                    
                    utility.click(click_position_x, click_position_y)
                    return image_found
            else:
                time.sleep(1)    
            
        else:
            return image_found

if __name__ == "__main__":
    main()
