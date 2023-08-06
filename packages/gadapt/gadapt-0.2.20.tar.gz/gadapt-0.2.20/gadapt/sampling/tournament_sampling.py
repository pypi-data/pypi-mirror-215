import random
from typing import List
from gadapt.ga_model.ranking_model import RankingModel
from gadapt.sampling.base_sampling import BaseSampling

class TournamentSampling(BaseSampling):

    """
    "Tournament" algorithm for extracting a sample from the population.
    """

    def __init__(self, group_size = None) -> None:
        super().__init__()
        self.group_size = group_size
    
    def prepare_sample(self, lst: List[RankingModel]) -> List[RankingModel]:
        ls = []
        ls = sorted(lst, key=self.sort_key)
        groups = self._get_groups(ls)
        self._play_tournament(groups, self.sort_key)
        return self._make_ranking(groups)
    
    def _get_groups(self, lst: List[RankingModel]) -> List[List[RankingModel]]:
        size = len(lst)
        ls = [rm for rm in lst]
        if self.group_size is None or self.group_size > len(ls):
            self.group_size = self._calculate_group_size(ls)
        num_of_groups = size // self.group_size
        #if size % self.group_size > 0:
        #    num_of_groups += 1
        groups = []
        for i in range(num_of_groups):
            l: list[RankingModel] = []
            groups.append(l)
        for i in range(self.group_size):
            for g in groups:
                random_index = random.randint(0, len(ls)-1)
                element = ls.pop(random_index)
                g.append(element)
                if len(ls) == 0:
                    break
            if len(ls) == 0:
                break
        if len(ls) > 0:
            groups.append(ls)
        return groups
    
    def _calculate_group_size(self, ls: List[RankingModel]):
        size = len(ls)
        if size <= 3:
            return len(ls)
        group_size = 2
        if size >= 9:
            group_size += 1
        if size >= 12:
            group_size += 1
        return group_size

    def _play_tournament(self, groups: List[List[RankingModel]], sort_key):
        for g in groups:
            g.sort(key=sort_key)

    def _make_ranking(self,  groups: List[List[RankingModel]]):
        rank = 0
        members_for_action = []
        number_of_groups = len(groups)
        while rank < self.max_num:
            number_of_empty_groups = 0
            for g in groups:
                if len(g) == 0:
                    number_of_empty_groups += 1
                    continue
                element = g.pop(0)
                element.rank = rank
                members_for_action.append(element)
                rank += 1
            if number_of_empty_groups == number_of_groups:
                break
        return members_for_action[:self.max_num]
