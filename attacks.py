"""
Bazaar information related classes
"""

import curses
import utility
from window import Window

MAX_NAME_LENGTH = 10

class Attack:
    """
    Definition of an attack based on the fields of the Torn API response
    """

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

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == "defender_name":
                    if len(value) > MAX_NAME_LENGTH:
                        value = value[:10]
                setattr(self, key, value)

    def __str__(self):
        attack_time = utility.format_timestamp(self.timestamp_ended, "%Y-%m-%d")
        name_id = "{} ({})".format(self.defender_name, self.defender_id)
        return "{:10} - {:21}: {:12} - {:02f}".format(
            attack_time,
            name_id,
            self.result,
            float(self.respect_gain))

class AttackWindow(Window):
    """
    curses window that displaying the list of attacks for the player
    """
    attacks = []

    def validate_attack(self, defender_id):
        """
        Validate if the id of a defender already exists on the attacks list
        """
        ids = [defender_id for defender_id, _ in self.attacks]
        if defender_id in ids:
            return False

        return True

    def populate(self):
        self.attacks = []
        max_items = 50

        for attack_id in self.main.user_response['attacks']:
            attack_info = self.main.user_response['attacks'][attack_id]
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
        self.new_line("My (initiated) Attacks",
                      contents,
                      attributes=curses.A_BOLD | curses.A_UNDERLINE
                      )
        self.new_line("", contents)
        self.new_line("{:10} - {:21}: {:12} - {}".format(
            "Date/Time",
            "Name (ID)",
            "Result",
            "Respect"), contents)
        self.new_line("", contents)

        for _, attack in self.attacks:
            self.new_line(attack.__str__(), contents)
