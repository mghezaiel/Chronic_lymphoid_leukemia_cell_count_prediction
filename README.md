# CLL Predictor 

Author: GHEZAIEL Morad 
email: Ghezaiel.morad@gmail.com


This tool allows to count lymphoid cell using Raman spectroscopy data. 

## Docker installation:  

### Image build:
In a command prompt (linux or windows), go to the root folder then: 

- docker image build -t cll_predictor -f Dockerfile .

The installation should take 2 minutes. 

### Launch the tool: 
Still in the root folder: 
- docker run -p 8501:8501 cll_predictor
 
The app will start and be accessible through the web browser at: 
- localhost:8501


## Informations 
The app is built using the streamlit library and deployed using Docker. 
All requirements are handled by the dockerfile. 
Information on how to use the app is available via the app itself (How it works)


