FROM ubuntu:latest

COPY requiremets.txt requiremets.txt

RUN pip install -r requiremets.txt

RUN git clone --branch telegram-bot https://github.com/AlexxFlexing/mtuci_prompt_analyzer.git telegram

COPY teletoken telegram/resources/

CMD telegram/telegram.py & backend/pappmanage.py runserver
