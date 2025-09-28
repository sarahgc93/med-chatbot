# Medical Chatbot

This repo contains work to create a chat bot for medical questions. The initial exploration, Part1-MedChatBot-Prep.ipynb, can be replicated locally, in a container built via the `make build command` and ran via `make run`.

In my first notebook you will find:
1. Data Exploration
2. Data Prep

and general notes on my plan for the chatbot.

The model itself was fine-tuned in a google colab gpu instance, using `meta-llama/Meta-Llama-3.1-8B-Instruct` and hugging face libraries.

Note that this repo requires an .env file, with a hugging face API key. See .env sample and set yours up accordingly. My data for this project is also not including in the repo.







