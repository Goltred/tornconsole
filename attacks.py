"""
Bazaar information related classes
"""

import curses
import utility
from window import Window

MAX_NAME_LENGTH = 10

class Attack:
    timestamp_started = None
    timestamp_ended = None
    attacker_id = None
    attacker_name = None
    attacker_faction = None
    attacker_factionname = None
    defender_id = None
    defender_name = None
    defender_faction = None
    defender_factionname = None
    result = None
    respect_gain = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                if k == "defender_name":
                    if len(v) > MAX_NAME_LENGTH:
                        v = v[:10]
                setattr(self, k, v)

    def __str__(self):
        attack_time = utility.format_timestamp(self.timestamp_ended, "%Y-%m-%d")
        name_id = "{} ({})".format(self.defender_name, self.defender_id)
        return "{:10} - {:21}: {:12} - {:02f}".format(
            attack_time,
            name_id,
            self.result,
            float(self.respect_gain))

class AttackWindow(Window):
    attacks = []

    def validate_attack(self, id):
        ids = [defender_id for defender_id, _ in self.attacks]
        if id in ids:
            return False
        
        return True


    def populate(self):
        self.attacks = []
        max_items = 50
        
        for id in self.main.user_response['attacks']:
            attack_info = self.main.user_response['attacks'][id]
            defender_id = attack_info["defender_id"]
            if defender_id != 1399239 and self.validate_attack(defender_id):
                attack = Attack(**attack_info)
                self.attacks.append((attack.defender_id, attack))

            if len(self.attacks) == max_items:
                break

        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("My (initiated) Attacks", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)
        self.new_line("{:10} - {:21}: {:12} - {}".format(
            "Date/Time",
            "Name (ID)",
            "Result",
            "Respect"), contents)
        self.new_line("", contents)
        
        for _, attack in self.attacks:
            self.new_line(attack.__str__(), contents)
