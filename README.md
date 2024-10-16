# Score Normaliser 9000
This is a simple python script for normalising scores.

The script expects a file path to the input csv file, a path to the higher-is-better csv file and the path to the output csv file as arguments.

The csv files should have the following structure:

```
team,task1,task2,task3,task4
team1,40,20,50,150
team2,20,20,40,200
team3,30,10,30,200
```

```
task,higher_is_better
task1,True
task2,True
task3,False
task4,True
```

Example: `python normalise.py input.csv higher_is_better.csv output.csv`