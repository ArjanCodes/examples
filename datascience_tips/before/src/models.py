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


class ConvNet(torch.nn.Module):

    def __init__(self):
        super(ConvNet, self).__init__()

        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1)
        self.relu1 = torch.nn.ReLU()
        self.pool1 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)
        self.relu2 = torch.nn.ReLU()
        self.pool2 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv3 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu3 = torch.nn.ReLU()
        self.pool3 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv4 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu4 = torch.nn.ReLU()
        self.pool4 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv5 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu5 = torch.nn.ReLU()
        self.pool5 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv6 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu6 = torch.nn.ReLU()
        self.pool6 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv7 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu7 = torch.nn.ReLU()
        self.pool7 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv8 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu8 = torch.nn.ReLU()
        self.pool8 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.conv9 = torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.relu9 = torch.nn.ReLU()
        self.pool9 = torch.nn.MaxPool2d(kernel_size=2, stride=1)

        self.linear1 = torch.nn.Linear(in_features=64 * 1 * 1, out_features=10)

        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x: torch.Tensor):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.pool3(self.relu3(self.conv3(x)))
        x = self.pool4(self.relu4(self.conv4(x)))
        x = self.pool5(self.relu5(self.conv5(x)))
        x = self.pool6(self.relu6(self.conv6(x)))
        x = self.pool7(self.relu7(self.conv7(x)))
        x = self.pool8(self.relu8(self.conv8(x)))
        x = self.pool9(self.relu9(self.conv9(x)))
        x = x.squeeze(-1).squeeze(-1)
        x = self.linear1(x)
        x = self.softmax(x)
        return x
