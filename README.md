---
title: GPT4TurboApp
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

## Prerequisites

> If you need an introduction to `git`, or information on how to set up API keys for the tools we'll be using in this repository - check out [Interactive Dev Environment for LLM Development](https://github.com/AI-Maker-Space/Interactive-Dev-Environment-for-LLM-Development/tree/main) which has everything you'll need to get started in this repository!

> If you need an introduction to accessing the OpenAI API like a developer, or to containerizing and deploying the application to a Hugging Face space, check out [Beyond ChatGPT - Build Your First LLM Application](https://github.com/AI-Maker-Space/Beyond-ChatGPT) which has everything you'll need to ship and share this local application build!

In this repository, we'll walk you through the steps to create a Large Language Model (LLM) application that leverages the latest models from OpenAI, GPT-4 Turbo and DALL·E 3.

## 🤖 Building Your GPT-4 Turbo Application with DALL·E 3 Image Generation

For a step-by-step YouTube video walkthrough, watch this! <br />
[How to Build an LLM Application using GPT-4 Turbo and DALL·E 3](https://www.youtube.com/live/rJm3nBzCmCY)

![How to Build an LLM Application using GPT-4 Turbo and DALL·E 3](https://img.youtube.com/vi/rJm3nBzCmCY/mqdefault.jpg)

1. Clone [this](https://github.com/AI-Maker-Space/GPT4AppWithDALLE3) repo.

     ``` bash
     git clone https://github.com/AI-Maker-Space/GPT4AppWithDALLE3.git
     ```

2. Navigate inside this repo
     ``` bash
     cd GPT4AppWithDALLE3
     ```

3. Install the packages required for this python envirnoment in `requirements.txt`.
     ``` bash
     pip install -r requirements.txt
     ``` 

4. Export Your OpenAI API Key to your local env. using
     ``` bash
     export OPENAI_API_KEY=XXXX
     ```

6. Let's try deploying it locally. Make sure you're in the python environment where you installed Chainlit and OpenAI. Run the app using Chainlit. This may take a minute to run.
     ``` bash
     chainlit run app.py -w
     ```

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/54bcccf9-12e2-4cef-ab53-585c1e2b0fb5"> 
</p>

Great work! Let's see if we can interact with our chatbot to answer questions and generate images!
