"""Streamlit integration coverage for navigation, live stats and event ordering."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from casino.blackjack import Card

ROOT = Path(__file__).resolve().parents[1]


class AppTests(unittest.TestCase):
    def app(self):
        return AppTest.from_file(str(ROOT / 'main.py')).run()

    def assert_clean(self, app):
        self.assertFalse(app.exception, [e.message for e in app.exception])

    def test_pages_show_live_stats_without_errors(self):
        # The custom roulette iframe is checked in a real browser instead.
        for page in ['blackjack','dice','coin_flip','horse_racing','social','secure',
                     'gang','stats','inventory','market','hospital']:
            with self.subTest(page=page):
                app = self.app()
                app.session_state.current_page = page
                app.run()
                self.assert_clean(app)
                self.assertTrue(any('rpg-panel' in m.value for m in app.markdown))

    def test_dice_and_coin_rounds_update_once(self):
        for page,label in [('dice','🎲 Zarları at'),('coin_flip','🪙 Parayı çevir')]:
            with self.subTest(page=page):
                app = self.app()
                app.session_state.current_page = page
                app.run()
                next(b for b in app.button if b.label == label).click().run()
                self.assert_clean(app)
                snapshot = app.session_state.player.to_dict()
                self.assertEqual(snapshot['total_actions'], 1)
                app.run()
                self.assertEqual(app.session_state.player.to_dict(), snapshot)

    def test_blackjack_split_then_double_with_widgets(self):
        app = self.app()
        c = lambda n: Card('Spades',str(n))
        app.session_state.current_page = 'blackjack'
        app.session_state.blackjack_state = dict(
            active=True,settled=False,index=0,split=False,double_rule=False,results=[],
            hands=[dict(cards=[c(8),c(8)],bet=100,done=False)],
            dealer=[c(10),c(8)],deck=[c(2),c(10),c(3),c(2)])
        app.run()
        next(b for b in app.button if b.label == '✂️ Split').click().run()
        next(b for b in app.button if b.label == '⏫ Double').click().run()
        self.assertEqual(app.session_state.blackjack_state['index'],1)
        next(b for b in app.button if b.label == '✋ Stand').click().run()
        self.assert_clean(app)
        self.assertTrue(app.session_state.blackjack_state['settled'])
        snapshot = app.session_state.player.to_dict()
        app.run()
        self.assertEqual(snapshot,app.session_state.player.to_dict())

    def test_normal_and_social_raids_both_happen(self):
        app = self.app()
        app.session_state.player.money = 20000
        app.session_state.mafia_active = True
        app.session_state.significant_action_performed = True
        app.session_state.social_raids = [dict(group_id='karahan',contact_id=999)]
        with patch('mafia.random.random',return_value=0):
            app.run()
        self.assertEqual(app.session_state.mafia_event_source,'normal')
        self.assertEqual(len(app.session_state.social_raids),1)
        app.button(key='mafia_pay').click().run()
        self.assert_clean(app)
        self.assertEqual(app.session_state.mafia_event_source,'social')
        self.assertTrue(app.session_state.mafia_event_pending)
        app.button(key='mafia_pay').click().run()
        self.assert_clean(app)
        self.assertFalse(app.session_state.mafia_event_pending)

    def test_hiring_protection_reduces_stress_even_at_low_balance(self):
        for page,label,minimum in [('secure','🛡️ Hire Bodyguard',5000),('gang','👊 Recruit Member',3000)]:
            with self.subTest(page=page):
                app = self.app()
                player = app.session_state.player
                player.money = minimum
                player.bodyguards = player.gang_members = 1
                player.stress = 50
                app.session_state.current_page = page
                app.run()
                next(b for b in app.button if b.label == label).click().run()
                self.assert_clean(app)
                self.assertLess(player.stress,50)

    def test_old_save_loads_through_menu_and_can_be_saved_again(self):
        app = self.app()
        old = {'player':{'money':16000,'hp':100,'hunger':100,'total_actions':5},'inventory':[],'mafia_active':True}
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder)/'old.json'
            filename.write_text(json.dumps(old))
            with patch('save_load.SAVE_FILE',str(filename)):
                next(b for b in app.button if b.label == '📂 Load').click().run()
                self.assert_clean(app)
                next(b for b in app.button if b.label == '💾 Save').click().run()
                self.assert_clean(app)
        self.assertTrue(app.session_state.social_unlocked)


if __name__ == '__main__':
    unittest.main()
