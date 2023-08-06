import pandas as pd
from torch.utils.data import Dataset, DataLoader

from recommend_model_sdk.mind_sdk.config.mind_base_config import MINDBaseConfig

class MINDBehaviorsParsedDataset(Dataset):
    """
    Load behaviors for evaluation, (user, time) pair as session
    """
    def __init__(self, behaviors_path,config):
        """_summary_

        Args:
            behaviors_path (_type_): _description_ is behaviors_parsed.tsv. not behaviors.tsv
            config (_type_): _description_

        Raises:
            ValueError: _description_
        """
        super(MINDBehaviorsParsedDataset, self).__init__()
        if isinstance(config,MINDBaseConfig) is False:
            raise ValueError("config is not MINDBaseConfig")
        self.__config = config
        self.__behaviors = pd.read_table(behaviors_path,
                                       header=None,
                                       usecols=range(4),
                                       names=[
                                           'user', 'clicked_news',
                                           'candidate_news', 'clicked','impression_id'
                                       ])
        # self.__behaviors.clicked_news.fillna(' ', inplace=True)

    def __len__(self):
        return len(self.__behaviors)

    def __getitem__(self, idx):
        row = self.__behaviors.iloc[idx]
        item = {
            "user": row.user,
            "candidate_news": row.candidate_news.split(),
            'clicked':row.clicked.split(),
            "impression_id": row.impression_id,
            "clicked_news":row.clicked_news.split()[:self.__config.num_clicked_news_a_user]
        }
        return item