import torch


class LinearNet(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.network = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=28 * 28, out_features=32),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=32, out_features=10),
            torch.nn.Softmax(dim=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
