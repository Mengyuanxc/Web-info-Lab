import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Data(Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        user = row[0].astype('float32')
        item = row[1].astype('float32')
        rating = row['Rate'].astype('float32')
        input = torch.tensor([user, item])
        return input, rating

    def __len__(self):
        return len(self.data)

#电影的dataset和dataloader
Movie_dir = "./data/movie_score.csv"
Movie_data = pd.read_csv(Movie_dir)
Movie_train_data, Movie_test_data = train_test_split(Movie_data, test_size=0.5, random_state=10)

Movie_train_dataset = Data(Movie_train_data)

Movie_test_dataset = Data(Movie_test_data)

#返回顺序：User_ID, Movie_ID, Rating
Movie_train_dataloader = DataLoader(Movie_train_dataset, batch_size=4096, shuffle=True, drop_last = True)
Movie_test_dataloader = DataLoader(Movie_test_dataset, batch_size=4096, shuffle=False, drop_last = True)



Book_dir = "./data/book_score.csv"
Book_data = pd.read_csv(Book_dir)
Book_train_data, Book_test_data = train_test_split(Book_data, test_size=0.5, random_state=10)

Book_train_dataset = Data(Book_train_data)

Book_test_dataset = Data(Book_test_data)

#返回顺序：User_ID, Book_ID, Rating
Book_train_dataloader = DataLoader(Book_train_dataset, batch_size=4096, shuffle=True, drop_last = True)
Book_test_dataloader = DataLoader(Book_test_dataset, batch_size=4096, shuffle=False, drop_last = True)


print("Movie Recommendation")
train_data_size = len(Movie_train_data)
test_data_size = len(Movie_test_data)
print("训练数据集长度为：{}".format(train_data_size))
print("测试数据集长度为：{}".format(test_data_size))


model = model.ThreeLayerPerceptron(2, 10, 6).to(device)

loss_function = torch.nn.CrossEntropyLoss().to(device)

learning_rate = 1e-1
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

epoch = 20

total_train_step = 0
total_test_step = 0

for i in range(epoch):
    print("第{}轮训练开始".format(i + 1))
    for data in Movie_train_dataloader:
        inputs, rating = data
        inputs = inputs.cuda()
        rating = rating.cuda()
        output = model(inputs)
        loss = loss_function(output, rating.long())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step += 1
        if(total_train_step % 100 == 0):
            print("训练次数：{}，Loss：{}".format(total_train_step, loss))

    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in Movie_test_dataloader:
            inputs, rating = data
            inputs = inputs.cuda()
            rating = rating.cuda()
            output = model(inputs)
            loss = loss_function(output, rating.long())
            total_test_loss = total_test_loss + loss
            accuracy = (output.argmax(1) == rating).sum()
            total_accuracy += accuracy
    print("整体测试集上的Loss：{}".format(total_test_loss))
    print("整体测试集上的正确率：{}".format(total_accuracy / test_data_size))



