def generate_Persona_txt(clip_descriptions,name):
    prompt = (
        "Your goal is to answer questions and timestamp of the answer that above by using the data that i will provide to you next."
        "example of answer like question: What is neural network, answer: the neural network is A neural network is a computational model inspired by the structure and functioning of the human brain., timestamp:0:00:23"
        "example of answer like question: When is neural network, answer: the neural network in timestamp, timestamp:0:00:23\n\n"
    )
    prompt += "\n\n"+clip_descriptions
    write_txt(prompt,name)

def write_txt(str,name):
    with open(name+'.txt', 'w',encoding="utf-8") as f:
        f.write(str) 