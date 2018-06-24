help:
	@echo "    train-nlu"
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train a dialogue model using Rasa core."
	@echo "    run"
	@echo "        Runs the bot on the command line."

run:
	python bot.py run

run-server:
	python bot.py run-server

train:
	rm -rf ./models
	make train-nlu
	make train-core

train-nlu:
	python bot.py train-nlu

train-core:
	python bot.py train-dialogue
