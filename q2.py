"""
Organized division  - The relative values of the objects in player B's basket are
smaller or equal to the relative values of the objects in player A's basket.
"""


# The full explanation is in the pdf

def isOrganized(values_A, values_B, partition_A, partition_B):
    ratioList = calculateRelative(values_A, values_B)
    player_A = [100]  # Player A starts with 100
    player_B = [0]  ## Player B starts with 0
    player_A_partition = [1] * len(values_A)
    player_B_partition = [0] * len(values_B)
    index = 0
    min_ind = None
    while player_A[-1] > player_B[-1]:
        min_ind = getMin(ratioList)
        ratioList[min_ind] = float('inf')
        player_A.append(player_A[-1] - values_A[min_ind])
        player_B.append(player_B[-1] + values_B[min_ind])
        player_A_partition[index] -= 1
        player_B_partition[index] += 1
        index += 1
    balanced_value_A = player_A[-1]
    balanced_value_B = player_B[-2]
    partition_ratio = getPartitionRatio(balanced_value_A, balanced_value_B, values_A, values_B, min_ind)
    player_A_partition[index - 1] = 1 - partition_ratio
    player_B_partition[index - 1] = partition_ratio
    if player_A_partition != partition_A or player_B_partition != partition_B:
        return checkForParetoImprovment(values_A, values_B, partition_A, partition_B)
    return True


def getPartitionRatio(balanced_value_A, balanced_value_B, value_A, value_B, index):
    # balanced_b + valueB[index]*x = balanced_A + valueA[index]*(1-x)
    # balanced_b + valueB[index]*x = balanced_A + valueA[index]-valueA[index]*x)
    # valueB[index]*x  + valueA[index]*x = balanced_A + valueA[index] -  balanced_B)
    # x = (balanced_A + valueA[index] - balanced_B )/valueB[index] + valueA[index]
    return (balanced_value_A + value_A[index] - balanced_value_B) / (value_B[index] + value_A[index])


def calculatePartition(value_A, value_B, precentage):
    return (value_A * (1 - precentage), value_B * precentage)


def getValues(values_A, values_B, partition_A, partition_B):
    player_A = []
    player_B = []
    for value, partition in zip(values_A, partition_A):
        player_A.append(value * partition)
    for value, partition in zip(values_B, partition_B):
        player_B.append(value * partition)
    return (player_A, player_B)


def checkForParetoImprovment(values_A, values_B, partition_A, partition_B):
    original_partition_values_A, original_partition_values_B = getValues(values_A, values_B, partition_A, partition_B)
    curr_index = 0
    original_partition_A = partition_A.copy()
    original_partition_B = partition_B.copy()

    ## From A to B
    while curr_index < len(values_A):
        curr_value = partition_A[curr_index]
        if curr_value != 0 and curr_value != 1:
            while partition_A[curr_index] > 0.1:
                partition_A[curr_index] -= 0.05
                partition_B[curr_index] += 0.05
                new_A, new_B = getValues(values_A, values_B, partition_A, partition_B)
                if (sum(original_partition_values_A) < sum(new_A) and sum(original_partition_values_B) <= sum(
                        new_B)) or sum(original_partition_values_A) <= sum(new_A) and sum(
                    original_partition_values_B) < sum(
                    new_B):
                    return partition_A, partition_B
            partition_A[curr_index] = curr_value
            partition_B[curr_index] = 1 - curr_value
        curr_index += 1

    ## From B to A
    curr_index = 0
    while curr_index < len(values_A):
        curr_value = original_partition_B[curr_index]
        if curr_value != 0 and curr_value != 1:
            while original_partition_B[curr_index] > 0:
                original_partition_B[curr_index] -= 0.05
                original_partition_A[curr_index] += 0.05
                new_A, new_B = getValues(values_A, values_B, original_partition_A, original_partition_B)
                if (sum(original_partition_values_A) < sum(new_A) and sum(original_partition_values_B) <= sum(
                        new_B)) or sum(original_partition_values_A) <= sum(new_A) and sum(
                    original_partition_values_B) < sum(
                    new_B):
                    return partition_A, partition_B
            partition_A[curr_index] = 1 - curr_value
            partition_B[curr_index] = curr_value
        curr_index += 1
    return "no pareto improvement"


def getMin(ratioList):
    min_value = min(ratioList)
    return ratioList.index(min_value)


def calculateRelative(values_A, values_B):
    ratioList = []
    for value1, value2 in zip(values_A, values_B):
        ratioList.append(value1 / value2)
    return ratioList


if __name__ == '__main__':
    print(isOrganized([40, 30, 20, 10], [10, 20, 30, 40], [0, 0, 1.0, 1], [1, 1, 0.0, 0]))
    print(isOrganized([15, 15, 40, 30], [40, 25, 30, 5], [1, 0, 0.4, 0.7], [0, 1, 0.6, 0.3]))
    print(isOrganized([40, 30, 20, 10], [10, 20, 30, 40], [1, 0, 0.4, 0.7], [0, 1, 0.6, 0.3]))
    print(isOrganized([20, 20, 30, 30], [40, 40, 10, 10], [1, 0.2, 0.9, 0], [0, 0.8, 0.1, 1]))
    print(isOrganized([16, 14, 35, 35], [35, 20, 15, 30], [0.5, 0.3, 1.0, 0], [0.5, 0.7, 0.0, 1]))
    print(isOrganized([50, 30, 15, 5], [5, 15, 30, 50], [0, 0, 1.0, 1], [1, 1, 0.0, 0]))

