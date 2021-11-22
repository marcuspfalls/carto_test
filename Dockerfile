FROM python:3.7.3-foss-2015a
ADD . /code
WORKDIR /code
RUN pip install -r docker_requirements.txt
CMD ["python", "plot_results.py"]