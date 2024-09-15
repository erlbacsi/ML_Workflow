FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install jupyter

COPY . .

EXPOSE 5000

CMD ["tail", "-f", "/dev/null"]
#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
#CMD ["python", "webservice.py"]


