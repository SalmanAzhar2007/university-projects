import torch
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from torch import nn
from torch.utils.data import DataLoader

#model hyperparameters
learning_rate = 1e-3
batch_size = 64      #number of samples in each batch
epochs = 20          #number of cycles

#setting device
device = 'cpu'
print("Using ", device, "device")

#loading mnist train and test datasets
mnistTrainset = datasets.MNIST(root='./data', train=True, download=True, transform=transforms.ToTensor())
mnistTestset = datasets.MNIST(root='./data', train=False, download=True, transform=transforms.ToTensor())

#set up dataloaders
trainDataloader = DataLoader(mnistTrainset, batch_size=batch_size, shuffle=True)
testDataloader = DataLoader(mnistTestset, batch_size=batch_size, shuffle=True)

#setting up the neural network class
class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten() #converts images to a 1D vector
        self.linear_relu_stack = nn.Sequential(   #defining the network's architecture
            nn.Linear(28*28, 512),  #first layer with 784 inputs and 512 outputs      
            nn.ReLU(),              #activation function
            nn.Linear(512, 512),    #second layer with 512 inputs and outputs
            nn.ReLU(),       
            nn.Linear(512, 10),     #third layer with 512 inputs and 10 outputs coinciding with the 10 possible numbers
        )
    def forward(self, x):           #defining forward pass
        x = self.flatten(x)
        return self.linear_relu_stack(x)

#defining the train and test loops
def train_loop(dataloader, model, loss_function, optimiser):
    size = len(dataloader.dataset)
    model.train() #set model to training mode

    for batch, (X, y) in enumerate(dataloader):
        pred = model(X) #forward pass, get prediction
        loss = loss_function(pred, y) #calculate loss (comparing with true y value)

        #backpropagation
        loss.backward() 
        optimiser.step()

        #reset gradients
        optimiser.zero_grad()

        #periodically print training progress
        if batch % 100 == 0:
            loss, current = loss.item(), batch * batch_size + len(X)
            print("loss: ", round(loss, 6), "[", current, "/", size, "]")

def test_loop(dataloader, model, loss_function):
    model.eval() #set model to evaluation mode

    size = len(dataloader.dataset)
    numBatches = len(dataloader)
    testLoss, correct = 0, 0

    #don't need to calculate gradients in test loop, so use no_grad
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            testLoss += loss_function(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item() #tracks number of correct predictions
        testLoss /= numBatches
        correct /= size
        print("Test Error: \nAccuracy: ", round(100 * correct, 1), "%, Avg loss: ", round(testLoss, 6), " \n") #print test metrics

#initialise model
model = NeuralNet()

#define appropriate loss function and optimiser.
lossFunction = nn.CrossEntropyLoss() 
optimiser = torch.optim.SGD(model.parameters(), lr=learning_rate)

#optimisation loop
for i in range(epochs):
    print("Epoch ",i+1,"\n-------------------------------")
    train_loop(trainDataloader, model, lossFunction, optimiser)
    test_loop(testDataloader, model, lossFunction)
print("Done!")

#save trained model
torch.save(model, 'model.pth')