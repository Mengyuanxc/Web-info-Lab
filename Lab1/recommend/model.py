import torch
from torch import nn


class ThreeLayerPerceptron(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ThreeLayerPerceptron, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = self.layer3(x)
        return x

class FiveLayerPerceptron(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(FiveLayerPerceptron, self).__init__()
        self.mlp = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.mlp(x)

if __name__ == "__main__":
    input_size = 10
    hidden_size = 20
    output_size = 5
    model = FiveLayerPerceptron(input_size, hidden_size, output_size)

    # 随机生成输入数据
    input_data = torch.randn(1, input_size)

    # 前向传播计算输出
    output = model(input_data)
    print(output)

