FROM python:3.9

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN git clone --branch telegram-bot https://github.com/AlexxFlexing/mtuci_prompt_analyzer.git telegram
RUN git clone --branch master https://github.com/AlexxFlexing/mtuci_prompt_analyzer.git backend

COPY teletoken telegram/resources/

CMD python telegram/telegram.py & python backend/pappmanage.py runserver
