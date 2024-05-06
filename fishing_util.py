""" Module handles the utilities for the economy fishing minigame """
import json
import random
import logging

class FishingUtil:
    """ Class handles the utilities for fishing """
    def __init__(self):
        self.fish_data = self.load_fish_data()
        # TODO maybe add the fishing level here, and the other class will just instantiate the class with the param every time the user uses the command

    def load_fish_data(self):
        """ Loads json fish data """
        with open('data/fish.json', 'r', encoding="utf-8") as file:
            logging.info("fish.json data loaded")
            return json.load(file)

    def catch_fish(self) -> [str, int, str, float, str]: # TODO add a fishing rod level parameter that is passed in to effect caught fishes
        """ 
        Simulate fishing
        
        Returns:
            str: catch message
            int: gold earned from selling fish
            str: species of the caught fish
            float : size of the fish
            str: rarity of the caught fish
        """
        chosen_fish = random.choices(
            self.fish_data['fish'],
            weights=[fish['catch_chance'] for fish in self.fish_data['fish']],
            k=1
        )[0]
        size = round(random.uniform(chosen_fish['size_range']['min_length'],
                              chosen_fish['size_range']['max_length']),2)
        base_gold, additional_gold = self.calculate_selling_price(chosen_fish, size)
        selling_price = base_gold + additional_gold
        return [f"You caught a {chosen_fish['name']} of size {size} cm! "
                f"It sells for {base_gold} gold. "
                f"This is a {chosen_fish['rarity']} fish! "
                f"You gain an additional {additional_gold} gold based on the size "
                f"for a total of {selling_price} gold!", selling_price, chosen_fish['name'], size, chosen_fish['rarity']]

    def calculate_selling_price(self, fish, size) -> [int, float]:
        """ 
        Calculates the fishes selling price. 

        Returns:
            int: base selling gold
            int: additional selling gold earned from size multiplier
        """
        base_gold = fish['gold']
        min_length = fish['size_range']['min_length']
        max_length = fish['size_range']['max_length']

        range_size = max_length - min_length
        relative_size = size - min_length

        if relative_size <= 0.5 * range_size:
            # Linear interpolation from 1.0 to 2.0 for sizes up to the midpoint
            additional_gold_multiplier = 1.0 + (relative_size / (0.5 * range_size)) * 1.0
        else:
            # Higher multiplier (e.g., up to 5 times) for sizes in the upper range (90th percentile)
            percentile = (relative_size - 0.5 * range_size) / (0.5 * range_size)
            additional_gold_multiplier = 2.0 + 3.0 * percentile  # Scale multiplier up to 5.0

        additional_gold = round((additional_gold_multiplier * base_gold) - (base_gold))
        return [base_gold, additional_gold]
