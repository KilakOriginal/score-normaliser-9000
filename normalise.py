import numpy as np
import csv
import argparse
from copy import deepcopy

def calculateNormalisedTeamScores(scores: dict[str, dict[str, float]], higher_is_better: dict[str, bool], max_points: float = 1.0):
    '''
    Normalises the team scores between 0 and max_points using z-scores.
    Returns a dictionary where keys are team names and values are dictionaries with normalised scores.
    '''
    scores = deepcopy(scores)  # Create a copy to avoid modifying original data
    categories = scores[next(iter(scores))].keys()
    
    # Calculate mean and standard deviation for each category
    means = {category: np.mean([team_scores[category] for team_scores in scores.values()]) for category in categories}
    std_devs = {category: np.std([team_scores[category] for team_scores in scores.values()]) for category in categories}
    
    for team_scores in scores.values():
        for category, score in team_scores.items():
            mean = means[category]
            std_dev = std_devs[category]
            if std_dev == 0:
                # Avoid division by zero if all scores are the same
                team_scores[category] = max_points / 2
            else:
                # Z-score normalization between [0, max_points]
                z_score = (score - mean) / std_dev
                if higher_is_better[category]:
                    team_scores[category] = (z_score + 3) / 6 * max_points
                else:
                    team_scores[category] = (3 - z_score) / 6 * max_points  # Invert z-score before scaling

    return scores

def getTeamScores(scores: dict[str, dict[str, float]], higher_is_better: dict[str, bool], max_points: float = 1.0):
    '''
    Normalises the scores and calculates the total score for each team.
    Returns a dictionary where keys are team names and values are their total normalised scores and their absolute scores.
    '''
    normalised_scores = calculateNormalisedTeamScores(scores, higher_is_better, max_points)
    team_total_scores = {}

    for team_name, team_scores in normalised_scores.items():
        total_normalised = sum(team_scores.values())  # Sum normalised scores
        team_total_scores[team_name] = {
            'total_normalised': total_normalised,
            'absolute_scores': scores[team_name]  # Store absolute scores
        }

    # Normalize the total scores between 0 and max_points
    min_score = min(team['total_normalised'] for team in team_total_scores.values())
    max_score = max(team['total_normalised'] for team in team_total_scores.values())
    
    if max_score != min_score:
        for team_name in team_total_scores:
            team_total_scores[team_name]['total_normalised'] = (
                (team_total_scores[team_name]['total_normalised'] - min_score) / (max_score - min_score) * max_points
            )
    else:
        # If all scores are the same, assign max_points to all
        for team_name in team_total_scores:
            team_total_scores[team_name]['total_normalised'] = max_points / 2

    return team_total_scores

def read_scores(input_file: str):
    '''
    Reads input_file as CSV
    Returns the scores dictionary.
    '''
    scores = {}
    with open(input_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            team = row['team']
            scores[team] = {key: float(value) for key, value in row.items() if key != 'team'}
    return scores

def read_higher_is_better(input_file: str):
    '''
    Reads the higher_is_better CSV file
    Returns the higher_is_better dictionary.
    '''
    higher_is_better = {}
    with open(input_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task = row['task']
            higher_is_better[task] = row['higher_is_better'].strip().lower() == 'true'
    return higher_is_better

def write_csv(output_file: str, team_scores: dict):
    '''Writes team_scores to a CSV file.'''
    with open(output_file, mode='w', newline='') as file:
        absolute_keys = list(next(iter(team_scores.values()))['absolute_scores'].keys())
        fieldnames = ['team', 'total_normalised'] + absolute_keys
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for team_name, scores_data in team_scores.items():
            row = {'team': team_name, 'total_normalised': scores_data['total_normalised']}
            row.update(scores_data['absolute_scores'])
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Process team scores and normalize them.")
    parser.add_argument('input_file', type=str, help='Input CSV file with team scores')
    parser.add_argument('higher_is_better_file', type=str, help='CSV file with higher_is_better definitions')
    parser.add_argument('output_file', type=str, help='Output CSV file to save results')
    
    args = parser.parse_args()

    scores = read_scores(args.input_file)
    higher_is_better = read_higher_is_better(args.higher_is_better_file)

    team_scores = getTeamScores(scores, higher_is_better)
    
    write_csv(args.output_file, team_scores)

if __name__ == '__main__':
    main()