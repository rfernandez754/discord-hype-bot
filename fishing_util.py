""" Module handles the utilities for the economy fishing minigame """
import json
import random
import logging

class FishingUtil:
    """ 
    Class handles the utilities for fishing.
    A fishing and rod level can be passed to the object when instantiated.
    The fishing and rod lvls can increase the weights of catching higher rarity fish.
    """
    def __init__(self, fishing_lvl=1, rod_lvl=1):
        self.fish_data = self.load_fish_data()
        self.fishing_lvl = fishing_lvl
        self.rod_lvl = rod_lvl

    def load_fish_data(self):
        """ Loads json fish data """
        with open('data/fish.json', 'r', encoding="utf-8") as file:
            logging.info("fish.json data loaded")
            return json.load(file)

    def calculate_catch_weight(self, fish) -> float:
        """
        Calculate the adjusted catch weight of a fish based on fishing and rod levels.

        Args:
            fish (dict): Fish data dictionary

        Returns:
            float: Weight for the fish used in random.choices()
        """
        base_catch_chance = fish['catch_chance']
        rarity = fish['rarity']

        # Adjust catch chance based on fishing and rod levels. Level 1 means no bonus.
        fishing_boost = 0.015 * (self.fishing_lvl - 1)
        rod_boost = 0.025 * (self.rod_lvl - 1)

        # Define scaling factors based on rarity
        rarity_scale = {
            'Joke' : 0,
            'Common': 0.01,
            'Uncommon': 0.012,
            'Rare': 0.015,
            'Very Rare': 0.017,
            'Legendary': 0.019,
            'Mythic': 0.021,
            'Godly': 0.022
        }

        # Get the scaling factor based on rarity (default to 0 for unknown rarity)
        scale_factor = rarity_scale.get(rarity, 0)

        # Calculate adjusted catch chance with scaled boosts (linear component)
        adjusted_catch_chance = base_catch_chance + scale_factor * (fishing_boost + rod_boost)

        return adjusted_catch_chance

    def catch_fish(self) -> [str, int, str, float, str, int]:
        """ 
        Simulate fishing
        
        Returns:
            str: catch message
            int: gold earned from selling fish
            str: species of the caught fish
            float : size of the fish
            str: rarity of the caught fish
            xp: fishing xp earned from catching the fish
        """
        chosen_fish = random.choices(
            self.fish_data['fish'],
            weights=[self.calculate_catch_weight(fish) for fish in self.fish_data['fish']],
            k=1
        )[0]
        size = round(random.uniform(chosen_fish['size_range']['min_length'],
                              chosen_fish['size_range']['max_length']),2)
        base_gold, additional_gold = self.calculate_selling_price(chosen_fish, size)
        selling_price = base_gold + additional_gold
        fish_species = chosen_fish['name']
        fish_rarity = chosen_fish['rarity']
        fish_xp = chosen_fish['xp']
        return [f"you caught a {fish_species} of size {size} cm! "
                f"You gain {fish_xp} fishing xp. "
                f"It sells for {base_gold} gold. "
                f"You gain an additional {additional_gold} gold based on the size "
                f"for a total of {selling_price} gold! "
                f"This is a {fish_rarity} fish!```",
                selling_price, fish_species, size, fish_rarity, fish_xp]

    def calculate_selling_price(self, fish, size) -> [int, float]:
        """ 
        Calculates the fishes selling price. 

        args:
            fish (dict): Fish data dictionary
            size (int): Size of the caught fish

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
            # Additional gold scales lower below the 50th percentile
            additional_gold_multiplier = 1.0 + (relative_size / (0.75 * range_size))
        elif relative_size <= 0.9 * range_size:
            additional_gold_multiplier = 1.0 + (relative_size / (0.5 * range_size))            
        else:
            # Higher multiplier for sizes above 90th percentile
            percentile = (relative_size - 0.5 * range_size) / (0.5 * range_size)
            additional_gold_multiplier = 2.0 + 2.0 * percentile

        additional_gold = round((additional_gold_multiplier * base_gold) - (base_gold))
        return [base_gold, additional_gold]
