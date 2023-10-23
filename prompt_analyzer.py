from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer
from llama_out import format_the_output

def prompt_analyzer(prompt:str, repo:str):
    model = AutoAWQForCausalLM.from_quantized(repo, fuse_layers=True, trust_remote_code=False, safetensors=True)                                  
    tokenizer = AutoTokenizer.from_pretrained(repo, trust_remote_code=False)
    users_prompt = prompt
    prompt = f"Analyze user's prompt for further usage with LLM. Give some advices how to make prompt better. User's prompt is {users_prompt}"
    prompt_template=f'''[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    {prompt}[/INST]
    '''
    tokens = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    generation_output = model.generate(tokens, do_sample=True, temperature=0.7, top_p=0.95, top_k=40, max_new_tokens=512)
    formatted_output = format_the_output(tokenizer.decode(generation_output[0]))
    return formatted_output


#print(prompt_analyzer('Make a sequel of "Never gonnna give you up"', "C:/Users/aleks/Desktop/step2/models/Llama-2-7b-Chat-AWQ"))