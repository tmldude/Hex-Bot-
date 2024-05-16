from multiprocessing import Pool, cpu_count, freeze_support

import os
import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from DataProcessing import ChessDataset

class ChessCNN(nn.Module):
    def __init__(self):
        super(ChessCNN, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 1)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_chess_cnn(model, data_loader, optimizer, device, epochs=10):
    criterion = nn.MSELoss()
    model.to(device)  
    
    for epoch in range(epochs):
        running_loss = 0.0
        for positions, evaluations in data_loader:
            positions, evaluations = positions.to(device), evaluations.to(device)  
            outputs = model(positions)
            loss = criterion(outputs, evaluations.unsqueeze(1))
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        avg_loss = running_loss / len(data_loader)
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}, Avrg_Loss: {avg_loss}')


if __name__ == "__main__":
    freeze_support()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f'Using device: {device}')

    engine_path = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"
    model_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_cnn_model.pth"
    optimizer_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_cnn_optimizer.pth"

    json_file = "chess_from_pgn_50000.json"
    dataset = ChessDataset(json_file)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    model = ChessCNN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.load_state_dict(torch.load(model_path))
    if os.path.exists(optimizer_path):
        optimizer.load_state_dict(torch.load(optimizer_path))

    train_chess_cnn(model, data_loader, optimizer, device, epochs=10)

    torch.save(model.state_dict(), model_path)
    torch.save(optimizer.state_dict(), optimizer_path)



