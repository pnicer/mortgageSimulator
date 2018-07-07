import argparse
import json

import os

import simulation


def run_simulation(config_path):
    path = os.path.join(os.path.dirname(__file__), '..', config_path)
    with open(path) as simulation_data:
        data = json.loads(simulation_data.read())

    simulation_config = simulation.Config(data)
    simulator = simulation.Simulator(simulation_config)
    return simulator.simulate()


parser = argparse.ArgumentParser(description='Calculate mortage')
parser.add_argument('simulation', help='path to simulation description')
parser.add_argument('--diff', help='path to second simulation description for diff')

args = parser.parse_args()

simulation_results = run_simulation(args.simulation)

if not args.diff:
    simulation_results.print(rates=True)
else:
    second_simulation_results = run_simulation(args.diff)
    diff = simulation.SimulatorResultsDiff(simulation_results, second_simulation_results)
    simulation_results.print()
    second_simulation_results.print()
    diff.print()
