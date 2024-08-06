#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models import state
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(state.State, first_state_id)))