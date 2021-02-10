import pypokerengine.utils.visualize_utils as U
from pypokerengine.players import BasePokerPlayer
from scores import combinations, comb, score_hand, hand_values, df
import pokersimulation as ps
from PIL import Image
from termcolor import colored

c3, c4 = [], []


class ConsolePlayer(BasePokerPlayer):
    def __init__(self, input_receiver=None):
        # print("*** __init__")
        self.input_receiver = input_receiver if input_receiver else self.__gen_raw_input_wrapper()
        self.console_player_name = ""
        self.advice_image_opened = False

    def declare_action(self, valid_actions, player_cards, round_state):
        # print("*** declare_action")
        # print("**** U.visualize_declare_action with Action: ", valid_actions, ", Hole card: ", player_cards,
        #      ", Round state:", round_state)
        print(U.visualize_declare_action(valid_actions, player_cards, round_state, self.uuid))

        advicePrompt = input("Do you need advice on your action? (y/n)")
        if advicePrompt == "y":
            bet_amount = 0

            # process PREFLOP actions
            if round_state.get('street') == "preflop":
                if self.console_player_name == "":
                    self.console_player_name = input("Confirm console player name (e.g. 'John' as in main/config): ")

                # find console player uuid
                for key in round_state:
                    if key == 'seats':
                        for item in round_state[key]:
                            if item['name'] == self.console_player_name:
                                console_uuid = item['uuid']
                print("Console player", self.console_player_name, "participates in",
                      colored(len(round_state.get('seats')), "red", on_color=None, attrs=None), "players game")

                # find console player preflop bet amount
                for key in round_state.get('action_histories').get('preflop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                print("Current pot value is",
                      colored(round_state.get('pot').get('main').get('amount'), "red", on_color=None, attrs=None))
                print("Console player", self.console_player_name, "bet amount is",
                      colored(bet_amount, "red", on_color=None, attrs=None))

                # define preflop state cards (called here player_cards)
                # for key, value in round_state.items():
                #    if key == 'community_card':
                #        player_cards.extend(value)
                print("Console player", self.console_player_name, "flop_cards are",
                      colored(player_cards, "red", on_color=None, attrs=None))

                # change player_cards to numbered values for scoring
                for card in range(len(player_cards)):
                    player_cards[card] = ps.change_card_value(player_cards[card])
                    # print("**** flop_cards after change ", player_cards)

                print("No advice calculation for",
                      colored(round_state.get('street'), "blue", on_color=None, attrs=None), "action")

                if not self.advice_image_opened:
                    adviceImage = input("Do you want to open starting hand advice image? (y/n)")

                    if adviceImage == "y":
                        print("-- Minimize, do not close the image window --")
                        self.advice_image_opened = True
                        path = r'.\hands_3.jpg'
                        img = Image.open(path)
                        img.show()
                    else:
                        print('...no need for advice image')

            # process FLOP actions
            if round_state.get('street') == "flop":
                if self.console_player_name == "":
                    self.console_player_name = input("Enter console player name (e.g. 'c1'): ")

                # find console player uuid
                for key in round_state:
                    if key == 'seats':
                        for item in round_state[key]:
                            if item['name'] == self.console_player_name:
                                console_uuid = item['uuid']
                print("Console player", self.console_player_name, "participates in",
                      colored(len(round_state.get('seats')), "red", on_color=None, attrs=None), "players game")

                # find console player bet amount
                for key in round_state.get('action_histories').get('preflop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                for key in round_state.get('action_histories').get('flop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                print("Current pot value is",
                      colored(round_state.get('pot').get('main').get('amount'), "red", on_color=None, attrs=None))
                print("Console player", self.console_player_name, "bet amount is",
                      colored(bet_amount, "red", on_color=None, attrs=None))

                # define flop state cards (called player_cards)
                for key, value in round_state.items():
                    if key == 'community_card':
                        player_cards.extend(value)
                print("Console player", self.console_player_name, "flop_cards are",
                      colored(player_cards, "red", on_color=None, attrs=None))

                # change cards to numbered values for scoring
                for card in range(len(player_cards)):
                    player_cards[card] = ps.change_card_value(player_cards[card])

                # count flop combinations
                print("Advice calculation for",
                      colored(round_state.get('street'), "blue", on_color=None, attrs=None), "action in progress...")
                ps.flop_combinations(player_cards)

                flopScore = ps.expected_value(player_cards, comb)
                current = df.loc[df['value'] >= flopScore[0]].index[0] / 2598960 * 100
                future = df.loc[df['value'] >= flopScore[1]].index[1] / 2598960 * 100
                print('**** Your current score value is %s (out of max 135) with average expected score value being %s'
                      % (int(current), int(future)))
                players = len(round_state.get('seats'))
                pot = round_state.get('pot').get('main').get('amount')
                price = bet_amount
                if current > future:
                    ps.should_call(players, current, pot, price)
                else:
                    ps.should_call(players, future, pot, price)

            # process TURN actions
            elif round_state.get('street') == "turn":
                if self.console_player_name == "":
                    self.console_player_name = input("Enter console player name (e.g. 'c1'): ")

                # find console player uuid
                for key in round_state:
                    if key == 'seats':
                        for item in round_state[key]:
                            if item['name'] == self.console_player_name:
                                console_uuid = item['uuid']
                print("Console player", self.console_player_name, "participates in",
                      colored(len(round_state.get('seats')), "red", on_color=None, attrs=None), "players game")

                # find console player current bet amount
                for key in round_state.get('action_histories').get('preflop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                for key in round_state.get('action_histories').get('flop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                print("Current pot value is",
                      colored(round_state.get('pot').get('main').get('amount'), "red", on_color=None, attrs=None))
                print("Console player", self.console_player_name, "current bet amount is",
                      colored(bet_amount, "red", on_color=None, attrs=None))

                # define turn cards (called player_cards)
                for key, value in round_state.items():
                    if key == 'community_card':
                        player_cards.extend(value)
                print("Console player", self.console_player_name, "turn_cards are",
                      colored(player_cards, "red", on_color=None, attrs=None))

                # change cards to numbered values for scoring
                for card in range(len(player_cards)):
                    player_cards[card] = ps.change_card_value(player_cards[card])

                # calculate turn combinations
                print("Advice calculation for",
                      colored(round_state.get('street'), "blue", on_color=None, attrs=None), "action in progress...")
                ps.turn_combinations(player_cards)

                combTurn = ps.expected_value(player_cards, comb)
                current = df.loc[df['value'] >= combTurn[0]].index[0] / 2598960 * 100
                future = df.loc[df['value'] >= combTurn[1]].index[0] / 2598960 * 100
                print('**** Your current score value is %s (out of max 135) with average expected score value being %s'
                      % (int(current), int(future)))
                players = len(round_state.get('seats'))
                pot = round_state.get('pot').get('main').get('amount')
                price = bet_amount
                if current > future:
                    ps.should_call(players, current, pot, price)
                else:
                    ps.should_call(players, future, pot, price)

            # process RIVER actions
            elif round_state.get('street') == "river":
                if self.console_player_name == "":
                    self.console_player_name = input("Enter console player name (e.g. 'c1'): ")

                # find console player uuid
                for key in round_state:
                    if key == 'seats':
                        for item in round_state[key]:
                            if item['name'] == self.console_player_name:
                                console_uuid = item['uuid']
                print("Console player", self.console_player_name, "participates in",
                      colored(len(round_state.get('seats')), "red", on_color=None, attrs=None), "players game")

                # find console player current bet amount
                for key in round_state.get('action_histories').get('preflop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                for key in round_state.get('action_histories').get('flop'):
                    if key['uuid'] == console_uuid:
                        bet_amount += key['amount']
                print("Current pot value is",
                      colored(round_state.get('pot').get('main').get('amount'), "red", on_color=None, attrs=None))
                print("Console player", self.console_player_name, "current bet amount is",
                      colored(bet_amount, "red", on_color=None, attrs=None))

                # define river cards (called player_cards)
                for key, value in round_state.items():
                    if key == 'community_card':
                        player_cards.extend(value)
                print("Console player", self.console_player_name, "river_cards are",
                      colored(player_cards, "red", on_color=None, attrs=None))

                # change cards to numbered values for scoring
                for card in range(len(player_cards)):
                    player_cards[card] = ps.change_card_value(player_cards[card])

                # calculate turn combinations
                print("Advice calculation for",
                      colored(round_state.get('street'), "blue", on_color=None, attrs=None), "action in progress...")

                combRiver = ps.expected_value(player_cards, comb)
                current = df.loc[df['value'] >= combRiver[0]].index[0] / 2598960 * 100
                print('**** Your final score value is %s' % int(current))
                players = len(round_state.get('seats'))
                pot = round_state.get('pot').get('main').get('amount')
                price = bet_amount
                ps.should_call(players, current, pot, price)

        else:
            print("...no need for advice in this round")

        action, amount = self.__receive_action_from_console(valid_actions)
        return action, amount

    def receive_game_start_message(self, game_info):
        # print("*** receive_game_start_message")
        # print("**** U.visualize_game_start")
        print(U.visualize_game_start(game_info, self.uuid))
        self.__wait_until_input()

    def receive_round_start_message(self, round_count, player_cards, seats):
        # print("*** receive_round_start_message")
        # print("**** U.visualize_round_start")
        print(U.visualize_round_start(round_count, player_cards, seats, self.uuid))
        self.__wait_until_input()

    def receive_street_start_message(self, street, round_state):
        # print("*** receive_street_start_message")
        # print("**** U.visualize_street_start")
        print(U.visualize_street_start(street, round_state, self.uuid))
        self.__wait_until_input()

    def receive_game_update_message(self, new_action, round_state):
        # print("*** receive_game_update_message")
        # print("**** U.visualize_game_update")
        print(U.visualize_game_update(new_action, round_state, self.uuid))
        self.__wait_until_input()

    def receive_round_result_message(self, winners, hand_info, round_state):
        # print("*** receive_round_result_message")
        # print("**** U.visualize_round_result")
        print(U.visualize_round_result(winners, hand_info, round_state, self.uuid))
        self.__wait_until_input()

    def __wait_until_input(self):
        input("Hit <Enter> key to continue...")

    def __gen_raw_input_wrapper(self):
        # print("*** __gen_raw_input_wrapper")
        return lambda msg: input(msg)

    def __receive_action_from_console(self, valid_actions):
        # print("*** __receive_action_from_console")
        flg = self.input_receiver('Enter f(fold), c(call), r(raise).\n >> ')
        # print("*** __gen_valid_flg(valid_actions)")
        if flg in self.__gen_valid_flg(valid_actions):
            if flg == 'f':
                # print("**** Flag: f, Action: ", valid_actions[0]['action'], ", Amount: ", valid_actions[0]['amount'])
                return valid_actions[0]['action'], valid_actions[0]['amount']
            elif flg == 'c':
                # print("**** Flag: c, Action: ", valid_actions[1]['action'], ", Amount: ", valid_actions[1]['amount'])
                return valid_actions[1]['action'], valid_actions[1]['amount']
            elif flg == 'r':
                valid_amounts = valid_actions[2]['amount']
                # print("*** __receive_raise_amount_from_console with valid_amounts min and max")
                raise_amount = self.__receive_raise_amount_from_console(valid_amounts['min'], valid_amounts['max'])
                # print("**** Flag: r, Action: ", valid_actions[2]['action'], ", Amount: ", valid_actions[2]['amount'],
                #       ", Raise amount: ", raise_amount)
                return valid_actions[2]['action'], raise_amount
        else:
            return self.__receive_action_from_console(valid_actions)

    def __gen_valid_flg(self, valid_actions):
        # print("*** __gen_valid_flg")
        flags = ['f', 'c']
        is_raise_possible = valid_actions[2]['amount']['min'] != -1
        if is_raise_possible:
            flags.append('r')
        return flags

    def __receive_raise_amount_from_console(self, min_amount, max_amount):
        # print("*** __receive_raise_amount_from_console")
        raw_amount = self.input_receiver("valid raise range = [%d, %d]" % (min_amount, max_amount))
        try:
            amount = int(raw_amount)
            if (min_amount <= amount) and (amount <= max_amount):
                return amount
            else:
                print("Invalid raise amount %d. Try again.")
                return self.__receive_raise_amount_from_console(min_amount, max_amount)
        except:
            print("Invalid input received. Try again.")
            return self.__receive_raise_amount_from_console(min_amount, max_amount)
