import pickle
import warnings
import pandas as pd

golfers = pd.read_csv("golfer_solution.csv", index_col=0)
golfers.index = [int(name.lstrip("Player ")) - 1 for name in golfers.index]
golfers.columns = [int(name.lstrip("Round ")) - 1 for name in golfers.columns]

class Groups:
    def __init__(self, num_players, num_groups):
        self.was_first = [False] * num_players
        self.num_groups = num_groups
        self.results = []

    def add_round(self, allocation):
        self.results.append([[] for _ in range(self.num_groups)])
        for player, group in enumerate(allocation):
            group_id = int(group.lstrip("Group ")) - 1
            if self.was_first[player]:
                self.results[-1][group_id].append(player)
            else:
                self.results[-1][group_id].insert(0, player)
        for group in range(len(self.results[-1])):
            first_in_group = self.results[-1][group][0]
            if self.was_first[self.results[-1][group][0]]:
                warnings.warn(f"Player {first_in_group} was first multiple times")
            self.was_first[first_in_group] = True

    def adjust_indices(self):
        for round in range(len(self.results)):
            for group in range(len(self.results[round])):
                for player in range(len(self.results[round][group])):
                    self.results[round][group][player] = self.results[round][group][player] + 1

groups = Groups(len(golfers), 6)
for round in golfers.columns:
    groups.add_round(golfers.loc[:, round])
groups.adjust_indices()

with open("group_matrices.pkl", "wb") as f:
    pickle.dump(groups.results, f)
