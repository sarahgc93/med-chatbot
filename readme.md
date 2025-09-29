# Medical Chatbot

This repo contains work to create a chat bot for medical questions. The goal is to create a model that can effectively generate answers to user queries related to medical diseases. The initial exploration, `Part1-MedChatBot-Prep.ipynb`, can be replicated locally, in a container built via the `make build command` and ran via `make run`.

In my first notebook you will find:
1. Data Exploration
2. Data Prep

and general notes on my plan for the chatbot. Note that this repo requires an .env file, with a hugging face API key. See .env sample and set yours up accordingly. My data for this project is also not included in the repo.

The subsequent notebooks require resources that I do not have locally. I have run them in google colab.

## My Approach:
1. Assumptions:

My assumptions for this project are that users will be interacting via a chat interface. They will be asking strictly medical questions. They will not expect the chatbot to retain memory of previous messages or continue a conversation.

I also assume that the data in my medical Q/A dataset is accurate and relevant to the use case. I assume the Q/A data is free of any PII, and there are no privacy or security concerns in using it with opensource tooling.

2. Constraints:

For this project, I am constrained by my hardware and time. While initial exploration can be done locally, I do  not have any GPUs in my personal set up. I will rely on google colab, using their GPUs (A100). I do have a paid membership to colab, which allows for more resources than the free account.

I am completing this project over the course of two days, **independently, and without the assistance of third-party AI systems (such as OpenAI, Claude, or similar tools)**.

3. Design:

For this project, I have decided to create a fine-tuned Large Language model. Given its chat-based nature, we can benefit from the existing state-of-the-art chat models and further improve upon them by tuning for our medical Q/A data. 

Huggingface has made many models available for free online. While I considered using a model from the huggingface leader board as my base, but utimately decided to go with the llama models because:

- I am familiar with them
- I know they would work well with this task
- I am confident they will be able to run given my resource constraints

I used `meta-llama/Meta-Llama-3.1-8B-Instruct`, which was optimized for dialogue use cases and outperforms many other available open source models. I chose 8B due to its size, based on my constraints. Read more about it here: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct.

I have also decided to use LoRA (Low-Rank Adaption) because it uses less computational resources than other methods, while still working well for low complexity tasks. You can read more about my training approach in `Part2-MedChatbot-Train.ipynb`.

I trained the model for 3 epochs, with a small learning rate, and the model continuted to improve over the course of its training.

4. Performance

Our final evaluation statistics were as follows:
```
{'eval_loss': 0.8120278120040894,
 'eval_runtime': 214.053,
 'eval_samples_per_second': 7.666,
 'eval_steps_per_second': 7.666,
 'eval_entropy': 0.7991135515894634,
 'eval_num_tokens': 13344000.0,
 'eval_mean_token_accuracy': 0.7887991961366443,
 'epoch': 3.0}
 ```

Our mean token accuracy of 0.78 is fairly good. We are correclt predicting 78% of our sequencial tokens correctly. I must note, however, that this is not representative of the quality of the outputs. In a future attempt, I will use BLEU or ROUGE metrics to get a better sense for my output quality.

Unfortuntely, our eval entropy is a bit high. This means our model is not very confident in its answers. This may be alright, given that generative tasks are non-deterministic and there could be a variety of correct answers.

Looking an individual text cases, our model is fairly good at answering medical questions with what appears to be correct information. Some of the output formatting contains a bit more context than I would like, but I think that could be improved with additional prompting.

The biggest weakness of the model is its hallucination: I asked about a "disease" that I made up, and it still attempted to tell me about this disease.

See `Part3-MedChatbot-Run-Evaluate.ipynb` for more details.

5. Potential improvements

Given more time and resources, I would like to try out different Llama models and compare them against eachother. I would also conduct some hyperparameter tuning-- I am not confident that I chose the optimal batch size or learning rate. I'd also trainfor more epochs. I'd ideally train until the model plateaus. Depending on results, I may also look for additional medical data I can use to suplement our training.

In the future, I will expand my evaluation to include more complex metrics that better capture output quality. I will also try out an LLM as a judge.

Finally, I plan to create an interface endpoint hosted on HuggingFace or elsewhere. I'd love to be able to interact with this model via API so that I can run more experiments locally and build out a better workflow or app to generate my outputs.









