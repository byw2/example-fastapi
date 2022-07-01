# specifies base image
FROM python:3.9.7

# tells Docker where all commands are going to run from
# analogy: set pwd to /usr/src/app
WORKDIR /usr/src/app

# copies requirements from local to Docker container 
# ./ refers to WORKDIR
COPY requirements.txt ./

# installs all packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copies all contents from local to WORKDIR
COPY . .

# NOTE: order matters for caching since if say we changed a file,
# steps 1-4 remain the same and only step 5 changes, so line 3 is
# for optimization purposes

# command that we want to run to start the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]