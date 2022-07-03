import unittest
from random import randrange

import pytest


class Vehicle:
    types = []

    def __init__(self, model, size, number):
        self.model = model
        self.size = size
        self.number = number
        self.parked = False

    def is_parked(self):
        if self.parked:
            print("Vehicle is parked")
            return True

        print("Vehicle is not parked")
        return False


class Bike(Vehicle):
    pass


class Scooter(Vehicle):
    pass


class Car(Vehicle):
    pass


class Bus(Vehicle):
    pass


class ParkZone:
    def __init__(self):
        self.space_available = 10
        self.parked = {}

    def park(self, vehicle):
        if self.is_space_available(vehicle.size):
            token = self.register(vehicle)
            self.space_available -= vehicle.size
            vehicle.parked = True
            print(vehicle.model, " has been parked.")
            print("Token: ", token, ", Space available ", self.space_available)
            return token
        print("No space available")
        return None

    def is_space_available(self, size):
        return (self.space_available - size) >= 0

    def register(self, vehicle):
        token = self.generate_token()
        while token in self.parked:
            token = self.generate_token()
        self.parked[token] = vehicle
        return token

    def generate_token(self):
        return randrange(1111, 9999)

    def depark(self, token):
        if token in self.parked:
            parked_vehicle = self.parked[token]
            parked_vehicle.parked = False
            self.space_available += parked_vehicle.size
            print(parked_vehicle.model, "has been deparked")
            print("Space Available: ", self.space_available)
            return self.parked.pop(token)
        raise ValueError("Invalid token or vehicle not found")

    def list_parked_vehicles(self):
        print("------Parked Vehicles------")
        for vehicle in self.parked.values():
            print(vehicle.model, vehicle.size, vehicle.number)

class TestParkingLot(unittest.TestCase):
    def test_parking_lot(self):
        bike = Bike("Suzuki Access", 1, "MH14AB1234")
        unittest.assertIsNot(not bike.is_parked())
        park_zone = ParkZone()
        token = park_zone.park(bike)
        unittest.assertIs(bike.is_parked())
        unittest.assertEquals(park_zone.depark(token), bike)
        unittest.assertIsNot(bike.is_parked())

        car = Car("Honda Jazz", 5, "MU268A")
        unittest.assertIsNot(car.is_parked())
        car_token = park_zone.park(car)
        unittest.assertIs(car.is_parked())
        with pytest.raises(ValueError, match="Invalid token or vehicle not found"):
            park_zone.depark(token)

        unittest.assertEquals(park_zone.depark(car_token), car)
        unittest.assertIs(car.is_parked())

        bus = Bus("Volvo", 5, "AN657")
        park_zone.park(bus)

        scooter = Scooter("Honda Activa", 1, "GI653")
        park_zone.park(scooter)
        park_zone.list_parked_vehicles()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
