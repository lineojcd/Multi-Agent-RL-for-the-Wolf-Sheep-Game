from config import *


def get_class_name():
    return 'BasicAstar'


class BasicAstarPlayer():
    """Greedy Kingsheep player. Sheep flee from the wolf or go to the nearest food
    in a straight line, wolves go to sheep in a straight line."""

    def __init__(self):
        self.name = "BasicAstarPlayer"
        self.uzh_shortname = "BasicAstar player"
        self.goal4Sheep = None
        self.goal4Wolf = None
        self.wolfAlertDistance = 2
        self.actionList = []
        self.RHUBARB_extra = 1
        self.foodclossness2sheep = 0
        self.foodfarness2wolf = -1  # -1, -2 ... - minimum available_food
        self.minimumavailable_food = 6

    def getManhDistance(self, y_V_from, x_H_from, y_V_to, x_H_to):
        return abs(x_H_from - x_H_to) + abs(y_V_from - y_V_to)

    # check if wolf can sabotage the food: if the food distance to own sheep is longer than enemy
    # return flag
    def sabotageable(self, sabotage_y_V, sabotage_x_H, ownSheep, enemySheep, field):
        FLAG = True
        ownSheep_pos = self.get_player_position(ownSheep, field)

        if ownSheep == None:
            return FLAG
        enemySheep_pos = self.get_player_position(enemySheep, field)
        dis2OwnSheep = self.getManhDistance(sabotage_y_V, sabotage_x_H, ownSheep_pos[0], ownSheep_pos[1])
        dis2EnemySheep = self.getManhDistance(sabotage_y_V, sabotage_x_H, enemySheep_pos[0], enemySheep_pos[1])
        if dis2OwnSheep < dis2EnemySheep:
            print("this food is more close to own sheep; dont sabotage")
            FLAG = False
        return FLAG

    # input: my wolf figure and position
    # outpur: my wolf figure and position and move towards enemy sheep
    def huntSheep(self, figure, mypos_y, mypos_x, enemySheep_figure, field):
        print("猎捕敌羊： huntSheep")
        new_tar_pos4Wolf = self.get_player_position(enemySheep_figure, field)
        self.actionList = ActionListGenerator(figure, mypos_y, mypos_x, new_tar_pos4Wolf[0], new_tar_pos4Wolf[1], field)
        suggestedAction = self.actionList[0]
        return suggestedAction, figure, (mypos_y,mypos_x)

    def get_player_position(self, figure, field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    # defs for sheep
    def food_present(self, field):
        food_present = False

        for line in field:
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present

    #  this function takes input position and returns what figure on this position
    #  it maybe a grass, rubber, fence, road, wolf, sheep or rtc.
    def getObjbyPosition(self, y_V_pos, x_H_pos, field):
        print(y_V_pos, x_H_pos)
        symbol = field[y_V_pos][x_H_pos]
        if symbol == CELL_FENCE:
            figure = CELL_FENCE
        elif symbol == CELL_RHUBARB:
            figure = CELL_RHUBARB
        elif symbol == CELL_GRASS:
            figure = CELL_GRASS
        elif symbol == CELL_EMPTY:
            figure = CELL_EMPTY
        elif symbol ==CELL_WOLF_2:
            figure=CELL_WOLF_2
        elif symbol==CELL_WOLF_1:
            figure = CELL_WOLF_1
        elif symbol == CELL_SHEEP_2:
            figure = CELL_SHEEP_2
        else:
            figure = CELL_SHEEP_1
        return figure

    def getMoveSearchforWolf(self,player_number, field):
        # determine which Wolf you are handling
        if player_number == 1:
            figure = CELL_WOLF_1
            own_sheep = CELL_SHEEP_1
            enemy_sheep = CELL_SHEEP_2
        else:
            figure = CELL_WOLF_2
            own_sheep = CELL_SHEEP_2
            enemy_sheep = CELL_SHEEP_1
        my_pos = self.get_player_position(figure, field)

        print(" 我战狼目标是猎捕敌羊")
        return self.huntSheep(figure, my_pos[0], my_pos[1], enemy_sheep, field)

    # compute ManhDistance between my wolf position and enemy sheep position
    # if the distance is 1, wolf is nearby the enemy sheep and return enemysheep position
    def catchableSheep(self, y_V, x_H, player_number, field):
        if player_number == 1:
            enemySheep_pos = self.get_player_position(CELL_SHEEP_2,field)
        else:
            enemySheep_pos = self.get_player_position(CELL_SHEEP_1,field)
        if self.getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1]) == 1:
            print('my wolf is close enough to enemy sheep! KILL IT')
            return enemySheep_pos
        else:
            return None

    # compute ManhDistance between my wolf position and enemy sheep position
    # compute ManhDistance between my sheep position and enemy sheep position
    # compute ManhDistance between my sheep position and my wolf position
    # SW   W    sS  s    s  Ss  WS  W
    # s   sS     W  SW  WS  W    s  Ss
    # return wolf action position
    def trapableSheep(self, y_V, x_H, player_number, field):
        if player_number == 1:
            ownSheep_pos = self.get_player_position(CELL_SHEEP_1,field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_2,field)
        else:
            ownSheep_pos = self.get_player_position(CELL_SHEEP_2, field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_1,field)
        wolfDist2EnemySheep = self.getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
        sheepDist2EnemySheep = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], enemySheep_pos[0], enemySheep_pos[1])
        sheepDist2myWolf = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], y_V, x_H)
        if wolfDist2EnemySheep == self.wolfAlertDistance and  sheepDist2EnemySheep == 1 and sheepDist2myWolf ==1:
            print('my wolf and sheep is about to trap enenmy sheep')
            wolfAction_pos=(y_V, x_H)
            # SW
            # s
            if y_V < enemySheep_pos[0]  and x_H > enemySheep_pos[1]  and ownSheep_pos[0]==y_V:
                wolfAction_pos =  (y_V+1, x_H)
            #  W
            # sS
            elif y_V < enemySheep_pos[0] and x_H > enemySheep_pos[1] and ownSheep_pos[1] == x_H:
                wolfAction_pos = (y_V , x_H-1)
            # sS
            #  W
            elif y_V > enemySheep_pos[0] and x_H > enemySheep_pos[1] and ownSheep_pos[1] == x_H:
                wolfAction_pos = (y_V, x_H- 1)
            # s
            # SW
            elif y_V > enemySheep_pos[0] and x_H > enemySheep_pos[1] and ownSheep_pos[0] == y_V:
                wolfAction_pos =  (y_V-1, x_H )
            #  s
            # WS
            elif y_V > enemySheep_pos[0] and x_H < enemySheep_pos[1] and ownSheep_pos[0] == y_V:
                wolfAction_pos = (y_V-1, x_H)
            # Ss
            # W
            elif y_V > enemySheep_pos[0] and x_H < enemySheep_pos[1] and ownSheep_pos[1] == x_H:
                wolfAction_pos = (y_V , x_H+1)
            # WS
            #  s
            elif y_V < enemySheep_pos[0] and x_H < enemySheep_pos[1] and ownSheep_pos[0] == y_V:
                wolfAction_pos = (y_V + 1, x_H)
            # W
            # Ss
            # if y_V < enemySheep_pos[0] and x_H < enemySheep_pos[1] and ownSheep_pos[1] == x_H:
            else:
                wolfAction_pos = (y_V,  x_H + 1)
            return wolfAction_pos
        else:
            return None

    def stuckableSheep(self, y_V, x_H, player_number, field):
        FLAG= False
        if player_number == 1:
            ownSheep_pos = self.get_player_position(CELL_SHEEP_1, field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_2, field)
        else:
            ownSheep_pos = self.get_player_position(CELL_SHEEP_2, field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_1, field)
        wolfDist2EnemySheep = self.getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
        sheepDist2EnemySheep = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], enemySheep_pos[0],enemySheep_pos[1])
        sheepDist2myWolf = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], y_V, x_H)
        if not (wolfDist2EnemySheep == self.wolfAlertDistance and sheepDist2EnemySheep == 1 and sheepDist2myWolf == 1):
            if  abs(y_V - enemySheep_pos[0]) ==1 and abs(x_H - enemySheep_pos[1]) == 1:
                # print( "敌羊坐标为：" , enemySheep_pos)
                # 左上角
                if enemySheep_pos[0]==0 and enemySheep_pos[1]==0:
                    FLAG = True
                    return FLAG
                # 左下角
                if enemySheep_pos[0] == FIELD_HEIGHT -1  and enemySheep_pos[1]==0:
                    FLAG = True
                    return FLAG
                # 右上角
                if enemySheep_pos[0] == 0  and enemySheep_pos[1]  ==  FIELD_WIDTH-1:
                    FLAG = True
                    return FLAG
                # 右下角
                if enemySheep_pos[0] == FIELD_HEIGHT-1 and enemySheep_pos[1]  == FIELD_WIDTH-1:
                    FLAG = True
                    return FLAG
                if enemySheep_pos[0]>0 and enemySheep_pos[0]< FIELD_HEIGHT -2  and enemySheep_pos[1]>0 and enemySheep_pos[1]<FIELD_WIDTH-2:
                    print('y now is : ',enemySheep_pos[0])
                    # 左和上皆为CELL_FENCE
                    if (self.getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                            (self.getObjbyPosition(enemySheep_pos[0] , enemySheep_pos[1]-1, field) == CELL_FENCE) :
                        FLAG = True
                        return FLAG
                    # 左和下皆为CELL_FENCE
                    if (self.getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                            (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE):
                        FLAG = True
                        return FLAG
                    # 右和上皆为CELL_FENCE
                    if (self.getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1] , field) == CELL_FENCE) and \
                            (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                        FLAG = True
                        return FLAG
                    # 右和下皆为CELL_FENCE
                    if (self.getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                            (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                        FLAG = True
                        return FLAG
            else:
                return FLAG
        else:
            print("这里其实进不来")
            return FLAG


    def closest_goal(self, player_number, field):
        possible_goals = []

        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)

        # make list of possible goals

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    possible_goals.append((y_position, x_position))
                x_position += 1
            y_position += 1

        # determine closest item and return
        distance = 1000
        for possible_goal in possible_goals:
            if (abs(possible_goal[0] - sheep_position[0]) + abs(possible_goal[1] - sheep_position[1])) < distance:
                distance = abs(possible_goal[0] - sheep_position[0]) + abs(possible_goal[1] - sheep_position[1])
                final_goal = (possible_goal)

        return final_goal



    def wolf_close(self, player_number, field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            wolf_position = self.get_player_position(CELL_WOLF_2, field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            wolf_position = self.get_player_position(CELL_WOLF_1, field)

        if (abs(sheep_position[0] - wolf_position[0]) <= 2 and abs(sheep_position[1] - wolf_position[1]) <= 2):
            # print('wolf is close')
            return True
        return False

    def valid_move(self, figure, x_new, y_new, field):
        # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH - 1:
            return False
        elif y_new < 0:
            return False

        # Neither the sheep nor the wolf, can enter a square with a fence on.
        if field[x_new][y_new] == CELL_FENCE:
            return False

        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if field[x_new][y_new] == CELL_WOLF_2:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if field[x_new][y_new] == CELL_WOLF_1:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_2:
                return False

        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if field[x_new][y_new] == CELL_SHEEP_2 or \
                    field[x_new][y_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if field[x_new][y_new] == CELL_SHEEP_1 or \
                    field[x_new][y_new] == CELL_WOLF_2:
                return False

        return True

    def run_from_wolf(self, player_number, field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            wolf_position = self.get_player_position(CELL_WOLF_2, field)
            sheep = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            wolf_position = self.get_player_position(CELL_WOLF_1, field)
            sheep = CELL_SHEEP_2

        distance_x = sheep_position[1] - wolf_position[1]
        abs_distance_x = abs(sheep_position[1] - wolf_position[1])
        distance_y = sheep_position[0] - wolf_position[0]
        abs_distance_y = abs(sheep_position[0] - wolf_position[0])

        # print('player_number %i' %player_number)
        # print('running from wolf')
        # if the wolf is close vertically
        if abs_distance_y == 1 and distance_x == 0:
            # print('wolf is close vertically')
            # if it's above the sheep, move down if possible
            if distance_y > 0:
                if self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
                    return MOVE_DOWN
            else:  # it's below the sheep, move up if possible
                if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
                    return MOVE_UP

            # if this is not possible, flee to the right or left
            if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                return MOVE_RIGHT
            elif self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                return MOVE_LEFT
            else:  # nowhere to go
                return MOVE_NONE

        # else if the wolf is close horizontally
        elif abs_distance_x == 1 and distance_y == 0:
            # print('wolf is close horizontally')
            # if it's to the left, move to the right if possible
            if distance_x > 0:
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    # if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_RIGHT
            else:  # it's to the right, move left if possible
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    # if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_LEFT
            # if this is not possible, flee up or down
            if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
                return MOVE_UP
            elif self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
                return MOVE_DOWN
            else:  # nowhere to go
                return MOVE_NONE

        elif abs_distance_x == 1 and abs_distance_y == 1:
            # print('wolf is in my surroundings')
            # wolf is left and up
            if distance_x > 0 and distance_y > 0:
                # move right or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN
            # wolf is left and down
            if distance_x > 0 and distance_y < 0:
                # move right or up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
            # wolf is right and up
            if distance_x < 0 and distance_y > 0:
                # move left or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN
            # wolf is right and down
            if distance_x < 0 and distance_y < 0:
                # move left and up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP


        else:  # this method was wrongly called
            return MOVE_NONE

    def move_sheep(self,player_number,field):
        finalMove = MOVE_NONE
        # Node, figure(CELL_SHEEP_1 or CELL_SHEEP_2 depends on player number), my_current_position(y_V, x_H)
        suggestedAction,figure,my_pos = self.getMoveSearchforSheep(player_number, field)
        suggestedActionPos = (suggestedAction.point.x, suggestedAction.point.y)
        # check this move is safe or valid later
        # actionList给出的list,已经排除了地图外和篱笆等不可走的情况

        if not self.checkSafeFromWolf_by_Manh(my_pos[0],my_pos[1],player_number,field):
            action = self.move_far_from_wolf(figure, my_pos[0], my_pos[1], field)
            print('the action is: ', action)
            return action

        # 先检验会不会因为临时占用，导致这一步撞到己方或敌方目标
        if self.my_move_validation(figure,suggestedActionPos[0],suggestedActionPos[1],field):

            #this grid is walkable, non-occupied
            # 检测走到这个位置和 敌方狼 是否保持安全距离
            if  self.checkSafeFromWolf_by_Manh(suggestedActionPos[0],suggestedActionPos[1], player_number, field):
                print("moving to this new grid is safe from wolf")
                finalMove = self.moveParser(my_pos[0],my_pos[1],suggestedActionPos[0],suggestedActionPos[1])
                return finalMove
            else:
                # 走到这里非常不安全， 需要逃离敌方的狼
                finalMove = self.move_far_from_wolf(figure, my_pos[0],my_pos[1] ,field)
                return finalMove
        return finalMove

    # defs for wolf
    def move_wolf(self,player_number,field):
        finalMove = MOVE_NONE
        print("战狼行动中,获取行动计划")
        # Node,  figure(CELL_SHEEP_1 or CELL_SHEEP_2 depends on player number),  my_current_position(y_V, x_H)
        suggestedAction,figure,my_pos = self.getMoveSearchforWolf(player_number, field)
        # suggestedActionPos: (y_V, x_H)
        suggestedActionPos = (suggestedAction.point.x, suggestedAction.point.y)

        checkSheepCatchable = self.catchableSheep(my_pos[0], my_pos[1], player_number, field)
        if checkSheepCatchable:
            print("敌羊离我很近， 猎捕敌羊")
            finalMove = self.moveParser(my_pos[0], my_pos[1], checkSheepCatchable[0], checkSheepCatchable[1])
            return finalMove

        checkSheepTrapable = self.trapableSheep(my_pos[0], my_pos[1], player_number, field)
        if checkSheepTrapable  :
            print("围猎敌羊")
            finalMove = self.moveParser(my_pos[0], my_pos[1], checkSheepTrapable[0], checkSheepTrapable[1])
            return finalMove

        checkSheepStuckable = self.stuckableSheep(my_pos[0], my_pos[1], player_number, field)
        if checkSheepStuckable:
            print("卡住敌羊，等待己羊驰援")
            return finalMove

        # check this move is valid： actionList给出的action,已排除了地图外和篱笆等不可走情况
        # 先检验会不会因为临时占用，导致这一步撞到己方或敌方目标
        if self.my_move_validation(figure,suggestedActionPos[0],suggestedActionPos[1],field):
            print(" grid is walkable, non-occupied")
            finalMove = self.moveParser(my_pos[0],my_pos[1],suggestedActionPos[0],suggestedActionPos[1])
        return finalMove

    def my_move_validation(self, figure, y_V_new, x_H_new, field):
        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if field[y_V_new][x_H_new] == CELL_WOLF_2:
                return False
            elif field[y_V_new][x_H_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if field[y_V_new][x_H_new] == CELL_WOLF_1:
                return False
            elif field[y_V_new][x_H_new] == CELL_SHEEP_2:
                return False

        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if field[y_V_new][x_H_new] == CELL_SHEEP_2 or \
                    field[y_V_new][x_H_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if field[y_V_new][x_H_new] == CELL_SHEEP_1 or \
                    field[y_V_new][x_H_new] == CELL_WOLF_2:
                return False
        return True

    def moveParser(self,  y_V_my_pos,x_H_my_pos,y_V_new,x_H_new):
        moveAction = MOVE_NONE
        # in the same row:
        if y_V_my_pos == y_V_new :
            if x_H_my_pos < x_H_new:
                moveAction = MOVE_RIGHT
            else:
                moveAction = MOVE_LEFT
        # in the same column
        else:
            if y_V_my_pos < y_V_new:
                moveAction = MOVE_DOWN
            else:
                moveAction = MOVE_UP
        return moveAction

    def getFoodsPosition(self, my_pos_y_V, my_pos_x_H, field):
     # if self.food_present(field):
     possible_foods = []
     y_V_position = 0
     for line in field:
         x_H_position = 0
         for item_figure in line:
             if item_figure == CELL_GRASS:
                 possible_foods.append(
                     (self.getManhDistance(my_pos_y_V, my_pos_x_H, y_V_position, x_H_position),
                      item_figure,
                      (y_V_position, x_H_position)))
             if item_figure == CELL_RHUBARB:
                 possible_foods.append((self.getManhDistance(my_pos_y_V, my_pos_x_H, y_V_position,
                                                             x_H_position) - (AWARD_RHUBARB -1),
                                        item_figure,
                                        (y_V_position, x_H_position)))
             x_H_position += 1
         y_V_position += 1
     return sorted(possible_foods)

    # return: True
    #   when the Manh Dist from the given spot to enemy wolf is lower than 2
    # otherwise: False
    def checkSafeFromWolf_by_Manh(self, y_V, x_H, player_number, field):
        if player_number == 1:
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
        else:
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
        distance2EnemyWolf = self.getManhDistance(y_V, x_H, wolf_position[0], wolf_position[1])
        if distance2EnemyWolf < self.wolfAlertDistance:
            print('wolf is close: dangerous!')
            return False
        else:
            return True

    def move_far_from_wolf(self, figure, my_pos_y,my_pos_x ,field):
        # action = MOVE_NONE
        if  figure == CELL_SHEEP_1:
            # enemy wolf position
            wolf_position  = self.get_player_position(CELL_WOLF_2,field)
        else:
            wolf_position = self.get_player_position(CELL_WOLF_1, field)

        sheep = figure
        sheep_position = (my_pos_y,my_pos_x)
        distance_x = sheep_position[1] - wolf_position[1]
        abs_distance_x = abs(sheep_position[1] - wolf_position[1])
        distance_y = sheep_position[0] - wolf_position[0]
        abs_distance_y = abs(sheep_position[0] - wolf_position[0])

        print('running from wolf')
        # if the wolf is close vertically
        if abs_distance_y == 1 and distance_x == 0:
            # if it's above the sheep, move down if possible
            if distance_y > 0:
                if self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
                    return MOVE_DOWN
            else:  # it's below the sheep, move up if possible
                if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
                    return MOVE_UP

            # if this is not possible, flee to the right or left
            if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                return MOVE_RIGHT
            elif self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                return MOVE_LEFT
            else:  # nowhere to go
                return MOVE_NONE

        # else if the wolf is close horizontally
        elif abs_distance_x == 1 and distance_y == 0:
            # print('wolf is close horizontally')
            # if it's to the left, move to the right if possible
            if distance_x > 0:
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                elif self.valid_move(sheep, sheep_position[0] -1, sheep_position[1] , field):
                    return MOVE_UP
                elif self.valid_move(sheep, sheep_position[0] +1, sheep_position[1] , field):
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
            else:  # it's to the right, move left if possible
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                elif self.valid_move(sheep, sheep_position[0] -1, sheep_position[1] , field):
                    return MOVE_UP
                elif self.valid_move(sheep, sheep_position[0] +1, sheep_position[1] , field):
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
            # if this is not possible, flee up or down
            # if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
            #     return MOVE_UP
            # elif self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
            #     return MOVE_DOWN
            # else:  # nowhere to go
            #     return MOVE_NONE

        elif abs_distance_x == 1 and abs_distance_y == 1:
            # print('wolf is in my surroundings')
            # wolf is left and up
            if distance_x > 0 and distance_y > 0:
                # move right or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN
            # wolf is left and down
            if distance_x > 0 and distance_y < 0:
                # move right or up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
            # wolf is right and up
            if distance_x < 0 and distance_y > 0:
                # move left or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN
            # wolf is right and down
            if distance_x < 0 and distance_y < 0:
                # move left and up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP
        else:  # this method was wrongly called
            print(" staying is the best")
            return MOVE_NONE
        # return action

    def sheepfencing(self, y_V, x_H, player_number, field):
        FLAG=False
        if player_number == 1:
            ownWolf = self.get_player_position(CELL_WOLF_1, field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_2, field)
        else:
            ownWolf = self.get_player_position(CELL_WOLF_2, field)
            enemySheep_pos = self.get_player_position(CELL_SHEEP_1, field)
        sheepDist2EnemySheep = self.getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
        wolfDist2EnemySheep = self.getManhDistance(ownWolf[0], ownWolf[1], enemySheep_pos[0],enemySheep_pos[1])
        # sheepDist2myWolf = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], y_V, x_H)
        if (wolfDist2EnemySheep == 1 and sheepDist2EnemySheep == 1) or \
            (wolfDist2EnemySheep == self.wolfAlertDistance and  sheepDist2EnemySheep == 1):
            # 左上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == 0:
                FLAG = True
                return FLAG
            # 左下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == 0:
                FLAG = True
                return FLAG
            # 右上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = True
                return FLAG
            # 右下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = True
                return FLAG
            if enemySheep_pos[0] > 0 and enemySheep_pos[0] < FIELD_HEIGHT - 2 and enemySheep_pos[1] > 0 and \
                    enemySheep_pos[1] < FIELD_WIDTH - 2:
                print('y now is : ', enemySheep_pos[0])
                # 左和上皆为CELL_FENCE
                if (self.getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE):
                    FLAG = True
                    return FLAG
                # 左和下皆为CELL_FENCE
                if (self.getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE):
                    FLAG = True
                    return FLAG
                # 右和上皆为CELL_FENCE
                if (self.getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                    FLAG = True
                    return FLAG
                # 右和下皆为CELL_FENCE
                if (self.getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (self.getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                    FLAG = True
                    return FLAG
        else:
            return FLAG

    def getMoveSearchforSheep(self, player_number, field):
        # determine which sheep you are handling
        if player_number == 1:
            figure = CELL_SHEEP_1
            mywolf = CELL_WOLF_1
            enemy_sheep = CELL_SHEEP_2
        else:
            figure = CELL_SHEEP_2
            mywolf = CELL_WOLF_2
            enemy_sheep = CELL_SHEEP_1
        my_pos = self.get_player_position(figure, field)
        my_wolf_pos = self.get_player_position(mywolf, field)

        if self.sheepfencing(my_pos[0], my_pos[1], player_number, field):
            print("咩~咩~咩~咩~ # 堵住不动，让我战狼吃你")
            new_tar_pos4sheep = self.get_player_position(enemy_sheep, field)
            self.actionList = ActionListGenerator(figure, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
            suggestedAction = self.actionList[0]
            return suggestedAction, figure, my_pos

        if self.stuckableSheep(my_wolf_pos[0], my_wolf_pos[1], player_number, field):
            print("咩~咩~咩~咩~ # my wolf is blocking the enemy sheep")
            new_tar_pos4sheep = self.get_player_position(enemy_sheep, field)
            self.actionList = ActionListGenerator(figure, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
            suggestedAction = self.actionList[0]
            return suggestedAction, figure, my_pos

        # goal( goal is a { 0- relative distance to my cur pos, 1- item figure,(rubber or grass)   2- (abs pos)}
        # check地图上有没有食物
        if self.food_present(field):
            # 有食物: 获取地图上所有食物距离排序的列表
            foodList = self.getFoodsPosition(my_pos[0], my_pos[1], field)
            # 根据距离 近度 选食物为目标
            self.goal4Sheep = foodList[self.foodclossness2sheep]
            new_tar_pos4sheep = self.goal4Sheep[2]
            self.actionList = ActionListGenerator(figure, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
            suggestedAction = self.actionList[0]
            return suggestedAction, figure,my_pos

        else:
            print("咩~ 没有食物了 # block enemy sheep")
            new_tar_pos4sheep = self.get_player_position(enemy_sheep, field)
            self.actionList = ActionListGenerator(figure, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
            suggestedAction = self.actionList[0]
            return suggestedAction, figure,my_pos



class Point():
    """docstring for point"""
    # 这里 x就是 y_V; y是x_H
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Node():
    def __init__(self, point, g = 0, h = 0):
        self.point = point        #own coor.
        self.father = None        #father node
        self.g = g                #g
        self.h = h                #h

    def manhattan(self, endNode):
        # self.h = (abs(endNode.point.x - self.point.x) + abs(endNode.point.y - self.point.y))*10
        self.h = (abs(endNode.point.x - self.point.x) + abs(endNode.point.y - self.point.y))

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

class AStarSearch_4way():
    def __init__(self, map2d, startNode, endNode):
        """
        map2d:      map
        startNode:  start point
        endNode:    end point
        """
        #openlist
        self.openList = []
        #closelist
        self.closeList = []
        #map data
        self.map2d = map2d
        #start point
        self.startNode = startNode
        #end point
        self.endNode = endNode
        #currentNode
        self.currentNode = startNode
        #final pathlist
        self.pathlist = []

    def getMinFNode(self):
        """
        获得openlist中F值最小的节点
        """
        nodeTemp = self.openList[0]
        for node in self.openList:
            if node.g + node.h < nodeTemp.g + nodeTemp.h:
                nodeTemp = node
        return nodeTemp

    def nodeInOpenlist(self,node):
        for nodeTmp in self.openList:
            if nodeTmp.point.x == node.point.x \
            and nodeTmp.point.y == node.point.y:
                return True
        return False

    def nodeInCloselist(self,node):
        for nodeTmp in self.closeList:
            if nodeTmp.point.x == node.point.x \
            and nodeTmp.point.y == node.point.y:
                return True
        return False

    def endNodeInOpenList(self):
        for nodeTmp in self.openList:
            if nodeTmp.point.x == self.endNode.point.x \
            and nodeTmp.point.y == self.endNode.point.y:
                return True
        return False

    def getNodeFromOpenList(self,node):
        for nodeTmp in self.openList:
            if nodeTmp.point.x == node.point.x \
            and nodeTmp.point.y == node.point.y:
                return nodeTmp
        return None

    def searchOneNode(self,node):
        """
        搜索一个节点
        x为是行坐标
        y为是列坐标
        """
        #忽略障碍
        if self.map2d.isPass(node.point) != True:
            return
        #忽略封闭列表
        if self.nodeInCloselist(node):
            return
        #G值计算
        # if abs(node.point.x - self.currentNode.point.x) == 1 and abs(node.point.y - self.currentNode.point.y) == 1:
        #     gTemp = 14
        # else:
        gTemp = 1


        #如果不再openList中，就加入openlist
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            #H值计算
            node.manhattan(self.endNode);
            self.openList.append(node)
            node.father = self.currentNode
        #如果在openList中，判断currentNode到当前点的G是否更小
        #如果更小，就重新计算g值，并且改变father
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp
                nodeTmp.father = self.currentNode
        return;

    def searchNear(self):
        """
        搜索节点周围的点
        按照八个方位搜索
        拐角处无法直接到达
                 (x-1,y)
        (x  ,y-1)(x  ,y)(x  ,y+1)
                 (x+1,y)
        """
        # if self.map2d.isPass(Point(self.currentNode.point.x - 1, self.currentNode.point.y)) and \
        # self.map2d.isPass(Point(self.currentNode.point.x, self.currentNode.point.y -1)):
        #     self.searchOneNode(Node(Point(self.currentNode.point.x - 1, self.currentNode.point.y - 1)))

        self.searchOneNode(Node(Point(self.currentNode.point.x - 1, self.currentNode.point.y)))

        # if self.map2d.isPass(Point(self.currentNode.point.x - 1, self.currentNode.point.y)) and \
        # self.map2d.isPass(Point(self.currentNode.point.x, self.currentNode.point.y + 1)):
        #     self.searchOneNode(Node(Point(self.currentNode.point.x - 1, self.currentNode.point.y + 1)))

        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y - 1)))
        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y + 1)))

        # if self.map2d.isPass(Point(self.currentNode.point.x, self.currentNode.point.y - 1)) and \
        # self.map2d.isPass(Point(self.currentNode.point.x + 1, self.currentNode.point.y)):
        #     self.searchOneNode(Node(Point(self.currentNode.point.x + 1, self.currentNode.point.y - 1)))

        self.searchOneNode(Node(Point(self.currentNode.point.x + 1, self.currentNode.point.y)))

        # if self.map2d.isPass(Point(self.currentNode.point.x + 1, self.currentNode.point.y)) and \
        # self.map2d.isPass(Point(self.currentNode.point.x, self.currentNode.point.y + 1)):
        #     self.searchOneNode(Node(Point(self.currentNode.point.x + 1, self.currentNode.point.y + 1)))
        return

    def start(self):
        '''''
        开始寻路
        '''
        #将初始节点加入开放列表
        self.startNode.manhattan(self.endNode);
        self.startNode.setG(0);
        self.openList.append(self.startNode)

        while True:
            #获取当前开放列表里F值最小的节点
            #并把它添加到封闭列表，从开发列表删除它
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)

            self.searchNear();

            #检验是否结束
            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp);
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True;
            elif len(self.openList) == 0:
                return False;
        return True;

    def setPathOnMap(self):
        for node in self.pathlist:
            self.map2d.setMap(node.point);

        # reversed(self.pathlist)
        # self.pathlist.pop(0)
        return self.pathlist

class Map2d():
    # """地图数据
    def __init__(self, field):
        self.data = field
        # self.w = 20
        # self.h = 10
        self.h = len(field)
        self.w = len(field[0])
        # self.passTag = '*'
        self.nonPassTag = '#'
        self.pathTag = 'o'

    def showMap(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                print(self.data[x][y], end='')
            print(" ")
        return;

    def setMap(self, point):
        if (self.data[point.x][point.y] == CELL_GRASS) or (self.data[point.x][point.y] == CELL_EMPTY) or (self.data[point.x][point.y] == CELL_RHUBARB):
            self.data[point.x][point.y] = self.pathTag
        return;

    def isPass(self, point):
        if (point.x < 0 or point.x > self.h - 1) or (point.y < 0 or point.y > self.w - 1):
            return False;

        if self.data[point.x][point.y] is not self.nonPassTag:
            return True;

class Map2d_ADV():
    # """地图数据
    def __init__(self, field):
        self.data = field
        # self.w = 20
        # self.h = 10
        self.h = len(field)
        self.w = len(field[0])
        # self.passTag = '*'
        self.nonPassTag = '#'
        self.extra_nonTag = 'x'
        self.pathTag = 'o'

    def showMap(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                print(self.data[x][y], end='')
            print(" ")
        return;

    def setMap(self, point):
        if (self.data[point.x][point.y] == CELL_GRASS) or (self.data[point.x][point.y] == CELL_EMPTY) or (self.data[point.x][point.y] == CELL_RHUBARB):
            self.data[point.x][point.y] = self.pathTag
        return;

    def isPass(self, point):
        if (point.x < 0 or point.x > self.h - 1) or (point.y < 0 or point.y > self.w - 1):
            return False;

        if self.data[point.x][point.y] not in [self.nonPassTag, self.extra_nonTag]:
            return True;

# return a pathlist or None
# pathList is a list of Point, each point is a tuple which contains a pair of coordinates
# def ActionListGenerator_adv(figure, mypos_y_V, mypos_x_H, target_y_V, target_x_H, field):
def ActionListGenerator(figure, mypos_y_V, mypos_x_H, target_y_V, target_x_H, field):
    mapTest = Map2d_ADV(field)
    if figure == CELL_SHEEP_1:
        taker = "sheep 1"
        mapTest.extra_nonTag = CELL_WOLF_2
    elif figure == CELL_SHEEP_2:
        taker = "sheep 2"
        mapTest.extra_nonTag = CELL_WOLF_1
    elif figure == CELL_WOLF_1:
        taker = "wolf 1"
    else:
        taker = "wolf 2"

    # if figure.upper() == "W":
    #     taker = "WOLF"
    # else:
    #     taker = "SHEEP"

    mapTest = Map2d(field)
    # print("show map before path planing")
    # mapTest.showMap()
    aStar = AStarSearch_4way(mapTest, Node(Point(mypos_y_V, mypos_x_H)), Node(Point(target_y_V, target_x_H)))
    ##开始寻路
    if aStar.start():
        pathList = aStar.setPathOnMap()
        print("A* start:", "show planed path on the map for",taker)
        mapTest.showMap()
        pathList.pop()

        newList = reversed(pathList)

        tmpList=[]
        for node in newList:
            tmpList.append(node)
        # self.pathlist.pop(0)
        return tmpList
    else:
        print("no way")
        return None

def ActionListGenerator_ori(figure, mypos_y_V, mypos_x_H, target_y_V, target_x_H, field):
    if figure.upper() == "W":
        taker = "WOLF"
    else:
        taker = "SHEEP"
    mapTest = Map2d(field)
    # print("show map before path planing")
    # mapTest.showMap()
    aStar = AStarSearch_4way(mapTest, Node(Point(mypos_y_V, mypos_x_H)), Node(Point(target_y_V, target_x_H)))
    ##开始寻路
    if aStar.start():
        pathList = aStar.setPathOnMap()
        print("A* start:", "show planed path on the map for",taker)
        mapTest.showMap()
        pathList.pop()

        newList = reversed(pathList)

        tmpList=[]
        for node in newList:
            tmpList.append(node)
        # self.pathlist.pop(0)
        return tmpList
    else:
        print("no way")
        return None