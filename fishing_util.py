""" Module handles the utilities for the economy fishing minigame """
import json
import random
import logging

class FishingUtil:
    """ Class handles the utilities for fishing """
    def __init__(self):
        self.fish_data = self.load_fish_data()

    def load_fish_data(self):
        """ Loads json fish data """
        with open('data/fish.json', 'r', encoding="utf-8") as file:
            logging.info("fish.json data loaded")
            return json.load(file)

    def catch_fish(self):
        """ 
        Simulate fishing
        
        Returns:
            str: catch message
            int: gold earned from selling fish
        """
        chosen_fish = random.choices(
            self.fish_data['fish'],
            weights=[fish['catch_chance'] for fish in self.fish_data['fish']],
            k=1
        )[0]
        size = random.randint(chosen_fish['size_range']['min_length'],
                              chosen_fish['size_range']['max_length'])
        selling_price = self.calculate_selling_price(chosen_fish, size)
        return [f"You caught a {chosen_fish['name']} of size {size} cm! "
                f"It sells for {selling_price} gold. "
                f"This is a {chosen_fish['rarity']} fish!", selling_price]

    def calculate_selling_price(self, fish, size):
        """ Calculates the fishes selling price given the fish and the size. """
        base_gold = fish['gold']
        # additional_gold = fish['gold_per_cm'] * size
        additional_gold = 1 * size
        return base_gold + additional_gold
