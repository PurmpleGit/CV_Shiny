import cv2
from executors.run_executor import RunExecutor
from executors.search_executor import SearchExecutor
from executors.spam_executor import SpamExecutor
from executors.wait_executor import WaitExecutor
from executors.throw_executor import ThrowExecutor
from executors.bag_pouch_executor import BagPouchExecutor
from executors.open_bag_executor import OpenBagExecutor
from executors.ball_executor import BallExecutor
from state import State
from conditions.condition import Condition
from conditions.confidence import Confidence


POKEMON_SCREENSHOT_X_START = 75
POKEMON_SCREENSHOT_X_WIDTH = 150
POKEMON_SCREENSHOT_Y_START = 360
POKEMON_SCREENSHOT_Y_WIDTH = 150
ENCOUNTER_FILE = './encounter_count.txt'
SHINY_FILE = './shiny_encounter_count.txt'

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
def main() -> None:
    background_image = cv2.imread('./images/Debug_Bg.png', cv2.IMREAD_UNCHANGED)
    last_shiny = cv2.imread('./last_shiny.png')
    encounter_count = int(open(ENCOUNTER_FILE).read())
    shiny_encounter_count = int(open(SHINY_FILE).read())

    find_wild_pokemon = State(SearchExecutor(), 'Finding Wild Pokemon')
    wait_for_battle_start = State(SpamExecutor(), 'Waiting For Battle to Start')
    run = State(RunExecutor(), 'Running From Battle')
    shiny_found = State(SpamExecutor(), 'Shiny Found')
    open_bag = State(OpenBagExecutor(), 'Opening Bag')
    select_ball_pouch = State(BagPouchExecutor(), 'Selecting Ball Pouch')
    select_ball = State(BallExecutor(), 'Selecting Ball')
    spam_balls = State(ThrowExecutor(), 'Throwing Balls')
    shiny_caught = State(SpamExecutor(), 'Shiny Caught')


    find_wild_pokemon.add_transition(Condition('./images/480p/Encounter_Found.png'), wait_for_battle_start)
    wait_for_battle_start.add_transition(Condition('./images/480p/Shiny_Star.png', Confidence.HIGHER), shiny_found)
    wait_for_battle_start.add_transition(Condition('./images/480p/Fight_Box.png'), run)
    run.add_transition(Condition('./images/480p/May_Left.png'), find_wild_pokemon)
    run.add_transition(Condition('./images/480p/May_Right.png'), find_wild_pokemon)
    run.add_transition(Condition('./images/480p/May_Front.png'), find_wild_pokemon)
    run.add_transition(Condition('./images/480p/May_Back.png'), find_wild_pokemon)

    shiny_found.add_transition(Condition('./images/480p/Fight_Box.png'), open_bag)
    open_bag.add_transition(Condition('./images/480p/Bag_Open.png'), select_ball_pouch)
    select_ball_pouch.add_transition(Condition('./images/480p/Bag_Ball_Slot.png', Confidence.VERY_HIGH), select_ball)
    select_ball.add_transition(Condition('./images/480p/Ball_Selected.png', Confidence.VERY_HIGH), spam_balls)
    spam_balls.add_transition(Condition('./images/480p/Caught.png'), shiny_caught)

    shiny_caught.add_transition(Condition('./images/480p/May_Left.png'), find_wild_pokemon)
    shiny_caught.add_transition(Condition('./images/480p/May_Right.png'), find_wild_pokemon)
    shiny_caught.add_transition(Condition('./images/480p/May_Front.png'), find_wild_pokemon)
    shiny_caught.add_transition(Condition('./images/480p/May_Back.png'), find_wild_pokemon)

    current_state:State = find_wild_pokemon

    while(True):
        screen_grab = camera.read()[1]
        
        next_state = current_state.process(screen_grab)
        if(next_state != current_state):
            if(next_state == wait_for_battle_start):
                encounter_count = encounter_count + 1
                open(ENCOUNTER_FILE, "w").write(str(encounter_count))
            if(next_state == shiny_found):
                last_shiny = screen_grab[POKEMON_SCREENSHOT_X_START:POKEMON_SCREENSHOT_X_START + POKEMON_SCREENSHOT_X_WIDTH,POKEMON_SCREENSHOT_Y_START:POKEMON_SCREENSHOT_Y_START + POKEMON_SCREENSHOT_Y_WIDTH].copy()
                shiny_encounter_count = encounter_count
                cv2.imwrite("./last_shiny.png", last_shiny)
                open(SHINY_FILE, "w").write(str(shiny_encounter_count))
            print(f'Transitioning from "{current_state.name}" to "{next_state.name}" on encounter "{encounter_count}".')

        ai_State_screen = cv2.putText(background_image.copy(), f'AI State: {current_state.name}', [10,20], cv2.FONT_HERSHEY_PLAIN, 1.6, [255,255,255], lineType = cv2.LINE_AA)
        cv2.putText(ai_State_screen, f'Encounters: {encounter_count}', [10,50], cv2.FONT_HERSHEY_PLAIN, 1.6, [255,255,255], lineType = cv2.LINE_AA)
        cv2.putText(ai_State_screen, f'Last Shiny: {shiny_encounter_count}', [10,80], cv2.FONT_HERSHEY_PLAIN, 1.6, [255,255,255], lineType = cv2.LINE_AA)
        cv2.addWeighted(ai_State_screen[50:50+POKEMON_SCREENSHOT_X_WIDTH,400:400+POKEMON_SCREENSHOT_Y_WIDTH],1,last_shiny,1,0,ai_State_screen[50:50+POKEMON_SCREENSHOT_X_WIDTH,400:400+POKEMON_SCREENSHOT_Y_WIDTH])
        cv2.imshow('AI State', ai_State_screen)
        
        current_state = next_state
        key = cv2.pollKey()
        if(key == ord('q')):
            break

import cProfile
cProfile.run('main()', sort='tottime')