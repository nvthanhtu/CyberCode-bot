from asyncio.windows_events import NULL
from turtle import color
from cv2 import threshold
import cv2 as cv
import numpy as np
import win32api,win32con
import time
from PIL import ImageGrab

area = (600,100,1400,1200)
printscreen = NULL
threshold=0.9
max_tried = 3
nb_enemies_killed = 0
nb_loot_droped = 0
start_time = 0

def main():
    
    level_mob_img_1 = cv.imread('Image/Level_24.png', cv.IMREAD_UNCHANGED)
    level_mob_img_2 = cv.imread('Image/Level_23.png', cv.IMREAD_UNCHANGED)
    nearby_enemy_img = cv.imread('Image/Nearby_Enemy.png', cv.IMREAD_UNCHANGED)
    primary_weapon_img = cv.imread('Image/Primary_Weapon.PNG', cv.IMREAD_UNCHANGED)
    take_all_img = cv.imread('Image/Take_all.PNG', cv.IMREAD_UNCHANGED)
    
    #load_wait_time
    load_wait_time_mob = 0.5
    load_wait_time_primary_weap = 1.5
    interval_between_shot = 0.75
    load_wait_time_loot = 0.75
    load_wait_time_after_loot = 1
    
    global nb_enemies_killed
    global nb_loot_droped
    global start_time 
    
    start_time= time.time()
    while True:
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
            clicked_nearby = click_on_template(nearby_enemy_img, printscreen)
            
            if not clicked_nearby:
                print ("Can't find Neaby_enemy btn...")
                return
            
            #loading
            time.sleep(load_wait_time_mob)
            
            #choose a target by level (do as least 2 levels)
            print ("Choosing enemy's level...")
            printscreen =  np.array(ImageGrab.grab(bbox=area))
            clicked_mob_1 = click_on_template(level_mob_img_1, printscreen)
            
            if not clicked_mob_1:
                print("Failed to find mob_1, looking for mob_2...")
                clicked_mob_2 = click_on_template(level_mob_img_2, printscreen)
                
            #if we cant find any mob => exit    
            if not clicked_mob_1 and not clicked_mob_2:
                print("Failed to find mob...")
                return
            
            #loading
            time.sleep(load_wait_time_primary_weap)
            
            #click on the primary weap until there is no more primary weapon
            print ("Looking for primary weapon...")
            printscreen =  np.array(ImageGrab.grab(bbox=area))    
            clicked_primary_weap = click_on_template(primary_weapon_img, printscreen)
            max_shot = 15
            shot = 1
            if not clicked_primary_weap:
                print("Can't find primary weap...")
                return
            
            while clicked_primary_weap and shot < max_shot:
                printscreen =  np.array(ImageGrab.grab(bbox=area))    
                clicked_primary_weap = click_on_template(primary_weapon_img, printscreen)
                shot += 1
                print("Shooting...")
                time.sleep(interval_between_shot)
                
            print("Enemy died...")
            nb_enemies_killed += 1
            
            #loading
            time.sleep(load_wait_time_loot)
            
            # check for takeall image (to get loot)
            print("Looting...")
            are_there_loot = click_on_template(take_all_img, printscreen)
            if are_there_loot:
                nb_loot_droped += 1
                print("Looted...")
                
            #loading
            time.sleep(load_wait_time_after_loot)
        except KeyboardInterrupt:
            break
    
        
def click_on_template(template, screenshot):
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    tried = 0
    while True:
        image_found = False
        if tried < max_tried: 
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
                    
                    click(click_position_x, click_position_y)
                    return image_found
        else:
            return image_found
    
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)    


if __name__ == "__main__":
    main()