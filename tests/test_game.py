"""Money, hidden social allegiance, persistence and casino regression tests.

Run: .venv/bin/python -m unittest discover -s tests -v
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import streamlit as st
from player import Player
from game_state import initialize_game_state, check_death_conditions
from casino import blackjack as bj
from casino import roulette as roulette
from casino.dice import next_target, dice_outcome
from casino.coin_flip import flip_coin
import social
import mafia
import save_load


class State(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def card(rank):
    return bj.Card('Spades', str(rank))


class GameTests(unittest.TestCase):
    def setUp(self):
        self.state = State()
        self.patcher = patch.object(st, 'session_state', self.state)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        initialize_game_state()
        self.player = self.state.player

    def hand_game(self, hands, dealer, deck=None, split=False):
        game = dict(active=True, settled=False,
                    hands=[dict(cards=[card(c) for c in ranks], bet=100, done=False) for ranks in hands],
                    dealer=[card(c) for c in dealer], deck=[card(c) for c in (deck or [])],
                    index=0, split=split, double_rule=False, results=[])
        self.state.blackjack_state = game
        return game

    def test_winning_blackjack_pays_once(self):
        game = self.hand_game([[10,10]], [10,8])
        self.player.money = 900  # $100 already escrowed
        bj.settle_round(game, self.player)
        self.assertEqual(self.player.money, 1100)
        snapshot = self.player.to_dict()
        bj.settle_round(game, self.player)
        self.assertEqual(self.player.to_dict(), snapshot)

    def test_blackjack_push_refunds_and_bust_loses(self):
        for ranks, expected in [([10,8], 1000), ([10,10,5], 900)]:
            with self.subTest(ranks=ranks):
                self.player.money = 900
                game = self.hand_game([ranks], [10,8])
                bj.settle_round(game, self.player)
                self.assertEqual(self.player.money, expected)

    def test_split_escrows_second_bet_and_settles_hands_separately(self):
        game = self.hand_game([[8,8]], [10,8], [10,3])
        self.player.money = 900
        bj.split_hand(game, self.player)
        self.assertEqual(self.player.money, 800)
        self.assertEqual([h['bet'] for h in game['hands']], [100,100])
        self.assertFalse(bj.can_split(game, self.player))
        # Two independent results: 11 loses, 18 pushes against dealer's 18.
        bj.settle_round(game, self.player)
        self.assertEqual(self.player.money, 900)
        self.assertEqual([r['outcome'] for r in game['results']], ['loss','push'])

    def test_split_requires_same_rank_and_funds(self):
        game = self.hand_game([['J','Q']], [10,8])
        self.assertFalse(bj.can_split(game, self.player))
        game = self.hand_game([[8,8]], [10,8])
        self.player.money = 99
        with self.assertRaises(ValueError):
            bj.split_hand(game, self.player)

    def test_double_takes_one_card_for_player_and_dealer(self):
        self.player.money = 900
        game = self.hand_game([[5,6]], [2,3], [2,10])
        bj.double_hand(game, self.player)
        self.assertTrue(game['settled'])
        self.assertEqual(game['hands'][0]['bet'], 200)
        self.assertEqual(len(game['hands'][0]['cards']), 3)
        self.assertEqual(len(game['dealer']), 3)
        self.assertEqual(bj.calculate_hand_value(game['dealer']), 7)  # no draw to 17
        self.assertEqual(self.player.money, 1200)
        self.assertFalse(bj.can_double(game, self.player))

    def test_double_after_split_does_not_finish_other_hand(self):
        game = self.hand_game([[5,6],[10,8]], [2,3], [2,10], split=True)
        bj.double_hand(game, self.player)
        self.assertFalse(game['settled'])
        self.assertEqual(game['index'], 1)
        self.assertEqual(len(game['dealer']), 2)
        game['hands'][1]['done'] = True
        bj.advance_hand(game, self.player)
        self.assertEqual(len(game['dealer']), 3)
        self.assertEqual(len(game['results']), 2)

    def test_double_bust_still_draws_one_dealer_card(self):
        game = self.hand_game([[10,9]], [2,3], [2,10])
        bj.double_hand(game, self.player)
        self.assertEqual(len(game['dealer']), 3)
        self.assertEqual(game['results'][0]['outcome'], 'loss')

    def test_blackjack_all_in_survives_until_settlement(self):
        self.state.mafia_active = True
        self.player.money = 10
        self.state.blackjack_state = bj.start_round(self.player, 10)
        self.assertFalse(check_death_conditions())
        self.state.blackjack_state['settled'] = True
        self.assertTrue(check_death_conditions())

    def test_aces_are_scored_without_busting(self):
        self.assertEqual(bj.calculate_hand_value([card('A'),card('A'),card(9)]), 21)

    def test_roulette_all_bet_coverages_and_returns(self):
        sizes = set()
        for bet in roulette.CATALOG.values():
            sizes.add(len(bet['numbers']))
            self.assertEqual(bet['multiplier'] * len(bet['numbers']), 36)
            self.assertTrue(set(bet['numbers']).issubset(range(37)))
            self.assertEqual(roulette.total_return([dict(id=bet['id'], amount=10)], bet['numbers'][0]), 10*bet['multiplier'])
        self.assertEqual(sizes, {1,2,3,4,6,12,18})
        self.assertEqual(set(roulette.WHEEL_ORDER), set(range(37)))

    def test_roulette_multiple_wagers_pay_independently(self):
        bets = [dict(id='n1',amount=10),dict(id='red',amount=20),dict(id='dozen0',amount=10)]
        with patch.object(roulette, 'spin_number', return_value=1):
            result = roulette.play_spin(bets)
        self.assertEqual(result['payout'], 430)
        self.assertEqual(self.player.money, 1390)

    def test_roulette_rejects_forged_insufficient_and_duplicate_bets(self):
        bad = [[dict(id='fake',amount=10)], [dict(id='n1',amount=-10)],
               [dict(id='n1',amount=11)], [dict(id='n1',amount=True)],
               [dict(id='n1',amount=10000)], [dict(id='n1',amount=10)]*2, None]
        for bets in bad:
            with self.subTest(bets=bets), self.assertRaises(ValueError):
                roulette.validate_bets(bets, self.player.money)
        self.assertEqual(self.player.money, 1000)

    def test_roulette_assist_selects_covered_numbers(self):
        with patch.object(roulette.random, 'random', return_value=0):
            self.assertEqual(roulette.spin_number([dict(id='n7',amount=10)]), 7)
        with patch.object(roulette.random, 'random', return_value=0.99), patch.object(roulette.random, 'randint', return_value=0):
            self.assertEqual(roulette.spin_number([dict(id='n7',amount=10)]), 0)

    def test_dice_targets_change_and_both_sides_are_possible(self):
        for previous in range(3,12):
            for _ in range(20):
                target = next_target(previous)
                self.assertIn(target, range(3,12))
                self.assertNotEqual(target, previous)
        self.assertEqual(dice_outcome(6,7,'Düşük'), 'win')
        self.assertEqual(dice_outcome(8,7,'Yüksek'), 'win')
        self.assertEqual(dice_outcome(7,7,'Yüksek'), 'push')
        self.assertEqual(dice_outcome(8,7,'Düşük'), 'loss')

    def test_coin_flip_uses_two_equal_choices(self):
        with patch('casino.coin_flip.random.choice', return_value='Yazı') as choice:
            self.assertEqual(flip_coin(), 'Yazı')
            choice.assert_called_once_with(['Yazı','Tura'])

    def test_social_unlock_persists_and_rerenders_do_not_farm_requests(self):
        with patch.object(st, 'toast'):
            self.player.money = 14999
            social.update_social()
            self.assertFalse(self.state.social_unlocked)
            self.player.money = 15000
            social.update_social()
            self.assertTrue(self.state.social_unlocked)
            self.assertEqual(len(self.state.social_requests), 1)
            social.update_social()
            self.assertEqual(len(self.state.social_requests), 1)
            self.player.money = 100
            social.update_social()
            self.assertTrue(self.state.social_unlocked)
        self.assertGreater(social.request_rate(90000)[0], social.request_rate(15000)[0])
        self.assertGreater(social.request_rate(90000)[1], social.request_rate(15000)[1])

    def test_request_allegiance_is_half_probability_and_not_in_bio(self):
        with patch.object(social.random, 'random', side_effect=[0.49,0.1]):
            hostile = social.generate_request()
        with patch.object(social.random, 'random', side_effect=[0.50,0.1]):
            friendly = social.generate_request()
        self.assertTrue(hostile['hostile'])
        self.assertFalse(friendly['hostile'])
        self.assertFalse(hostile['revealed'])
        self.assertIsNotNone(friendly['enemy_of'])

    def test_accepted_spy_queues_extra_raid_without_consuming_normal_check(self):
        with patch.object(social.random, 'random', return_value=0):
            request = social.generate_request()
        self.state.social_requests.append(request)
        self.state.significant_action_performed = True
        self.state.mafia_active = True
        social.accept_request(request['id'])
        social.accept_request(request['id'])  # duplicate click is harmless
        self.assertEqual(len(self.state.social_raids), 1)
        self.assertEqual(social.group_contact_count(request['group_id']), 1)
        with patch.object(mafia.random, 'random', return_value=0):
            self.assertTrue(mafia.should_trigger_mafia_event())
        self.assertEqual(len(self.state.social_raids), 1)
        raid = self.state.social_raids[0]
        mafia.trigger_mafia_event(raid['group_id'], 'social', raid['contact_id'])
        self.assertTrue(request['revealed'])
        self.assertEqual(self.state.mafia_event_source, 'social')

    def test_friendly_contact_gives_support_once(self):
        with patch.object(social.random, 'random', return_value=0.9):
            request = social.generate_request()
        self.state.social_requests.append(request)
        social.accept_request(request['id'])
        money = self.player.money
        social.accept_request(request['id'])
        self.assertGreater(money,1000)
        self.assertEqual(money,self.player.money)
        self.assertFalse(self.state.social_raids)

    def test_stress_clamps_responds_to_events_and_has_no_gameplay_effect(self):
        self.player.change_stress(1000)
        self.assertEqual(self.player.stress,100)
        self.player.change_stress(-1000)
        self.assertEqual(self.player.stress,0)
        self.player.remove_money(200)
        self.assertGreater(self.player.stress,0)
        stress = self.player.stress
        self.player.add_money(400)
        self.assertLess(self.player.stress,stress)
        with patch.object(roulette.random, 'random', return_value=0.99), patch.object(roulette.random, 'randint', return_value=7):
            for value in [0,50,100]:
                self.player.stress=value
                self.assertEqual(roulette.spin_number([dict(id='n1',amount=10)]),7)

    def test_save_load_preserves_social_stress_and_queued_raids(self):
        self.state.social_unlocked=True
        with patch.object(social.random,'random',return_value=0):
            self.state.social_requests.append(social.generate_request())
        social.accept_request(self.state.social_requests[0]['id'])
        self.player.stress=72
        expected_contacts=copy.deepcopy(self.state.social_contacts)
        with tempfile.TemporaryDirectory() as directory, patch.object(save_load,'SAVE_FILE',str(Path(directory)/'save.json')):
            self.assertTrue(save_load.save_game()[0])
            self.state.social_contacts=[]
            self.state.social_raids=[]
            self.player.stress=0
            self.assertTrue(save_load.load_game()[0])
            self.assertEqual(self.state.social_contacts,expected_contacts)
            self.assertEqual(self.player.stress,72)
            self.assertEqual(len(self.state.social_raids),1)

    def test_old_save_migrates_with_empty_social_state(self):
        data={'player':{'money':16000,'hp':90,'total_actions':20}, 'inventory':[], 'mafia_active':True}
        with tempfile.TemporaryDirectory() as directory:
            filename=Path(directory)/'old.json'
            filename.write_text(json.dumps(data))
            with patch.object(save_load,'SAVE_FILE',str(filename)):
                self.assertTrue(save_load.load_game()[0])
                self.assertTrue(save_load.save_game()[0])
        self.assertEqual(self.player.stress,10)
        self.assertFalse(self.state.social_contacts)
        self.assertEqual(self.state.social_last_action,20)


if __name__ == '__main__':
    unittest.main()
