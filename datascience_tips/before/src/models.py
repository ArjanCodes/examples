import torch


class LinearNet(torch.nn.Module):
    def __init__(self):
        super(LinearNet, self).__init__()

        self.flatten = torch.nn.Flatten()
        self.linear1 = torch.nn.Linear(in_features=28 * 28, out_features=32)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(in_features=32, out_features=10)
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x: torch.Tensor):
        x = self.flatten(x)
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x = self.softmax(x)
        return x
