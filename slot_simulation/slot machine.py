import random
import math
from data import slot_machines_data, machine_prize_data, multipliers


def ucb1(k, slot_machines_data):
    n_machines = len(slot_machines_data)

    # Initialization step: play each machine once
    if k < n_machines:
        return k

    total_trials = sum([len(data) for data in slot_machines_data])

    # Calculate total win and cost for each machine
    machine_totals = [
        {
            'slot': len(data),
            'win': sum([trial[0] for trial in data]),
            'cost': sum([trial[1] for trial in data]),
        }
        for data in slot_machines_data
    ]

    # Calculate average reward for each machine
    average_rewards = [
        (total['win'] / total['slot']) - (total['cost'] / total['slot'])
        for total in machine_totals
    ]

    # Calculate upper confidence bounds for each machine
    ucb_values = [
        average_rewards[i] + math.sqrt(2 * math.log(total_trials) / machine_totals[i]['slot'])
        for i in range(n_machines)
    ]

    # Choose the machine with the highest UCB value
    best_machine = ucb_values.index(max(ucb_values))

    return best_machine


def simulate_machine_play(machine_data):
    multiplier = random.choice(multipliers[machine_data])
    cost = machine_prize_data[machine_data]['cost'] * multiplier
    reward_prize_dict = machine_prize_data[machine_data]['prizes']
    reward_prize_list = reward_prize_dict[random.choice(list(reward_prize_dict.keys()))]

    if isinstance(random.choices(reward_prize_list, weights=[prize[1] for prize in reward_prize_list])[0][0], tuple):
        reward = random.randint(reward_prize_list[-1][0][0], reward_prize_list[-1][0][1])
    else:
        reward = random.choices(reward_prize_list, weights=[prize[1] for prize in reward_prize_list])[0][0]

    return (reward, cost)


k = 100000  # Number of trials to simulate
n_machines = len(slot_machines_data)

for i in range(k):
    best_machine = ucb1(i, slot_machines_data)
    play_result = simulate_machine_play(best_machine)
    slot_machines_data[best_machine].append(play_result) # Update dataset after simulation

# Print the final results
machine_totals = [
    {
        'slot': len(data),
        'win': sum([trial[0] for trial in data]),
        'cost': sum([trial[1] for trial in data]),
    }
    for data in slot_machines_data
]
average_rewards = [
    (total['win'] / total['slot']) - (total['cost'] / total['slot'])
    for total in machine_totals
]

best_machine_index = average_rewards.index(max(average_rewards))

print("Average rewards for each machine:", average_rewards)
print(f"Best machine: {best_machine_index+1}")
