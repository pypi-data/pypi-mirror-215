import Signal8

env = Signal8.env()
env.reset(options={'problem_instance': 'einstein_tile'})
start_state = env.state()
observation, _, terminations, truncations, _ = env.last()
env.step(1)
env.close()
