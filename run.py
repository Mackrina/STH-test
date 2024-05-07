import pandas as pd
import matplotlib.pyplot as plt
import pypfilt

def simulate_Model_observations():
    scenario_file = 'experiments.toml'
    instances = list(pypfilt.load_instances(scenario_file))
    instance = instances[0]

    # Simulate observations for x(t), y(t), and z(t).
    obs_tables = pypfilt.simulate_from_model(instance)

    # Save the observations to plain-text files.
    for obs_unit, obs_table in obs_tables.items():
        out_file = f'M-{obs_unit}.csv'
        pypfilt.io.write_table(out_file, obs_table)

        df = pd.DataFrame(obs_table)
        df.set_index('time', inplace=True)
        plt.figure()
        df.plot(title=f'Observations for {obs_unit}')
        plt.xlabel('Time')
        plt.ylabel(obs_unit)
        plt.savefig(f'lorenz63-{obs_unit}.png')

    return obs_tables

# Call the function to simulate observations and save them to files
simulate_Model_observations()