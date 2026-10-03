import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import beta
import multiprocessing as mp
# import logging

# # Set up the logger
# logging.basicConfig(level=logging.INFO)

# Load the movies data with 'latin1' encoding
movies = pd.read_csv('movies.dat', sep='::', names=['MovieID', 'Title', 'Genres'], engine='python', encoding='latin1')

# Load the ratings data with 'latin1' encoding
ratings = pd.read_csv('ratings.dat', sep='::', names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python', encoding='latin1')

# Load the users data with 'latin1' encoding
users = pd.read_csv('users.dat', sep='::', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python', encoding='latin1')

# Merge the ratings and users DataFrames
merged = pd.merge(pd.merge(ratings, users), movies)

# Split the genres column and create a new entry for each genre
merged = merged.assign(Genres = merged['Genres'].str.split('|')).explode('Genres')

# get the unique genres
genres = merged['Genres'].unique()

# Map each genre to an index
genre_to_index = {genre: i for i, genre in enumerate(genres)}

# Initialize the counts and averages
counts = {genre: 0 for genre in genres}
averages = {genre: 0 for genre in genres}

# Initialize the parameters of the Beta distribution for each arm
alpha = {genre: 1 for genre in genres}
beta = {genre: 1 for genre in genres}

# Calculate the frequency of each rating for each genre
rating_freq = merged.groupby('Genres')['Rating'].value_counts(normalize=True)

# Pre-calculate the ratings and probabilities arrays for each genre
rating_dist = {genre: (rating_freq[genre].index, rating_freq[genre].values)
               for genre in rating_freq.index.levels[0]}

def pull_arm(chosen_genre):
    # Check if there are any movies of this genre left
    if chosen_genre not in rating_dist:
        return 0

    # Sample a rating from the pre-calculated distribution
    ratings, probabilities = rating_dist[chosen_genre]
    reward = ratings[np.random.multinomial(1, probabilities).argmax()]

    return reward

## Multi-processing code for running multiple experiments in parallel

## Code for UCB

def run_single_experiment_UCB(params):

    # # Log the start of the experiment
    # logging.info(f'Starting experiment {experiment}')
    n, num_arms, experiment = params

    B = 4  # Constant for adjusting the degree of exploration

    cumulative_regret_UCB = np.zeros(n+1)

    # Reset the counts, averages, and cumulative regret at the start of each experiment
    counts = {genre: 0 for genre in genres}
    averages = {genre: 0 for genre in genres}

    for t in range(1, n+1):
        # Calculate the UCB index for each arm
        ucb_indices = {genre: averages[genre] + B * np.sqrt((4 * np.log(n)) / (1 + counts[genre])) for genre in genres}

        # Choose the arm with the highest UCB index
        chosen_arm = max(ucb_indices, key=ucb_indices.get)

        # Pull the chosen arm and get the reward
        reward = pull_arm(chosen_arm)

        # Update the counts and averages
        counts[chosen_arm] += 1
        averages[chosen_arm] = ((averages[chosen_arm] * (counts[chosen_arm] - 1)) + reward) / counts[chosen_arm]

        # Calculate the regret
        optimal_reward = max(averages.values())
        regret = optimal_reward - reward

        # Store the cumulative regret
        cumulative_regret_UCB[t] = cumulative_regret_UCB[t-1] + regret

    return cumulative_regret_UCB

def run_experiment_UCB(n, num_experiments, num_arms):
    with mp.Pool(mp.cpu_count()) as pool:  # Use 20 processes
        results_UCB = pool.map(run_single_experiment_UCB, [(n, num_arms, experiment) for experiment in range(num_experiments)])

    cumulative_regret_UCB = np.array(results_UCB)
    avg_regret_UCB = np.mean(cumulative_regret_UCB, axis=0)
    std_dev_UCB = np.std(cumulative_regret_UCB, axis=0)

    return cumulative_regret_UCB, avg_regret_UCB, std_dev_UCB

## Code for TS

def run_single_experiment_TS(params):
    n, num_arms, experiment = params
    # Initialize the cumulative regret
    cumulative_regret_TS = np.zeros((n))

    # Run the Thompson Sampling algorithm
    # Reset the counts, averages, and cumulative regret at the start of each experiment
    counts = {genre: 0 for genre in genres}
    averages = {genre: 0 for genre in genres}

    # Initialize by choosing each arm once
    for t in range(num_arms):
        chosen_arm = genres[t]
        reward = pull_arm(chosen_arm)
        counts[chosen_arm] += 1
        averages[chosen_arm] = reward

    # Update the distributions and choose the arm with the highest sample
    for t in range(num_arms, n):
        samples = {genre: np.random.normal(loc=averages[genre], scale=np.sqrt(4/(counts[genre]))) for genre in genres}
        chosen_arm = max(samples, key=samples.get)
        reward = pull_arm(chosen_arm)
        counts[chosen_arm] += 1
        averages[chosen_arm] = ((averages[chosen_arm] * (counts[chosen_arm] - 1)) + reward) / counts[chosen_arm]

        # Calculate the regret
        optimal_reward = max(averages.values())
        regret = optimal_reward - reward

        # Store the cumulative regret
        cumulative_regret_TS[t] = cumulative_regret_TS[t-1] + regret
    
    return cumulative_regret_TS

def run_experiment_TS(n, num_experiments, num_arms):
    with mp.Pool(mp.cpu_count()) as pool:  # Use 20 processes
        results_TS = pool.map(run_single_experiment_TS, [(n,num_arms, experiment) for experiment in range(num_experiments)])

    cumulative_regret_TS = np.array(results_TS)
    avg_regret_TS = np.mean(cumulative_regret_TS, axis=0)
    std_dev_TS = np.std(cumulative_regret_TS, axis=0)

    return cumulative_regret_TS, avg_regret_TS, std_dev_TS

## code for ETC

def run_single_experiment_ETC(params):
    n, num_arms, experiment = params
    # Set the length of the exploration phase
    m = n // (10 * num_arms) # Use integer division to ensure m is an integer

    cumulative_regret_ETC = np.zeros((n))

    # Reset the counts, averages, and cumulative regret at the start of each experiment
    counts = {genre: 0 for genre in genres}
    averages = {genre: 0 for genre in genres}

    # Exploration phase
    for t in range(m * num_arms):
        chosen_arm = genres[t % num_arms]  # Cycle through the arms
        reward = pull_arm(chosen_arm)
        counts[chosen_arm] += 1
        averages[chosen_arm] = ((averages[chosen_arm] * (counts[chosen_arm] - 1)) + reward) / counts[chosen_arm]

        # Calculate the regret
        optimal_reward = max(averages.values())
        regret = optimal_reward - reward

        # Store the cumulative regret
        cumulative_regret_ETC[t] = (cumulative_regret_ETC[t-1] if t > 0 else 0) + regret

    # Exploitation phase
    best_arm = max(averages, key=averages.get)
    for t in range(m * num_arms, n):
        reward = pull_arm(best_arm)
        counts[best_arm] += 1
        averages[best_arm] = ((averages[best_arm] * (counts[best_arm] - 1)) + reward) / counts[best_arm]

        # Calculate the regret
        optimal_reward = max(averages.values())
        regret = optimal_reward - reward

        # Store the cumulative regret
        cumulative_regret_ETC[t] = cumulative_regret_ETC[t-1] + regret
    
    return cumulative_regret_ETC

def run_experiment_ETC(n, num_experiments, num_arms):
    with mp.Pool(mp.cpu_count()) as pool:  # Use 20 processes
        results_ETC = pool.map(run_single_experiment_ETC, [(n, num_arms, experiment) for experiment in range(num_experiments)])

    cumulative_regret_ETC = np.array(results_ETC)
    avg_regret_ETC = np.mean(cumulative_regret_ETC, axis=0)
    std_dev_ETC = np.std(cumulative_regret_ETC, axis=0)

    return cumulative_regret_ETC, avg_regret_ETC, std_dev_ETC

def plot_graph(avg_regrets, std_devs, title):

    # Define marker shapes for each algorithm
    # markers = {
    #     'UCB': 'o',
    #     'ETC': 's',  # square
    #     'TS': '^',  # triangle
    # }

    # colors = {
    #     'UCB': 'blue',
    #     'ETC': 'green',
    #     'TS': 'red'
    # }
    # Plot the average regret for each algorithm with error bars
    for algorithm in avg_regrets.keys():
        plt.errorbar(range(len(avg_regrets[algorithm])), avg_regrets[algorithm], yerr=std_devs[algorithm], label=algorithm, elinewidth= 0.1, alpha=0.7, markersize=4, capsize=2, capthick= 0.5)

    plt.xlabel('Time Steps')
    plt.ylabel('Average Regret')
    plt.title(title)  # Title of the plot
    plt.legend()
    plt.show()

def main():
    np.random.seed(122)
    n = 500
    num_experiments = 100
    num_arms = len(genres)

    cumulative_regret_UCB, avg_regret_UCB, std_dev_UCB = run_experiment_UCB(n, num_experiments, num_arms)
    cumulative_regret_TS, avg_regret_TS, std_dev_TS = run_experiment_TS(n, num_experiments, num_arms)
    cumulative_regret_ETC, avg_regret_ETC, std_dev_ETC = run_experiment_ETC(n, num_experiments, num_arms)
    avg_regret: dict = {'UCB': avg_regret_UCB, 'TS': avg_regret_TS, 'ETC': avg_regret_ETC}
    std_devs = {'UCB': std_dev_UCB, 'TS': std_dev_TS, 'ETC': std_dev_ETC}
    plot_graph(avg_regret, std_devs, 'Average Regret vs Time Steps')
    

if __name__ == '__main__':
    main()



