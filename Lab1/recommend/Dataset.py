import random
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class Data(Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        user = row[0]
        item = row[1]
        rating = row['Rate'].astype('float32')
        return user, item, rating

#电影的dataset和dataloader
Movie_dir = "./data/movie_score.csv"
Movie_data = pd.read_csv(Movie_dir)
Movie_train_data, Movie_test_data = train_test_split(Movie_data, test_size=0.5, random_state=10)

Movie_train_dataset = Data(Movie_train_data)

Movie_test_dataset = Data(Movie_test_data)

#返回顺序：User_ID, Movie_ID, Rating, Embedding
Movie_train_dataloader = DataLoader(Movie_train_dataset, batch_size=4096, shuffle=True, drop_last = True)
Movie_test_dataloader = DataLoader(Movie_test_dataset, batch_size=4096, shuffle=False, drop_last = True)



Book_dir = "./data/book_score.csv"
Book_data = pd.read_csv(Book_dir)
Book_train_data, Book_test_data = train_test_split(Book_data, test_size=0.5, random_state=10)

Book_train_dataset = Data(Book_train_data)

Book_test_dataset = Data(Book_test_data)

#返回顺序：User_ID, Book_ID, Rating, Embedding
Book_train_dataloader = DataLoader(Book_train_dataset, batch_size=4096, shuffle=True, drop_last = True)
Book_test_dataloader = DataLoader(Book_test_dataset, batch_size=4096, shuffle=False, drop_last = True)

