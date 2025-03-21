import pandas as pd
import param as pm
import numpy as np
import hvplot.pandas
import panel as pn
import holoviews as hv


class PAMMModel:
    def __init__(self, kappa, initial_reserve, initial_supply):
        self.kappa = kappa  # Constant kappa
        self.V0 = 1  # Constant V0
        self.reserve = initial_reserve  # Initial reserve
        self.supply = initial_supply    # Initial supply
        self.update_constants()

    def update_constants(self):
        """ Update V0 based on current reserve and supply to maintain the invariants. """
        self.V0 = (self.supply ** self.kappa) / self.reserve

    def deltaR_for_deltaS(self, deltaS):
        """ Calculate the required change in reserves (deltaR) for a given change in supply (deltaS) """
        S = self.supply
        R = self.reserve
        new_S = S + deltaS
        new_R = R * (new_S / S) ** self.kappa
        return new_R - R

    def deltaS_for_deltaR(self, deltaR):
        """ Calculate the required change in supply (deltaS) for a given change in reserves (deltaR) """
        S = self.supply
        R = self.reserve
        new_R = R + deltaR
        new_S = S * (new_R / R) ** (1 / self.kappa)
        return new_S - S

    def update_supply_reserve(self, deltaS, deltaR):
        """ Update the supply and reserve based on deltas and adjust V0 if necessary """
        self.supply += deltaS
        self.reserve += deltaR
        self.update_constants()

    def realised_price(self, deltaR, deltaS):
        """ Calculate the realised price of a trade, which is deltaR divided by deltaS """
        return deltaR / deltaS if deltaS != 0 else None

    def spot_price(self):
        """ Calculate the spot price based on current S and R """
        return (self.kappa*(self.supply**(self.kappa-1)))/self.V0

    def print_state_message(self):
        message = f"Supply: {self.supply}\nReserve: {self.reserve}\nV0: {self.V0}\nSpot Price: {self.spot_price()}\n"
        return message

    def print_state(self, message=""):
        """ Print the current state of the model with an optional message """
        print(message)
        print(f"Supply: {self.supply}")
        print(f"Reserve: {self.reserve}")
        print(f"V0: {self.V0}")
        print(f"Spot Price: {self.spot_price()}")
        print()  # Print a newline for better readability
