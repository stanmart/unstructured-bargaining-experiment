# Create group matrices for reshuffling

Make sure that 
- players within the same matching group have as little overlap with other players across rounds as possible
- everyone gets a chance at being the first player (as much as possible)(in the current setting, everyone is the first player twice)

## How it works

 - The initial group allocation for one sample matching group is from [goodenoughgolfers.com/](https://goodenoughgolfers.com/ with 2 groups, 3 people per group and 6 number of rounds). The output from the website is `golfer_solution.csv`
 - The jupyter notebook `create_group_matrices.ipynb` creates the group matrices for all matching groups within a session. It also reshuffles the players within groups so that everyone gets an equal chance at being the first player. Its output is a list(rounds) of lists (groups) of integers(player ids): `group_matrices.pkl`
 - The group matrices are considered to be fixed, and are therefore committed to the repo. This readme file and notebook are only here for documentation purposes.
