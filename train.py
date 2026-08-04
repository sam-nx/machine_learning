import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import time


def main():
    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    train_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])

    test_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])

    train_ds = datasets.ImageFolder("data/Train", transform=train_tf)
    test_ds = datasets.ImageFolder("data/Test", transform=test_tf)

    train_loader = DataLoader(train_ds, batch_size=64,
                              shuffle=True, num_workers=4)
    test_loader = DataLoader(test_ds, batch_size=32,
                             shuffle=False, num_workers=4)

    num_classes = len(train_ds.classes)
    print(f"{num_classes} classes")
    n_start_time = time.time()

    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

    for param in model.parameters():
        param.requires_grad = False

    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)

    def evaluate(loader):
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for images, labels in loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                preds = outputs.argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        return correct / total

    num_epochs = 10
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        train_acc = evaluate(train_loader)
        test_acc = evaluate(test_loader)
        print(f"Epoch {epoch+1}/{num_epochs} | Loss: {running_loss/len(train_loader):.4f} | Train acc: {train_acc:.3f} | Test acc: {test_acc:.3f}")

    n_end_time = time.time()

    print(f"Took {n_end_time - n_start_time}")

    torch.save({
        "model_state_dict": model.state_dict(),
        "classes": train_ds.classes
    }, "bird_classifier.pth")

    print("Saved to bird_classifier.pth")


if __name__ == "__main__":
    main()
