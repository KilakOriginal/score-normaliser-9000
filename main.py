import numpy as np
from copy import deepcopy

def calculateNormalisedTeamScores(scores: dict[str, dict[str, float]], higher_is_better: dict[str, bool], max_points: float = 10.0):
    '''
    Normalises the team scores between 0 and max_points using z-scores.
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
                team_scores[category] = max_points / 2  # Assign middle score if no variation
            else:
                # Z-score normalization
                z_score = (score - mean) / std_dev
                if higher_is_better[category]:
                    team_scores[category] = (z_score + 3) / 6 * max_points  # Scale z-score to [0, max_points]
                else:
                    team_scores[category] = (3 - z_score) / 6 * max_points  # Invert and scale z-score to [0, max_points]

    return scores

def getTeamScores(scores: dict[str, dict[str, float]], higher_is_better: dict[str, bool], max_points: float = 10.0):
    '''
    Normalises the scores and calculates the total score for each team.
    Returns a dictionary where keys are team names and values are their total scores.
    '''
    normalised_scores = calculateNormalisedTeamScores(scores, higher_is_better, max_points)
    team_total_scores = {}

    for team_name, team_scores in normalised_scores.items():
        team_total_scores[team_name] = sum(team_scores.values())  # Sum team scores

    # Normalize the total scores between 0 and max_points
    min_score = min(team_total_scores.values())
    max_score = max(team_total_scores.values())
    if max_score != min_score:
        for team_name in team_total_scores:
            team_total_scores[team_name] = (team_total_scores[team_name] - min_score) / (max_score - min_score) * max_points
    else:
        # If all scores are the same, assign max_points to all
        for team_name in team_total_scores:
            team_total_scores[team_name] = max_points / 2

    return team_total_scores

def main():
    scores = {
        'team1': {'station1': 40, 'station2': 20, 'station3': 50, 'station4': 150},
        'team2': {'station1': 20, 'station2': 20, 'station3': 40, 'station4': 200},
        'team3': {'station1': 30, 'station2': 10, 'station3': 30, 'station4': 200},
    }
    higher_is_better = {'station1': False, 'station2': False, 'station3': False, 'station4': True}
    
    team_scores = getTeamScores(scores, higher_is_better, max_points=10)
    print(team_scores)

if __name__ == '__main__':
    main()