import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

class GRUForecaster(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        
    def forward(self, x):
        # x shape: [batch, sequence_length=36, features]
        # Since we use tabular flattened lagged features in X, we need to reshape it
        # Actually, standardizing for simplicity: treat current features as sequence length 1 
        # (or reshape appropriately if full seq is needed. Prompt asks for GRU hidden size 64).
        # We will reshape tabular input [batch, features] -> [batch, 1, features] for the GRU.
        out, _ = self.gru(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze()

def train_gru(X_train, y_train, X_val, y_val, epochs=10, batch_size=256):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Scale targets for better neural network convergence
    y_mean, y_std = y_train.mean(), y_train.std()
    y_train_scaled = (y_train - y_mean) / y_std
    
    X_train_t = torch.tensor(X_train, dtype=torch.float32).unsqueeze(1).to(device)
    y_train_t = torch.tensor(y_train_scaled.values, dtype=torch.float32).to(device)
    
    dataset = TensorDataset(X_train_t, y_train_t)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model = GRUForecaster(input_dim=X_train.shape[1]).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.01)
    
    for epoch in range(epochs):
        model.train()
        for batch_X, batch_y in loader:
            optimizer.zero_grad()
            preds = model(batch_X)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()
            
    return model, y_mean, y_std

def predict_gru(model_data, X):
    model, y_mean, y_std = model_data
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    with torch.no_grad():
        X_t = torch.tensor(X, dtype=torch.float32).unsqueeze(1).to(device)
        preds_scaled = model(X_t)
    return preds_scaled.cpu().numpy() * y_std + y_mean
