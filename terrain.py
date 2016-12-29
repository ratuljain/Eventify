from django.core.management import call_command
from lettuce import before, after
import os


@before.all
def start_neo4_data():
    pass


@after.all
def delete_neo4_data(scenario):
    pass


@before.each_scenario
def flush_database(scenario):
    call_command('flush', interactive=False, verbosity=0)


@before.each_scenario
def prepare_browser(scenario):
    pass


@after.each_scenario
def destroy_browser(scenario):
    pass
