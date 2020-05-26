from math import sqrt
import sys
import copy


def get_hackerrank_input():

    data_points = list()
    number_of_clusters = 0
    first_line = True
    for line in sys.stdin.readlines():
        if first_line:
            number_of_clusters = int(line.strip().split()[1])
            first_line = False
        else:
            data_point = list()
            coordinates = line.strip().split()
            for coordinate in coordinates:
                data_point.append(float(coordinate))
            data_points.append(data_point)

    return data_points, number_of_clusters


def get_input():
    data_points = [[8.98320053625, -2.08946304844], [2.61615632899, 9.46426282022],
                   [1.60822068547, 8.29785986996], [8.64957587261, -0.882595891607],
                   [1.01364234605, 10.0300852081], [1.49172651098, 8.68816850944],
                   [7.95531802235, -1.96381815529], [0.527763520075, 9.22731148332],
                   [6.91660822453, -3.2344537134], [6.48286208351, -0.605353440895]]
    number_of_clusters = 2
    return data_points, number_of_clusters



def euclidean_distance(pointA, pointB):
    distance = float(0.0)
    for index in range(len(pointA)):
        distance += (pointA[index] - pointB[index])**2
    return sqrt(distance)


def create_proximity_matrix(data_points):

    proximity_matrix = list()
    for which_row in range(len(data_points)):
        row_matrix = [float("inf")] * len(data_points)
        for which_column in range(which_row):
            row_value = data_points[which_row]
            column_value = data_points[which_column]
            distance = euclidean_distance(row_value, column_value)
            row_matrix[which_column] = distance
        proximity_matrix.append(row_matrix)

    return proximity_matrix


def find_matrix_minimum(proximity_matrix):
    minimum_distance = float("inf")
    minimum_distance_at_row = None
    minimum_distance_at_column = None
    for which_row in range(len(proximity_matrix)):
        for which_column in range(which_row):

            # Tie breaking condition mentioned in HW
            if minimum_distance == proximity_matrix[which_row][which_column]:
                if not ((min(minimum_distance_at_row, minimum_distance_at_column) == min(which_row, which_column)) and (max(minimum_distance_at_row, minimum_distance_at_column) < max(which_row, which_column))):
                    minimum_distance = proximity_matrix[which_row][which_column]
                    minimum_distance_at_row = which_row
                    minimum_distance_at_column = which_column
            elif minimum_distance > proximity_matrix[which_row][which_column]:
                minimum_distance = proximity_matrix[which_row][which_column]
                minimum_distance_at_row = which_row
                minimum_distance_at_column = which_column

    return min(minimum_distance_at_row, minimum_distance_at_column), max(minimum_distance_at_row, minimum_distance_at_column)


def update_proximity_matrix(proximity_matrix, merge_row, merge_column):

    previous_proximity_matrix = copy.deepcopy(proximity_matrix)

    merge_row_values = proximity_matrix[merge_row]
    merge_column_values = proximity_matrix[merge_column]

    # Update merge row values
    add_new_row = [float("inf")]*len(proximity_matrix)
    for which_column in range(merge_row):
        replacing_value = min(merge_row_values[which_column], merge_column_values[which_column])
        add_new_row[which_column] = replacing_value
    # Delete merge row and replace with revised values
    del proximity_matrix[merge_row]
    proximity_matrix.insert(merge_row, add_new_row)

    # Update column values
    for which_row in range(len(previous_proximity_matrix)):
        if which_row > merge_row:
            minimum_of_matrix_similarity = min(previous_proximity_matrix[merge_column][which_row], previous_proximity_matrix[which_row][merge_column])
            replacing_value = min(previous_proximity_matrix[which_row][merge_row], minimum_of_matrix_similarity)
            proximity_matrix[which_row][merge_row] = replacing_value
        # Delete the merge column in each row
        del proximity_matrix[which_row][merge_column]

    # Delete entire merge row; here merge column which is actually one of the row
    del proximity_matrix[merge_column]

    return proximity_matrix


def agnes(data_points, desired_number_of_clusters):

    cluster_ids = list()
    for which_point in range(len(data_points)):
        a_cluster = list()
        a_cluster.append(which_point)
        cluster_ids.append(a_cluster)

    number_of_clusters = len(cluster_ids)

    proximity_matrix = create_proximity_matrix(data_points)

    while number_of_clusters > desired_number_of_clusters:

        row, column = find_matrix_minimum(proximity_matrix=proximity_matrix)

        proximity_matrix = update_proximity_matrix(proximity_matrix=proximity_matrix,merge_row=row, merge_column=column)

        cluster_ids = update_cluster_ids(cluster_ids, row, column)

        number_of_clusters = len(cluster_ids)

    datapoints_to_cluster_mapping = dict()
    for which_cluster, current_cluster in enumerate(cluster_ids):
        for which_point in current_cluster:
            datapoints_to_cluster_mapping[which_point] = current_cluster[0]

    predicted_labels = list()
    for key in sorted(datapoints_to_cluster_mapping.keys()):
        predicted_labels.append(datapoints_to_cluster_mapping[key])
        # Printing output here!
        print (datapoints_to_cluster_mapping[key])

    return predicted_labels


def update_cluster_ids(cluster_ids, row, column):

    # We know than row value < column value
    cluster_A = cluster_ids[row]
    cluster_B = cluster_ids[column]
    combine_cluster = list()

    for cluster_id in cluster_A:
        combine_cluster.append(cluster_id)
    for cluster_id in cluster_B:
        combine_cluster.append(cluster_id)

    cluster_ids.pop(row)
    cluster_ids.pop(column-1)
    cluster_ids.insert(row,combine_cluster)

    return cluster_ids


def read_testcase_input(sourceFile):
    datapoints = list()
    with open(sourceFile, 'r') as file:
        for line in file:
            point = list()
            for coordinate in line.split():
                point.append(float(coordinate))
            datapoints.append(point)

    number_of_clusters = int(datapoints[0][1])
    datapoints = datapoints[1:]

    return datapoints, number_of_clusters


def read_testcase_output(sourceFile):

    labels = list()
    with open(sourceFile, 'r') as file:
        for line in file:
            labels.append(int(line.strip()))

    return labels


def check_accuracy(truth, predicted):

    correct_answers = list()
    wrong_answers = list()
    for which_label in range(len(truth)):
        point = list()
        point.append(which_label)
        point.append(truth[which_label])
        point.append(predicted[which_label])

        if truth[which_label] == predicted[which_label]:
            correct_answers.append(point)
        else:
            wrong_answers.append(point)

    accuracy = len(correct_answers)/len(truth) * 100

    return accuracy


if __name__ == '__main__':

    # Extra test case
    # data_points, desired_number_of_clusters = read_testcase_input(sourceFile="AGNES_testcase.txt")
    # true_labels = read_testcase_output(sourceFile="AGNES_testcase_output.txt")

    data_points, desired_number_of_clusters = get_input()
    # data_points, desired_number_of_clusters = get_hackerrank_input()

    # AGNES
    predicted_output_labels = agnes(data_points, desired_number_of_clusters)

    # Accuracy; printing stuff
    # check_accuracy(truth=true_labels, predicted=predicted_output_labels)