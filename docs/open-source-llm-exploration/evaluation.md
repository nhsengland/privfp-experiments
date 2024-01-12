# Evaluating generated outputs

How do we run evaluate an open source LLM? The following table contains a (non-exhaustive) list of methods to evaluate an open source LLM.

Some of these projects such as lm-evaluation-harness provide extensive evaluation tools however they can be cumbersome to set up and computationally expensive to run locally due to the vast number of requests each evaluation task passes to the LLM.

!!! info "Projects"

    === "Language Model Evaluation Harness"

        Framework

        A unified framework to test LLMs on a large number of different evaluation tasks

        https://github.com/EleutherAI/lm-evaluation-harness	

    === "FastChat"	
        Benchmark
        LLM as a judge

        Uses MT-bench, a set of challenging multi-turn open-ended questions to evaluate models
        To automate the evaluation process, FastChat prompts strong LLMs like GPT-4 to act as judges and assess the quality of responses

        https://github.com/lm-sys/FastChat	

    === "AlpacaEval"

        Benchmark

        An LLM-based automatic evaluation that validated against human annotations
        Evaluation by measuring the fraction of times a powerful LLM (e.g. GPT-4, Claude or ChatGPT) prefers the outputs from a LLM over outputs from a reference LLM

        https://github.com/tatsu-lab/alpaca_eval	

    === "Measuring Massive Multitask Language Understanding"

        Multiple choice tests	
        A variety of 57 tasks to assess an LLMs general knowledge and ability to problem solve

        https://arxiv.org/abs/2009.03300	

    === "promptfoo"

        Custom

        A tool for testing and evaluating LLM output quality
        Define test cases to score LLM outputs

        https://github.com/typpo/promptfoo


    === "agenta"

        Application

        An open source LLMOps platform for prompt engineering, evaluation, human feedback, and deployment of complex LLM apps
        Provides a nice GUI to iterate versions
        Multiple evaluation methods and metrics available out of the box

        https://github.com/agenta-ai/agenta


    === "PromptTools"	
        Benchmark
        LLM as a judge

        Self-host tools for experimenting with, testing, and evaluating LLMs
        Evaluation tools: https://prompttools.readthedocs.io/en/latest/utils.html
        Supports multiple LLMs, vector databases, frameworks and Stable Diffusion

        https://github.com/hegelai/prompttools


    === "OpenAI Evals"

        Framework

        A framework for evaluating LLMs or systems built using LLMs as components
        Includes an open source registry of challenging evals
        An "eval" is a task used to evaluate the quality of a system's behaviour
        Requires an OpenAI API key

        https://github.com/openai/evals

When using pre-trained models it may be more effective to review performance benchmarks and metrics already published, for example the chatbot-arena-leaderboard on Hugging Face https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard.

If we start fine-tuning models, it may be worth considering a more efficient platform for running evaluation tasks.