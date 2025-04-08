import google.generativeai as genai

genai.configure(api_key="AIzaSyCDsdqeERmjUQn37XDymbQ3qKGMAnlCS44")

models = genai.list_models()

for model in models:
    print(model.name)
