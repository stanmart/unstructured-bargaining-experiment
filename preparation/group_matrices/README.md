# Create group matrices for reshuffling

Make sure that

 - no players are in the same group more than once (as much as possible)
 - everyone gets a chance at being the first player (as much as possible)

## How it works

 - The initial group allocation is from [goodenoughgolfers.com/](https://goodenoughgolfers.com/). The output from the website is `golfer_solution.csv`
 - The script `create_group_matrices.py` reshuffles the players within groups so that everyone gets a chance at being the first player. It's output is a list(rounds) of lists (groups) of integers (player ids): `group_matrices.pkl`
 - The group matrices are considered to be fixed, and are therefore committed to the repo. This readme file and Python script is only here for documentation purposes.
