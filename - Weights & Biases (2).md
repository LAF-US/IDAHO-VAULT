---
title: "Weights & Biases"
source: "https://wandb.ai/laf-us"
author:
published:
created: 2026-05-03
description: "Weights & Biases, developer tools for machine learning"
date created: Sunday, May 3rd 2026, 11:33:55 pm
date modified: Sunday, May 3rd 2026, 11:34:13 pm
---

[Skip to main content](https://wandb.ai/laf-us#main-content)

29 days remaining in your team trial.

[Learn more →](https://wandb.ai/trial_end)

W&B Models

Build & fine-tune models

W&B Weave

Develop AI apps

W&B Inference

Access hosted models

## Visualize your model training with

or

1. Set up the wandb library

Install the CLI and Python library for interacting with the Weights and Biases API.

`pip install wandb`

Next, log in and paste your API key when prompted.

`wandb login`

**Generate your API key.** Use it to log in to the wandb library.

Generate

8. Log a Run to a new project

Start tracking system metrics and console logs, right out of the box. Run this sample code to see the new run appear in W&B.

`import random  import wandb  # Start a new wandb run to track this script. run = wandb.init(     # Set the wandb entity where your project will be logged (generally your team name).     entity="laf-us",     # Set the wandb project where this run will be logged.     project="my-awesome-project",     # Track hyperparameters and run metadata.     config={         "learning_rate": 0.02,         "architecture": "CNN",         "dataset": "CIFAR-100",         "epochs": 10,     }, )  # Simulate training. epochs = 10 offset = random.random() / 5 for epoch in range(2, epochs):     acc = 1 - 2**-epoch - random.random() / epoch - offset     loss = 2**-epoch + random.random() / epoch + offset      # Log metrics to wandb.     run.log({"acc": acc, "loss": loss})  # Finish the run and upload any remaining data. run.finish()`

Show more

12. See live metrics, terminal logs, and system stats in your project

🎉 Congrats! Now that you've run the code, navigate to your newly created project to compare the runs and their metrics.