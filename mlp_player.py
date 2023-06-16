"""
Xiason Kingsheep Agent by SVM


Please edit the following things before you upload your agent:
    - change the name of your file to '[uzhshortname]_A2.py', where [uzhshortname] needs to be your uzh shortname
    - change the name of the class to a name of your choosing
    - change the def 'get_class_name()' to return the new name of your class
    - change the init of your class:
        - self.name can be an (anonymous) name of your choosing
        - self.uzh_shortname needs to be your UZH shortname
    - change the name of the model in get_sheep_model to [uzhshortname]_sheep_model
    - change the name of the model in get_wolf_model to [uzhshortname]_wolf_model

The results and rankings of the agents will be published on OLAT using your 'name', not 'uzh_shortname',
so they are anonymous (and your 'name' is expected to be funny, no pressure).

"""
from config import *
import pickle
import copy

def get_class_name():
    return 'MLPPlayer'


class MLPPlayer():
    """Example class for a Kingsheep player"""

    def __init__(self):
        self.name = "MLPPlayer"
        self.uzh_shortname = "xiason"

    def get_sheep_model(self):
        return pickle.load(open('xiason_sheep_model.sav','rb'))

    def get_wolf_model(self):
        return pickle.load(open('xiason_wolf_model.sav','rb'))

    def move_sheep(self, figure, field, sheep_model):
        X_sheep = []
        game_features = []

        if figure == 1:
            sheep = 'S'
            wolf = 'W'
            player_number = 1
            enemy_sheep = 's'
            enemy_wolf = 'w'
        else:
            sheep = 's'
            wolf = 'w'
            player_number = 2
            enemy_sheep = 'S'
            enemy_wolf = 'W'


        #preprocess field to get features, add to X_sheep
        #create empty feature array for this game state

        # get positions of sheep, wolf and food items
        sheep_position = get_player_position(sheep, field)
        my_pos = sheep_position

        s_92_stayable = 0

        #       feature: sheepfencing 1(yes) or 0(no)
        s_feature_90_sheepfencing = sheepfencing(my_pos[0], my_pos[1], player_number, field)
        #        if fencing:  move: None
        if s_feature_90_sheepfencing:
            s_feature_100_food_present = 0
            s_92_stayable = 1
        else:
            s_feature_100_food_present = food_present(field)

        #       feature: stuckableSheep 1(yes) or 0(no)
        s_feature_91_stuckableSheep = stuckableSheep(my_pos[0], my_pos[1], player_number, field)

        if s_feature_91_stuckableSheep:
            s_feature_100_food_present = 0
        else:
            s_feature_100_food_present = food_present(field)

        s_101_mypos_2_new_tar_has_way = 0
        s_101_mypos_up_2_new_tar_real_dist_smaller = 0
        s_101_mypos_down_2_new_tar_real_dist_smaller = 0
        s_101_mypos_left_2_new_tar_real_dist_smaller = 0
        s_101_mypos_right_2_new_tar_real_dist_smaller = 0

        if s_feature_100_food_present:
            foodList = getFoodsPosition(my_pos[0], my_pos[1], field)
            #             foodSamplingList = getFoodsPosition(sheep,my_pos[0], my_pos[1], field)
            foodSamplingList = getFoodRealDistforPositionList(sheep, my_pos[0], my_pos[1], foodList, field)
            #  foodList: list of  (realDist,item_figure,(tar_pos_y_V, tar_pos_x_H))
            goal4Sheep = foodSamplingList[foodclossness2sheep]
            new_tar_pos4sheep = goal4Sheep[2]
            real_food_dist_from_current_2_tar = goal4Sheep[0]
            if real_food_dist_from_current_2_tar < MAX_DIST - 10:
                hasWay,real_dist_from_current_2_tar  = getRealDistance(sheep, my_pos[0], my_pos[1], new_tar_pos4sheep[0], new_tar_pos4sheep[1], field)
            else:
                real_dist_from_current_2_tar = MAX_DIST
        else:
            new_tar_pos4sheep = get_player_position(enemy_sheep, field)
            hasWay, real_dist_from_current_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)

        if getManhDistance(my_pos[0], my_pos[1], new_tar_pos4sheep[0], new_tar_pos4sheep[1]) == 1:
            s_feature_102_new_tar_neighboring = 1
        else:
            s_feature_102_new_tar_neighboring = 0

        s_105_runfromwolf = 0
        s_103_my_pos_up_walkable = 0
        s_103_my_pos_down_walkable = 0
        s_103_my_pos_left_walkable = 0
        s_103_my_pos_right_walkable = 0

        real_dist_from_current_up_2_tar = MAX_DIST + 1
        real_dist_from_current_down_2_tar = MAX_DIST + 1
        real_dist_from_current_left_2_tar = MAX_DIST + 1
        real_dist_from_current_right_2_tar = MAX_DIST + 1

        if real_dist_from_current_2_tar < MAX_DIST - 10:
            #    this means has way and one can reach there
            s_101_mypos_2_new_tar_has_way = 1
            if my_pos[1] > 0 and my_pos[1] < FIELD_WIDTH - 1 and my_pos[0] > 0 and my_pos[0] < FIELD_HEIGHT - 1:
                up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],new_tar_pos4sheep[0], new_tar_pos4sheep[1],field)
                down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1, my_pos[1],new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
                left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
                right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)

                s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
            else:
                if my_pos[1] == 0:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,
                                                                                       new_tar_pos4sheep[0],
                                                                                       new_tar_pos4sheep[1], field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                elif my_pos[1] == FIELD_WIDTH - 1:
                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,
                                                                                      new_tar_pos4sheep[0],
                                                                                      new_tar_pos4sheep[1], field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                else:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,
                                                                                       new_tar_pos4sheep[0],
                                                                                       new_tar_pos4sheep[1], field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)

                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,
                                                                                      new_tar_pos4sheep[0],
                                                                                      new_tar_pos4sheep[1], field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)

                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)

            if real_dist_from_current_up_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_up_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_down_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_down_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_left_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_left_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_right_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_right_2_new_tar_real_dist_smaller = 1

            if s_103_my_pos_up_walkable == 1:
                if s_101_mypos_up_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_up_walkable =0
            else:
                s_101_mypos_up_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_down_walkable == 1:
                if s_101_mypos_down_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_down_walkable =0
            else:
                s_101_mypos_down_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_left_walkable == 1:
                if s_101_mypos_left_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_left_walkable =0
            else:
                s_101_mypos_left_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_right_walkable == 1:
                if s_101_mypos_right_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_right_walkable =0
            else:
                s_101_mypos_right_2_new_tar_real_dist_smaller = 0


            s_105_runfromwolf = 1

        else:
            #     no way
            s_feature_104_my_pos_stay_safeable = checkSafeFromWolf_by_Manh(my_pos[0], my_pos[1], player_number, field)
            if not s_feature_104_my_pos_stay_safeable:
                #      if stay is dangerous (not safe)
                s_105_runfromwolf = 1
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0

                if my_pos[1] > 0 and my_pos[1] < FIELD_WIDTH - 1 and my_pos[0] > 0 and my_pos[0] < FIELD_HEIGHT - 1:
                    s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
                else:
                    if my_pos[1] == 0:
                        s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number,
                                                                            field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        elif my_pos[0] == FIELD_HEIGHT - 1:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                    elif my_pos[1] == FIELD_WIDTH - 1:
                        s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number,
                                                                           field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        elif my_pos[0] == FIELD_HEIGHT - 1:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                    else:
                        s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number,
                                                                            field)
                        s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number,
                                                                           field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
            else:
                s_92_stayable = 1
                s_105_runfromwolf = 0
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0

        s_feature_104_my_pos_stay_safeable = checkSafeFromWolf_by_Manh(my_pos[0], my_pos[1], player_number, field)


        if (not  s_feature_104_my_pos_stay_safeable) and real_dist_from_current_2_tar <  min(real_dist_from_current_up_2_tar,real_dist_from_current_down_2_tar,real_dist_from_current_left_2_tar,real_dist_from_current_right_2_tar ):
            minVfourWay = min(real_dist_from_current_up_2_tar,real_dist_from_current_down_2_tar,real_dist_from_current_left_2_tar,real_dist_from_current_right_2_tar )
            dictWay={ 'real_dist_from_current_up_2_tar':real_dist_from_current_up_2_tar,
                'real_dist_from_current_down_2_tar':real_dist_from_current_down_2_tar,
                'real_dist_from_current_left_2_tar':real_dist_from_current_left_2_tar,
                'real_dist_from_current_right_2_tar':real_dist_from_current_right_2_tar}

            special_way ='stay'
            for way in dictWay:
                if minVfourWay == dictWay[way]:
                    special_way = way

            if  'up'  in special_way:
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way=1
                s_101_mypos_up_2_new_tar_real_dist_smaller=1
                s_103_my_pos_up_walkable =1
                # s_101_mypos_up_2_new_tar_real_dist_smaller=1
            elif 'down' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_down_2_new_tar_real_dist_smaller=1
                s_103_my_pos_down_walkable = 1
            elif 'left' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_left_2_new_tar_real_dist_smaller=1
                s_103_my_pos_left_walkable=1
            elif 'right' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_right_2_new_tar_real_dist_smaller=1
                s_103_my_pos_right_walkable = 1
            else:
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0
                s_feature_104_my_pos_stay_safeable=1

        # features from here 
        game_features.append(s_feature_90_sheepfencing)
        game_features.append(s_feature_91_stuckableSheep)
        game_features.append(s_92_stayable)
        game_features.append(s_feature_100_food_present)
        game_features.append(s_101_mypos_2_new_tar_has_way)
        #
        game_features.append(s_101_mypos_up_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_down_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_left_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_right_2_new_tar_real_dist_smaller)
        #
        game_features.append(s_feature_102_new_tar_neighboring)
        game_features.append(s_103_my_pos_up_walkable)
        game_features.append(s_103_my_pos_down_walkable)
        game_features.append(s_103_my_pos_left_walkable)
        game_features.append(s_103_my_pos_right_walkable)
        game_features.append(s_feature_104_my_pos_stay_safeable)
        game_features.append(s_105_runfromwolf)

        #add features and move to X_sheep
        X_sheep.append(game_features)
        result = sheep_model.predict(X_sheep)
        return result

    def move_sheep_costum(self, figure, field, sheep_model):
        X_sheep = []
        game_features = []

        if figure == 1:
            sheep = 'S'
            wolf = 'W'
            player_number = 1
            enemy_sheep = 's'
            enemy_wolf = 'w'
        else:
            sheep = 's'
            wolf = 'w'
            player_number = 2
            enemy_sheep = 'S'
            enemy_wolf = 'W'


        #preprocess field to get features, add to X_sheep
        #create empty feature array for this game state

        # get positions of sheep, wolf and food items
        sheep_position = get_player_position(sheep, field)
        my_pos = sheep_position

        s_92_stayable = 0

        #       feature: sheepfencing 1(yes) or 0(no)
        s_feature_90_sheepfencing = sheepfencing(my_pos[0], my_pos[1], player_number, field)
        #        if fencing:  move: None
        if s_feature_90_sheepfencing:
            s_feature_100_food_present = 0
            s_92_stayable = 1
        else:
            s_feature_100_food_present = food_present(field)

        #       feature: stuckableSheep 1(yes) or 0(no)
        s_feature_91_stuckableSheep = stuckableSheep(my_pos[0], my_pos[1], player_number, field)

        if s_feature_91_stuckableSheep:
            s_feature_100_food_present = 0
        else:
            s_feature_100_food_present = food_present(field)

        s_101_mypos_2_new_tar_has_way = 0
        s_101_mypos_up_2_new_tar_real_dist_smaller = 0
        s_101_mypos_down_2_new_tar_real_dist_smaller = 0
        s_101_mypos_left_2_new_tar_real_dist_smaller = 0
        s_101_mypos_right_2_new_tar_real_dist_smaller = 0

        if s_feature_100_food_present:
            foodList = getFoodsPosition(my_pos[0], my_pos[1], field)
            #             foodSamplingList = getFoodsPosition(sheep,my_pos[0], my_pos[1], field)
            foodSamplingList = getFoodRealDistforPositionList(sheep, my_pos[0], my_pos[1], foodList, field)
            #  foodList: list of  (realDist,item_figure,(tar_pos_y_V, tar_pos_x_H))
            goal4Sheep = foodSamplingList[foodclossness2sheep]
            new_tar_pos4sheep = goal4Sheep[2]
            real_food_dist_from_current_2_tar = goal4Sheep[0]
            if real_food_dist_from_current_2_tar < MAX_DIST - 10:
                hasWay,real_dist_from_current_2_tar  = getRealDistance(sheep, my_pos[0], my_pos[1], new_tar_pos4sheep[0], new_tar_pos4sheep[1], field)
            else:
                real_dist_from_current_2_tar = MAX_DIST
        else:
            new_tar_pos4sheep = get_player_position(enemy_sheep, field)
            hasWay, real_dist_from_current_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1], new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)

        if getManhDistance(my_pos[0], my_pos[1], new_tar_pos4sheep[0], new_tar_pos4sheep[1]) == 1:
            s_feature_102_new_tar_neighboring = 1
        else:
            s_feature_102_new_tar_neighboring = 0

        s_105_runfromwolf = 0
        s_103_my_pos_up_walkable = 0
        s_103_my_pos_down_walkable = 0
        s_103_my_pos_left_walkable = 0
        s_103_my_pos_right_walkable = 0

        real_dist_from_current_up_2_tar = MAX_DIST + 1
        real_dist_from_current_down_2_tar = MAX_DIST + 1
        real_dist_from_current_left_2_tar = MAX_DIST + 1
        real_dist_from_current_right_2_tar = MAX_DIST + 1

        if real_dist_from_current_2_tar < MAX_DIST - 10:
            #    this means has way and one can reach there
            s_101_mypos_2_new_tar_has_way = 1
            if my_pos[1] > 0 and my_pos[1] < FIELD_WIDTH - 1 and my_pos[0] > 0 and my_pos[0] < FIELD_HEIGHT - 1:
                up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],new_tar_pos4sheep[0], new_tar_pos4sheep[1],field)
                down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1, my_pos[1],new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
                left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)
                right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,new_tar_pos4sheep[0],new_tar_pos4sheep[1], field)

                s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
            else:
                if my_pos[1] == 0:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,
                                                                                       new_tar_pos4sheep[0],
                                                                                       new_tar_pos4sheep[1], field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                elif my_pos[1] == FIELD_WIDTH - 1:
                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,
                                                                                      new_tar_pos4sheep[0],
                                                                                      new_tar_pos4sheep[1], field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,field)
                else:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] + 1,
                                                                                       new_tar_pos4sheep[0],
                                                                                       new_tar_pos4sheep[1], field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)

                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistance(sheep, my_pos[0], my_pos[1] - 1,
                                                                                      new_tar_pos4sheep[0],
                                                                                      new_tar_pos4sheep[1], field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)

                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistance(sheep, my_pos[0] + 1,my_pos[1],
                                                                                         new_tar_pos4sheep[0],
                                                                                         new_tar_pos4sheep[1], field)
                        s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistance(sheep, my_pos[0] - 1, my_pos[1],
                                                                                     new_tar_pos4sheep[0],
                                                                                     new_tar_pos4sheep[1], field)
                        s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)

            if real_dist_from_current_up_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_up_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_down_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_down_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_left_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_left_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_right_2_tar < real_dist_from_current_2_tar:
                s_101_mypos_right_2_new_tar_real_dist_smaller = 1

            if s_103_my_pos_up_walkable == 1:
                if s_101_mypos_up_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_up_walkable =0
            else:
                s_101_mypos_up_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_down_walkable == 1:
                if s_101_mypos_down_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_down_walkable =0
            else:
                s_101_mypos_down_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_left_walkable == 1:
                if s_101_mypos_left_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_left_walkable =0
            else:
                s_101_mypos_left_2_new_tar_real_dist_smaller = 0
            if s_103_my_pos_right_walkable == 1:
                if s_101_mypos_right_2_new_tar_real_dist_smaller ==1:
                    pass
                else:
                    s_103_my_pos_right_walkable =0
            else:
                s_101_mypos_right_2_new_tar_real_dist_smaller = 0


            s_105_runfromwolf = 1

        else:
            #     no way
            s_feature_104_my_pos_stay_safeable = checkSafeFromWolf_by_Manh(my_pos[0], my_pos[1], player_number, field)
            if not s_feature_104_my_pos_stay_safeable:
                #      if stay is dangerous (not safe)
                s_105_runfromwolf = 1
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0

                if my_pos[1] > 0 and my_pos[1] < FIELD_WIDTH - 1 and my_pos[0] > 0 and my_pos[0] < FIELD_HEIGHT - 1:
                    s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number, field)
                    s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number, field)
                    s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number, field)
                    s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number, field)
                else:
                    if my_pos[1] == 0:
                        s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number,
                                                                            field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        elif my_pos[0] == FIELD_HEIGHT - 1:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                    elif my_pos[1] == FIELD_WIDTH - 1:
                        s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number,
                                                                           field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        elif my_pos[0] == FIELD_HEIGHT - 1:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                    else:
                        s_103_my_pos_right_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] + 1, player_number,
                                                                            field)
                        s_103_my_pos_left_walkable = checkwalkableforsheep(my_pos[0], my_pos[1] - 1, player_number,
                                                                           field)
                        if my_pos[0] == 0:
                            s_103_my_pos_down_walkable = checkwalkableforsheep(my_pos[0] + 1, my_pos[1], player_number,
                                                                               field)
                        else:
                            s_103_my_pos_up_walkable = checkwalkableforsheep(my_pos[0] - 1, my_pos[1], player_number,
                                                                             field)
            else:
                s_92_stayable = 1
                s_105_runfromwolf = 0
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0

        s_feature_104_my_pos_stay_safeable = checkSafeFromWolf_by_Manh(my_pos[0], my_pos[1], player_number, field)


        if (not  s_feature_104_my_pos_stay_safeable) and real_dist_from_current_2_tar <  min(real_dist_from_current_up_2_tar,real_dist_from_current_down_2_tar,real_dist_from_current_left_2_tar,real_dist_from_current_right_2_tar ):
            minVfourWay = min(real_dist_from_current_up_2_tar,real_dist_from_current_down_2_tar,real_dist_from_current_left_2_tar,real_dist_from_current_right_2_tar )
            dictWay={ 'real_dist_from_current_up_2_tar':real_dist_from_current_up_2_tar,
                'real_dist_from_current_down_2_tar':real_dist_from_current_down_2_tar,
                'real_dist_from_current_left_2_tar':real_dist_from_current_left_2_tar,
                'real_dist_from_current_right_2_tar':real_dist_from_current_right_2_tar}

            special_way ='stay'
            for way in dictWay:
                if minVfourWay == dictWay[way]:
                    special_way = way

            if  'up'  in special_way:
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way=1
                s_101_mypos_up_2_new_tar_real_dist_smaller=1
                s_103_my_pos_up_walkable =1
                # s_101_mypos_up_2_new_tar_real_dist_smaller=1
            elif 'down' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_down_2_new_tar_real_dist_smaller=1
                s_103_my_pos_down_walkable = 1
            elif 'left' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_left_2_new_tar_real_dist_smaller=1
                s_103_my_pos_left_walkable=1
            elif 'right' in special_way :
                s_feature_102_new_tar_neighboring = 0
                s_101_mypos_2_new_tar_has_way = 1
                s_101_mypos_right_2_new_tar_real_dist_smaller=1
                s_103_my_pos_right_walkable = 1
            else:
                s_103_my_pos_up_walkable = 0
                s_103_my_pos_down_walkable = 0
                s_103_my_pos_left_walkable = 0
                s_103_my_pos_right_walkable = 0
                s_feature_104_my_pos_stay_safeable=1

        # features from here 
        game_features.append(s_feature_90_sheepfencing)
        game_features.append(s_feature_91_stuckableSheep)
        game_features.append(s_92_stayable)
        game_features.append(s_feature_100_food_present)
        game_features.append(s_101_mypos_2_new_tar_has_way)
        #
        game_features.append(s_101_mypos_up_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_down_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_left_2_new_tar_real_dist_smaller)
        game_features.append(s_101_mypos_right_2_new_tar_real_dist_smaller)
        #
        game_features.append(s_feature_102_new_tar_neighboring)
        game_features.append(s_103_my_pos_up_walkable)
        game_features.append(s_103_my_pos_down_walkable)
        game_features.append(s_103_my_pos_left_walkable)
        game_features.append(s_103_my_pos_right_walkable)
        game_features.append(s_feature_104_my_pos_stay_safeable)
        game_features.append(s_105_runfromwolf)

        #add features and move to X_sheep
        X_sheep.append(game_features)
        result = sheep_model.predict(X_sheep)
        return result, game_features


    def move_wolf(self, figure, field, wolf_model):
        X_wolf = []
        game_features = []

        if figure == 1:
            sheep = 'S'
            wolf = 'W'
            player_number = 1
            enemy_sheep = 's'
            enemy_wolf = 'w'
        else:
            sheep = 's'
            wolf = 'w'
            player_number = 2
            enemy_sheep = 'S'
            enemy_wolf = 'W'

        #preprocess field to get features, add to X_wolf
        #create empty feature array for this game state

        # get positions of sheep, wolf and food items
        sheep_position = get_player_position(sheep, field)
        wolf_position = get_player_position(wolf, field)
        my_pos = wolf_position
        enemy_sheep_pos = get_player_position(enemy_sheep, field)

        w_92_stayable = 0
        #       feature: stuckableSheep 1(yes) or 0(no)
        w_feature_91_stuckableSheep = WolfstuckableSheep(my_pos[0], my_pos[1], player_number, field)

        if w_feature_91_stuckableSheep:
            w_92_stayable = 1
        else:
            w_92_stayable = 0

        w_101_mypos_2_new_tar_has_way = 0

        w_101_mypos_up_2_new_tar_real_dist_smaller = 0
        w_101_mypos_down_2_new_tar_real_dist_smaller = 0
        w_101_mypos_left_2_new_tar_real_dist_smaller = 0
        w_101_mypos_right_2_new_tar_real_dist_smaller = 0

        w_103_my_pos_up_walkable = 0
        w_103_my_pos_down_walkable = 0
        w_103_my_pos_left_walkable = 0
        w_103_my_pos_right_walkable = 0

        new_tar_pos4wolf = enemy_sheep_pos
        hasWay, real_dist_from_current_2_tar = getRealDistanceforWolf(wolf, my_pos[0], my_pos[1],
                                                                      new_tar_pos4wolf[0], new_tar_pos4wolf[1], field)
        if hasWay == 1:
            w_101_mypos_2_new_tar_has_way = 1
            if w_feature_91_stuckableSheep == 1:
                w_92_stayable = 1
            else:
                w_92_stayable = 0
        else:
            w_101_mypos_2_new_tar_has_way = 0
            w_92_stayable = 1

        if real_dist_from_current_2_tar < MAX_DIST - 10:
            #             this means has way and one can reach there
            real_dist_from_current_up_2_tar = MAX_DIST + 1
            real_dist_from_current_down_2_tar = MAX_DIST + 1
            real_dist_from_current_left_2_tar = MAX_DIST + 1
            real_dist_from_current_right_2_tar = MAX_DIST + 1

            w_103_my_pos_up_walkable = 0
            w_103_my_pos_down_walkable = 0
            w_103_my_pos_left_walkable = 0
            w_103_my_pos_right_walkable = 0

            if my_pos[1] > 0 and my_pos[1] < FIELD_WIDTH - 1 and my_pos[0] > 0 and my_pos[0] < FIELD_HEIGHT - 1:
                w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)
                w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number, field)
                w_103_my_pos_left_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] - 1, player_number, field)
                w_103_my_pos_right_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] + 1, player_number, field)
                if w_103_my_pos_up_walkable:
                    up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                           my_pos[1],
                                                                                           new_tar_pos4wolf[0],
                                                                                           new_tar_pos4wolf[1], field)
                if w_103_my_pos_down_walkable:
                    down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                if w_103_my_pos_left_walkable:
                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                               my_pos[1] - 1,
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                if w_103_my_pos_right_walkable:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                                 my_pos[1] + 1,
                                                                                                 new_tar_pos4wolf[0],
                                                                                                 new_tar_pos4wolf[1],
                                                                                                 field)

            else:
                if my_pos[1] == 0:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                                 my_pos[1] + 1,
                                                                                                 new_tar_pos4wolf[0],
                                                                                                 new_tar_pos4wolf[1],
                                                                                                 field)
                    w_103_my_pos_right_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] + 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                                   my_pos[1],
                                                                                                   new_tar_pos4wolf[0],
                                                                                                   new_tar_pos4wolf[1],
                                                                                                   field)
                        w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number,
                                                                          field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                        w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                        w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                                   my_pos[1],
                                                                                                   new_tar_pos4wolf[0],
                                                                                                   new_tar_pos4wolf[1],
                                                                                                   field)
                        w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number,
                                                                          field)
                elif my_pos[1] == FIELD_WIDTH - 1:
                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                               my_pos[1] - 1,
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                    w_103_my_pos_left_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] - 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                                   my_pos[1],
                                                                                                   new_tar_pos4wolf[0],
                                                                                                   new_tar_pos4wolf[1],
                                                                                                   field)
                        w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number,
                                                                          field)
                    elif my_pos[0] == FIELD_HEIGHT - 1:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                        w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                        w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                                   my_pos[1],
                                                                                                   new_tar_pos4wolf[0],
                                                                                                   new_tar_pos4wolf[1],
                                                                                                   field)
                        w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number,
                                                                          field)
                else:
                    right_hasWay, real_dist_from_current_right_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                                 my_pos[1] + 1,
                                                                                                 new_tar_pos4wolf[0],
                                                                                                 new_tar_pos4wolf[1],
                                                                                                 field)
                    w_103_my_pos_right_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] + 1, player_number, field)
                    left_hasWay, real_dist_from_current_left_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0],
                                                                                               my_pos[1] - 1,
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                    w_103_my_pos_left_walkable = checkwalkableforWolf(my_pos[0], my_pos[1] - 1, player_number, field)
                    if my_pos[0] == 0:
                        down_hasWay, real_dist_from_current_down_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] + 1,
                                                                                                   my_pos[1],
                                                                                                   new_tar_pos4wolf[0],
                                                                                                   new_tar_pos4wolf[1],
                                                                                                   field)
                        w_103_my_pos_down_walkable = checkwalkableforWolf(my_pos[0] + 1, my_pos[1], player_number,
                                                                          field)
                    else:
                        up_hasWay, real_dist_from_current_up_2_tar = getRealDistanceforWolfTri(wolf, my_pos[0] - 1,
                                                                                               my_pos[1],
                                                                                               new_tar_pos4wolf[0],
                                                                                               new_tar_pos4wolf[1],
                                                                                               field)
                        w_103_my_pos_up_walkable = checkwalkableforWolf(my_pos[0] - 1, my_pos[1], player_number, field)

            if real_dist_from_current_up_2_tar < real_dist_from_current_2_tar:
                w_101_mypos_up_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_down_2_tar < real_dist_from_current_2_tar:
                w_101_mypos_down_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_left_2_tar < real_dist_from_current_2_tar:
                w_101_mypos_left_2_new_tar_real_dist_smaller = 1
            if real_dist_from_current_right_2_tar < real_dist_from_current_2_tar:
                w_101_mypos_right_2_new_tar_real_dist_smaller = 1

            if w_103_my_pos_up_walkable == 1:
                if w_101_mypos_up_2_new_tar_real_dist_smaller == 1:
                    pass
                else:
                    w_103_my_pos_up_walkable = 0
            else:
                w_101_mypos_up_2_new_tar_real_dist_smaller = 0

            if w_103_my_pos_down_walkable == 1:
                if w_101_mypos_down_2_new_tar_real_dist_smaller == 1:
                    pass
                else:
                    w_103_my_pos_down_walkable = 0
            else:
                w_101_mypos_down_2_new_tar_real_dist_smaller = 0

            if w_103_my_pos_left_walkable == 1:
                if w_101_mypos_left_2_new_tar_real_dist_smaller == 1:
                    pass
                else:
                    w_103_my_pos_left_walkable = 0
            else:
                w_101_mypos_left_2_new_tar_real_dist_smaller = 0

            if w_103_my_pos_right_walkable == 1:
                if w_101_mypos_right_2_new_tar_real_dist_smaller == 1:
                    pass
                else:
                    w_103_my_pos_right_walkable = 0
            else:
                w_101_mypos_right_2_new_tar_real_dist_smaller = 0

        else:
            w_92_stayable = 1

        res = trapableSheep(my_pos[0], my_pos[1], player_number, field)
        if res:
            w_92_stayable=0

        game_features.append(w_feature_91_stuckableSheep)
        game_features.append(w_92_stayable)
        # game_features.append(w_93_trapableSheep)
        game_features.append(w_101_mypos_2_new_tar_has_way)
        game_features.append(w_101_mypos_up_2_new_tar_real_dist_smaller)
        game_features.append(w_101_mypos_down_2_new_tar_real_dist_smaller)
        game_features.append(w_101_mypos_left_2_new_tar_real_dist_smaller)
        game_features.append(w_101_mypos_right_2_new_tar_real_dist_smaller)
        game_features.append(w_103_my_pos_up_walkable)
        game_features.append(w_103_my_pos_down_walkable)
        game_features.append(w_103_my_pos_left_walkable)
        game_features.append(w_103_my_pos_right_walkable)

        #add features and move to X_wolf
        X_wolf.append(game_features)
        result = wolf_model.predict(X_wolf)
        return result

wolfAlertDistance = 2
foodclossness2sheep = 0
minimumavailable_food = 8
RHUBARB_extra = 1
AWARD_RHUBARB = 5
MAX_DIST=999

def getManhDistance(y_V_from, x_H_from, y_V_to, x_H_to):
    return abs(x_H_from - x_H_to) + abs(y_V_from - y_V_to)

def get_player_position(figure, field):
    line = [x for x in field if figure in x]
    if line:
        x = line[0]
        return (field.index(x), x.index(figure))
    else:
        return None

def food_present(field):
    for line in field:
        for item in line:
            if item == CELL_RHUBARB or item == CELL_GRASS:
                return 1
    return 0

def getObjbyPosition(y_V_pos, x_H_pos, field):
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

# return a list of available food and its ABS location and
# relatively location to my current figure position or another position.
# the returned list is ordered by relatively distance to me
# by default the relative distance is referring sheep
# def getFoodsPosition(self, player_number, field):
def getFoodsPosition( my_pos_y_V, my_pos_x_H, field):
    # if self.food_present(field):
    possible_foods = []
    y_V_position = 0
    for line in field:
        x_H_position = 0
        for item_figure in line:
            if item_figure == CELL_GRASS:
                possible_foods.append(
                    (getManhDistance(my_pos_y_V, my_pos_x_H, y_V_position, x_H_position),
                     item_figure,
                     (y_V_position, x_H_position)))
            if item_figure == CELL_RHUBARB:
                possible_foods.append((getManhDistance(my_pos_y_V, my_pos_x_H, y_V_position,
                                                            x_H_position) - (AWARD_RHUBARB + RHUBARB_extra),
                                       item_figure,
                                       (y_V_position, x_H_position)))
            x_H_position += 1
        y_V_position += 1
    return sorted(possible_foods)

def getFoodsPositionbyRealDist(figure, my_pos_y_V, my_pos_x_H, field):
    print(field)
    possible_foods = []
    y_V_position = 0
    for line in field:
        x_H_position = 0
        for item_figure in line:
            hasWay,realDist = getRealDistance(figure,my_pos_y_V, my_pos_x_H, y_V_position, x_H_position,field)
            if item_figure == CELL_GRASS:
                possible_foods.append((realDist,item_figure,(y_V_position, x_H_position)) )
            if item_figure == CELL_RHUBARB:
                possible_foods.append((realDist - (AWARD_RHUBARB + RHUBARB_extra),
                                       item_figure,
                                       (y_V_position, x_H_position)))
            x_H_position += 1
        y_V_position += 1
    return sorted(possible_foods)

def getFoodRealDistforPositionList(figure, my_pos_y_V, my_pos_x_H, foodlist, field):
    possible_foods = []
    for n in range(min(6, len(foodlist))):
        manh_f, item_figure, pos_f = foodlist[n]
        hasWay, realDist = getRealDistance(figure, my_pos_y_V, my_pos_x_H, pos_f[0], pos_f[1], field)

        if item_figure == CELL_GRASS:
            possible_foods.append((realDist, item_figure, pos_f))
        if item_figure == CELL_RHUBARB:
            possible_foods.append((realDist - (AWARD_RHUBARB + RHUBARB_extra), item_figure, pos_f))

        possible_foods.append((realDist - (AWARD_RHUBARB + RHUBARB_extra), item_figure,
                               pos_f))
    return possible_foods

def sheepfencing(y_V, x_H, player_number, field):
    FLAG = 0
    if player_number == 1:
        ownWolf = get_player_position(CELL_WOLF_1, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_2, field)
        enemyWolf_pos = get_player_position(CELL_WOLF_2, field)
    else:
        ownWolf = get_player_position(CELL_WOLF_2, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_1, field)
        enemyWolf_pos = get_player_position(CELL_WOLF_1, field)
    sheepDist2EnemySheep = getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
    wolfDist2EnemySheep = getManhDistance(ownWolf[0], ownWolf[1], enemySheep_pos[0], enemySheep_pos[1])
    # sheepDist2myWolf = self.getManhDistance(ownSheep_pos[0], ownSheep_pos[1], y_V, x_H)
    sheepDist2EnemyWolf = getManhDistance(y_V, x_H, enemyWolf_pos[0], enemyWolf_pos[1])
    if (wolfDist2EnemySheep == 1 and sheepDist2EnemySheep == 1) or \
            (wolfDist2EnemySheep == wolfAlertDistance and sheepDist2EnemySheep == 1
                and sheepDist2EnemyWolf >= wolfAlertDistance):
            # (wolfDist2EnemySheep == wolfAlertDistance and sheepDist2EnemySheep == 1):

        # 左上角
        if enemySheep_pos[0] == 0 and enemySheep_pos[1] == 0:
            FLAG = 1
            return FLAG
        # 左下角
        if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == 0:
            FLAG = 1
            return FLAG
        # 右上角
        if enemySheep_pos[0] == 0 and enemySheep_pos[1] == FIELD_WIDTH - 1:
            FLAG = 1
            return FLAG
        # 右下角
        if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == FIELD_WIDTH - 1:
            FLAG = 1
            return FLAG
        if enemySheep_pos[0] > 0 and enemySheep_pos[0] < FIELD_HEIGHT - 1 and enemySheep_pos[1] > 0 and \
                enemySheep_pos[1] < FIELD_WIDTH - 1:
            # 左和上皆为CELL_FENCE
            if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                    (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE):
                FLAG = 1
                return FLAG
            # 左和下皆为CELL_FENCE
            if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                    (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE):
                FLAG = 1
                return FLAG
            # 右和上皆为CELL_FENCE
            if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                    (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                FLAG = 1
                return FLAG
            # 右和下皆为CELL_FENCE
            if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                    (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE):
                FLAG = 1
                return FLAG
            else:
                return FLAG
        else:
            return FLAG
    else:
        return FLAG

# stuck enemy sheep, let my wolf eat it
def stuckableSheep(y_V, x_H, player_number, field):
    #         print("in")
    FLAG = 0
    if player_number == 1:
        ownWolf_pos = get_player_position(CELL_WOLF_1, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_2, field)
    else:
        ownWolf_pos = get_player_position(CELL_WOLF_2, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_1, field)

    wolfDist2EnemySheep = getManhDistance(ownWolf_pos[0], ownWolf_pos[1], enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2EnemySheep = getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2myWolf = getManhDistance(y_V, x_H, ownWolf_pos[0], ownWolf_pos[1])

    #         print(wolfDist2EnemySheep,sheepDist2EnemySheep,sheepDist2myWolf)

    if not (wolfDist2EnemySheep == wolfAlertDistance and sheepDist2EnemySheep == 1 and sheepDist2myWolf == 1):
        if abs(y_V - enemySheep_pos[0]) == 1 and abs(x_H - enemySheep_pos[1]) == 1:
            # print( "敌羊坐标为：" , enemySheep_pos)
            # 左上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == 0:
                FLAG = 1
                return FLAG
            # 左下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == 0:
                FLAG = 1
                return FLAG
            # 右上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = 1
                return FLAG
            # 右下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = 1
                return FLAG
            if enemySheep_pos[0] > 0 and enemySheep_pos[0] < FIELD_HEIGHT - 1 and enemySheep_pos[1] > 0 and \
                    enemySheep_pos[1] < FIELD_WIDTH - 1:
                #                     print('y now is : ',enemySheep_pos[0])
                # 左和上皆为CELL_FENCE

                # print("Y#")
                # print("#T")
                # print("不算卡住")

                if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE) and\
                        getManhDistance(y_V,x_H, enemySheep_pos[0] - 1, enemySheep_pos[1]) !=1 and\
                        getManhDistance(y_V,x_H, enemySheep_pos[0], enemySheep_pos[1] -1 ) !=1 :
                    FLAG = 1
                    return FLAG
                # 左和下皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE) and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0] +1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] - 1) != 1:
                    FLAG = 1
                    return FLAG
                # 右和上皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE) and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0] - 1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] + 1) != 1:
                    FLAG = 1
                    return FLAG
                # 右和下皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) ==  CELL_FENCE) and\
                        getManhDistance(y_V, x_H, enemySheep_pos[0] + 1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] + 1) != 1:
                    FLAG = 1
                    return FLAG
                else:
                    #                         print("i do not believe you!")
                    return FLAG

            else:
                #                     print("can you reach here?")
                return FLAG

        else:
            return FLAG
    else:
        #             print("不具备卡住条件 这里其实进不来")
        return FLAG

# stuck enemy sheep, wait for my sheep's assitance
def WolfstuckableSheep(y_V, x_H, player_number, field):
    #         print("in")
    FLAG = 0
    if player_number == 1:
        ownSheep_pos = get_player_position(CELL_SHEEP_1, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_2, field)
    else:
        ownSheep_pos = get_player_position(CELL_SHEEP_2, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_1, field)

    wolfDist2EnemySheep = getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2EnemySheep = getManhDistance(ownSheep_pos[0], ownSheep_pos[1], enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2myWolf = getManhDistance(y_V, x_H, ownSheep_pos[0], ownSheep_pos[1])

    #         print(wolfDist2EnemySheep,sheepDist2EnemySheep,sheepDist2myWolf)

    if not (wolfDist2EnemySheep == wolfAlertDistance and sheepDist2EnemySheep == 1 and sheepDist2myWolf == 1):
        if abs(y_V - enemySheep_pos[0]) == 1 and abs(x_H - enemySheep_pos[1]) == 1:
            # print( "敌羊坐标为：" , enemySheep_pos)
            # 左上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == 0:
                FLAG = 1
                return FLAG
            # 左下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == 0:
                FLAG = 1
                return FLAG
            # 右上角
            if enemySheep_pos[0] == 0 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = 1
                return FLAG
            # 右下角
            if enemySheep_pos[0] == FIELD_HEIGHT - 1 and enemySheep_pos[1] == FIELD_WIDTH - 1:
                FLAG = 1
                return FLAG
            if enemySheep_pos[0] > 0 and enemySheep_pos[0] < FIELD_HEIGHT - 1 and enemySheep_pos[1] > 0 and \
                    enemySheep_pos[1] < FIELD_WIDTH - 1:
                #                     print('y now is : ',enemySheep_pos[0])
                # 左和上皆为CELL_FENCE

                # print("Y#")
                # print("#T")
                # print("不算卡住")

                if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE) and\
                        getManhDistance(y_V,x_H, enemySheep_pos[0] - 1, enemySheep_pos[1]) !=1 and\
                        getManhDistance(y_V,x_H, enemySheep_pos[0], enemySheep_pos[1] -1 ) !=1 :
                    FLAG = 1
                    return FLAG
                # 左和下皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] - 1, field) == CELL_FENCE) and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0] +1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] - 1) != 1:
                    FLAG = 1
                    return FLAG
                # 右和上皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] - 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) == CELL_FENCE) and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0] - 1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] + 1) != 1:
                    FLAG = 1
                    return FLAG
                # 右和下皆为CELL_FENCE
                if (getObjbyPosition(enemySheep_pos[0] + 1, enemySheep_pos[1], field) == CELL_FENCE) and \
                        (getObjbyPosition(enemySheep_pos[0], enemySheep_pos[1] + 1, field) ==  CELL_FENCE) and\
                        getManhDistance(y_V, x_H, enemySheep_pos[0] + 1, enemySheep_pos[1]) != 1 and \
                        getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1] + 1) != 1:
                    FLAG = 1
                    return FLAG
                else:
                    #                         print("i do not believe you!")
                    return FLAG

            else:
                #                     print("can you reach here?")
                return FLAG

        else:
            return FLAG
    else:
        #             print("不具备卡住条件 这里其实进不来")
        return FLAG

# case like: W
#            Ss
def trapableSheep( y_V, x_H, player_number, field):
    FLAG = 0
    if player_number == 1:
        ownSheep_pos = get_player_position(CELL_SHEEP_1,field)
        enemySheep_pos = get_player_position(CELL_SHEEP_2,field)
    else:
        ownSheep_pos = get_player_position(CELL_SHEEP_2, field)
        enemySheep_pos = get_player_position(CELL_SHEEP_1,field)
    wolfDist2EnemySheep = getManhDistance(y_V, x_H, enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2EnemySheep = getManhDistance(ownSheep_pos[0], ownSheep_pos[1], enemySheep_pos[0], enemySheep_pos[1])
    sheepDist2myWolf = getManhDistance(ownSheep_pos[0], ownSheep_pos[1], y_V, x_H)
    if wolfDist2EnemySheep == wolfAlertDistance and  sheepDist2EnemySheep == 1 and sheepDist2myWolf ==1\
            and  (enemySheep_pos[0] - y_V) * (enemySheep_pos[1] - x_H) != 0:
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
        return FLAG


def checkwalkableforsheep(y_V, x_H, player_number, field):
    FLAG = 0
    NonWalkableList = [CELL_FENCE, CELL_WOLF_1, CELL_WOLF_2]
    if player_number == 1:
        NonWalkableList.append(CELL_SHEEP_2)
        enemy_wolf_pos = get_player_position(CELL_WOLF_2, field)
    else:
        NonWalkableList.append(CELL_SHEEP_1)
        enemy_wolf_pos = get_player_position(CELL_WOLF_1, field)
    SpotDist2EnemyWolf = getManhDistance(y_V, x_H, enemy_wolf_pos[0], enemy_wolf_pos[1])

    if y_V < 0 or y_V > FIELD_HEIGHT - 1 or x_H > FIELD_WIDTH - 1 or x_H < 0:
        return FLAG
    else:
        if getObjbyPosition(y_V, x_H, field) in NonWalkableList:
            return FLAG
        elif SpotDist2EnemyWolf < wolfAlertDistance:
            return FLAG
        else:
            FLAG = 1
            return FLAG

def checkSafeFromWolf_by_Manh(y_V, x_H, player_number, field):
    if player_number == 1:
        enemy_wolf_pos = get_player_position(CELL_WOLF_2,field)
    else:
        enemy_wolf_pos = get_player_position(CELL_WOLF_1,field)
    SpotDist2EnemyWolf = getManhDistance( y_V, x_H, enemy_wolf_pos[0], enemy_wolf_pos[1])
    if SpotDist2EnemyWolf < wolfAlertDistance:
        return 0
    else:
        return 1

class Point():
    """docstring for point"""
    # x: y_V; y:x_H
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Node():
    def __init__(self, point, g=0, h=0):
        self.point = point  # own coor.
        self.father = None  # father node
        self.g = g  # g
        self.h = h  # h

    def manhattan(self, endNode):
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
        # openlist
        self.openList = []
        # closelist
        self.closeList = []
        # map data
        self.map2d = map2d
        # start point
        self.startNode = startNode
        # end point
        self.endNode = endNode
        # currentNode
        self.currentNode = startNode
        # final pathlist
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

    def nodeInOpenlist(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.point.x == node.point.x \
                    and nodeTmp.point.y == node.point.y:
                return True
        return False

    def nodeInCloselist(self, node):
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

    def getNodeFromOpenList(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.point.x == node.point.x \
                    and nodeTmp.point.y == node.point.y:
                return nodeTmp
        return None

    def searchOneNode(self, node):
        """
        搜索一个节点
        x为是行坐标
        y为是列坐标
        """
        # 忽略障碍
        if self.map2d.isPass(node.point) != True:
            return
        # 忽略封闭列表
        if self.nodeInCloselist(node):
            return
        # G值计算
        # if abs(node.point.x - self.currentNode.point.x) == 1 and abs(node.point.y - self.currentNode.point.y) == 1:
        #     gTemp = 14
        # else:
        gTemp = 1

        # 如果不再openList中，就加入openlist
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            # H值计算
            node.manhattan(self.endNode);
            self.openList.append(node)
            node.father = self.currentNode
        # 如果在openList中，判断currentNode到当前点的G是否更小
        # 如果更小，就重新计算g值，并且改变father
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp
                nodeTmp.father = self.currentNode
        return

    def searchNear(self):
        """
        搜索节点周围的点
        按照八个方位搜索
        拐角处无法直接到达
                 (x-1,y)
        (x  ,y-1)(x  ,y)(x  ,y+1)
                 (x+1,y)
        """
        self.searchOneNode(Node(Point(self.currentNode.point.x - 1, self.currentNode.point.y)))
        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y - 1)))
        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y + 1)))
        self.searchOneNode(Node(Point(self.currentNode.point.x + 1, self.currentNode.point.y)))
        return

    def start(self):
        '''''
        开始寻路
        '''
        # 将初始节点加入开放列表
        self.startNode.manhattan(self.endNode);
        self.startNode.setG(0);
        self.openList.append(self.startNode)

        while True:
            # 获取当前开放列表里F值最小的节点
            # 并把它添加到封闭列表，从开发列表删除它
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)

            self.searchNear();

            # 检验是否结束
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
        return True

    def setPathOnMap(self):
        for node in self.pathlist:
            self.map2d.setMap(node.point);

        # reversed(self.pathlist)
        # self.pathlist.pop(0)
        return self.pathlist

class Map2d_ADV():
    # """地图数据
    def __init__(self, field):
        self.data = field
        self.h = len(field)
        self.w = len(field[0])
        # self.passTag = '*'
        self.nonPassTag = '#'
        self.extraNonPassList = []
        self.pathTag = 'o'

    def showMap(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                print(self.data[x][y], end='')
            print(" ")
        return;

    def setMap(self, point):
        if (self.data[point.x][point.y] == CELL_GRASS) or (self.data[point.x][point.y] == CELL_EMPTY) or (
                self.data[point.x][point.y] == CELL_RHUBARB):
            self.data[point.x][point.y] = self.pathTag

    def isPass(self, point):
        if (point.x < 0 or point.x > self.h - 1) or (point.y < 0 or point.y > self.w - 1):
            return False

        if (self.data[point.x][point.y] is not self.nonPassTag) and (
                self.data[point.x][point.y] not in self.extraNonPassList):
            return True
        else:
            return False

def ActionListGenerator(figure, mypos_y_V, mypos_x_H, target_y_V, target_x_H, field):
    adv_map = copy.deepcopy(field)

    mapTest = Map2d_ADV(adv_map)
    if figure == CELL_SHEEP_1:
        avoid_wolf = CELL_WOLF_2
        taker = "sheep 1"
        mapTest.extraNonPassList = [CELL_WOLF_2, CELL_WOLF_1]

    elif figure == CELL_SHEEP_2:
        avoid_wolf = CELL_WOLF_1
        taker = "sheep 2"
        mapTest.extraNonPassList = [CELL_WOLF_2, CELL_WOLF_1]

    elif figure == CELL_WOLF_1:
        taker = "wolf 1"
        mapTest.extraNonPassList = [CELL_WOLF_2, CELL_SHEEP_1]
    else:
        taker = "wolf 2"
        mapTest.extraNonPassList = [CELL_WOLF_1, CELL_SHEEP_2]

    if figure in [CELL_SHEEP_1, CELL_SHEEP_2]:
        enemy_wolf_pos_y_V, enemy_wolf_pos_x_H = get_player_position(avoid_wolf, adv_map)

        if enemy_wolf_pos_x_H > 0 and enemy_wolf_pos_x_H < FIELD_WIDTH - 1 and enemy_wolf_pos_y_V > 0 and enemy_wolf_pos_y_V < FIELD_HEIGHT - 1:
            if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
            if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
            if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] = mapTest.nonPassTag
            if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] = mapTest.nonPassTag
        else:
            if enemy_wolf_pos_x_H == 0:
                if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                    mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] = mapTest.nonPassTag

                if enemy_wolf_pos_y_V == 0:
                    if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                elif enemy_wolf_pos_y_V == FIELD_HEIGHT - 1:
                    if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                else:
                    if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                    if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
            elif enemy_wolf_pos_x_H == FIELD_WIDTH - 1:
                if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                    mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] = mapTest.nonPassTag

                if enemy_wolf_pos_y_V == 0:
                    if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                elif enemy_wolf_pos_y_V == FIELD_HEIGHT - 1:
                    if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                else:
                    if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                    if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag

            else:
                if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                    mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H + 1] = mapTest.nonPassTag
                if mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] in [CELL_EMPTY, CELL_RHUBARB, CELL_GRASS]:
                    mapTest.data[enemy_wolf_pos_y_V][enemy_wolf_pos_x_H - 1] = mapTest.nonPassTag

                if enemy_wolf_pos_y_V == 0:
                    if mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                    CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V + 1][enemy_wolf_pos_x_H] = mapTest.nonPassTag
                else:
                    if mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H + 1] in [CELL_EMPTY, CELL_RHUBARB,
                                                                                        CELL_GRASS]:
                        mapTest.data[enemy_wolf_pos_y_V - 1][enemy_wolf_pos_x_H + 1] = mapTest.nonPassTag

    aStar = AStarSearch_4way(mapTest, Node(Point(mypos_y_V, mypos_x_H)), Node(Point(target_y_V, target_x_H)))
    ##开始寻路
    if aStar.start():
        pathList = aStar.setPathOnMap()
        # print("A* start:", "show planed path on the map for", taker)
        #         mapTest.showMap()
        pathList.pop()

        newList = reversed(pathList)

        tmpList = []
        for node in newList:
            tmpList.append(node)
        # self.pathlist.pop(0)
        hasWay = 1
        return tmpList, hasWay
    else:
        # print("no way, stay")
        # print("I am ", taker, "my current loc is :", mypos_y_V, mypos_x_H)
        hasWay = 0
        return [Node(Point(mypos_y_V, mypos_x_H))], hasWay


def getRealDistance(figure, my_pos_y_V, my_pos_x_H, y_V_position, x_H_position, field):
    if getObjbyPosition(my_pos_y_V, my_pos_x_H, field) in [CELL_EMPTY, CELL_GRASS, CELL_RHUBARB, figure]:
        mypos = (my_pos_y_V, my_pos_x_H)
        new_tar = (y_V_position, x_H_position)

        if mypos == new_tar:
            hasWay = 1
            return hasWay, 0

        actionList, hasWay = ActionListGenerator(figure, mypos[0], mypos[1], new_tar[0], new_tar[1], field)
        if hasWay:
            return hasWay, len(actionList)
        else:
            return hasWay, MAX_DIST
    else:
        hasWay = 0
        return hasWay, MAX_DIST

def checkwalkableforWolf(y_V, x_H, player_number, field):
    FLAG = 0
    NonWalkableList = [CELL_FENCE]
    if player_number == 1:
        NonWalkableList.append(CELL_SHEEP_1)
        NonWalkableList.append(CELL_WOLF_2)
    else:
        NonWalkableList.append(CELL_SHEEP_2)
        NonWalkableList.append(CELL_WOLF_1)

    if y_V < 0 or y_V > FIELD_HEIGHT - 1 or x_H > FIELD_WIDTH - 1 or x_H < 0:
        return FLAG
    else:
        if getObjbyPosition(y_V, x_H, field) in NonWalkableList:
            return FLAG
        else:
            FLAG = 1
            return FLAG

def getRealDistanceforWolf(figure, my_pos_y_V, my_pos_x_H, y_V_position, x_H_position, field):
    if getObjbyPosition(my_pos_y_V, my_pos_x_H, field) in [CELL_EMPTY, CELL_GRASS, CELL_RHUBARB, figure]:
        mypos = (my_pos_y_V, my_pos_x_H)
        new_tar = (y_V_position, x_H_position)

        if mypos == new_tar:
            hasWay = 1
            return hasWay, 0
        actionList, hasWay = ActionListGenerator(figure, mypos[0], mypos[1], new_tar[0], new_tar[1], field)
        if hasWay:
            return hasWay, len(actionList)
        else:
            return hasWay, MAX_DIST
    else:
        hasWay = 0
        return hasWay, MAX_DIST

def getRealDistanceforWolfTri(figure,my_pos_y_V, my_pos_x_H, y_V_position, x_H_position,field):
    mypos = (my_pos_y_V, my_pos_x_H)
    new_tar = (y_V_position,x_H_position )
    ADD_figure = getObjbyPosition(new_tar[0], new_tar[1], field)
    if getObjbyPosition(my_pos_y_V, my_pos_x_H, field) in [ADD_figure,CELL_EMPTY,CELL_GRASS,CELL_RHUBARB, figure]:
        if mypos==new_tar:
            hasWay=1
            return hasWay, 0
        actionList,hasWay = ActionListGenerator(figure, mypos[0], mypos[1], new_tar[0], new_tar[1], field)
        if hasWay :
            return hasWay, len(actionList)
        else:
            return hasWay, MAX_DIST
    else:
        hasWay=0
        return hasWay,  MAX_DIST
