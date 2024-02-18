#Author: Prisha
#Date: 02/01/24
#Purpose: To create a DES environment for a clinic to cal. wait times of patients that are generated based on data analysis of the DHMC incoming patients


import simpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


Q = 0
#Slots per day for each provider
A = 2
B = 3
C = 1

class Provider:
    def __init__(self, capacity, env):
        self.capacity = capacity
        self.provider = simpy.Resource(env, capacity=self.capacity)
        self.PAT_WAIT = []


class Center:
    def __init__(self, env):
        self.env = env
        self.provider1 = Provider(A, env)
        self.provider2 = Provider(B, env)
        self.provider3 = Provider(C, env)

        capacities = [len(self.provider1.PAT_WAIT), len(self.provider2.PAT_WAIT), len(self.provider3.PAT_WAIT)]
        max_capacity = min(capacities)

        if max_capacity == self.provider1.capacity:
            self.first = self.provider1
        elif max_capacity == self.provider2.capacity:
            self.first = self.provider2
        else:
            self.first = self.provider3

        self.wait_times = []

def patient(name, env, center):
    arrival = env.now
    global Q
    Q += 1


    print(f'Patient {name} tries to book appointment at {arrival}')
    center.first.PAT_WAIT.append(name)
    with center.first.provider.request() as req:

        yield req  # Request the resource

        if center.first.capacity < Q - len(center.first.PAT_WAIT):  # Check if there are no available slots
            print("No appointments for the day")
            yield env.timeout(24)  # Release the resource
            Q = 0



        wait_time = env.now - arrival
        center.wait_times.append(wait_time)
        print(f'Patient {name} gets appointment after {wait_time} hours of waiting')
        # center.first.get(1)
        yield env.timeout(0.5)  # 30 mins
        center.first.PAT_WAIT.remove(name)
        print(f'Patient {name} completes visit at {env.now}')


#Patient Generator

df = pd.read_csv('Data.csv')
centers = df['Center'].unique()
df1 = df[df["Group1"] == 'New']


def patient_generator(i):



    df2 = df1[df1["Center"] == i]

    grouped = df2.groupby('AppointmentEntryDate')
    sizes = grouped.size()

    group_sizes_df = sizes.reset_index(name='No. Of Patients')

    frequency_table = group_sizes_df['No. Of Patients'].value_counts().reset_index()

    # Calculate the total count
    total_count = frequency_table['count'].sum()

    # Divide each count by the total count to get the probability
    frequency_table['probability'] = frequency_table['count'] / total_count

    frequency_table_sorted = frequency_table.sort_values(by='probability')


    # Generate a random number between 0 and 1 for sampling
    random_number = np.random.rand()

    # Cumulative sum of probabilities to use for sampling
    cumulative_probabilities = frequency_table_sorted['probability'].cumsum()

    # Find the index where the cumulative probability exceeds the random number
    index = (cumulative_probabilities >= random_number).idxmax()

    # The corresponding 'No. Of Patients' value for that index
    patients_assigned = frequency_table_sorted.loc[index, 'No. Of Patients']

    print("Random number:", random_number)
    print("Assigned No. Of Patients:", patients_assigned)
    return patients_assigned



def patient_gen(env, clinic):
    x = patient_generator('IBD')
    for i in range(x):
        env.process(patient(i, env, clinic))
        yield env.timeout(8/x)
    yield env.timeout(16)

for i in range(1):
    env = simpy.Environment()
    center = Center(env)
    patient_g = env.process(patient_gen(env, center))
    env.run(until=2400)
    print(center.wait_times)


# Analyze the wait times
def analyze_wait_times(wait_times):
    average_wait_time = sum(wait_times) / len(wait_times)

    plt.hist(wait_times, bins=20, edgecolor='black')
    plt.title('Wait Time Histogram')
    plt.xlabel('Wait Time (hours)')
    plt.ylabel('Frequency')
    plt.show()

    print(f'Average Wait Time: {average_wait_time:.2f} hours')

analyze_wait_times(center.wait_times)





