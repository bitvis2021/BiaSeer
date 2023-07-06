import openai
import os

openai.api_key = "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"

def use_openai_api(words):
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "user", "content": "summarizing this text:" + words + "in four sentences."}]
    )
    output_text = response["choices"][0]["message"]["content"]
    print("output_text: ", output_text)
    return output_text



def summarize_documents(docpaths):

    paths = []
    paths = docpaths
    summary_doc_content = ''

    for filename in paths:
        with open(filename, 'r') as file:
            lines = file.readlines()
            modified_lines = lines[:1] + lines[3:6]
            print("len before filter:",len(''.join(modified_lines)))
            sentencelist=(''.join(modified_lines)).split('.')
            print("lines len: ",len(sentencelist))
            sentencelist=sentencelist[:5]
            print("len after 0:10")
            print(len(''.join(sentencelist)))
            for line in sentencelist:
                line=line.replace('\n','')
                line=line.replace('\t','')
                line+='.'
                summary_doc_content += line
    print("summary_doc_content:",summary_doc_content)
    if len(summary_doc_content)>4070:
        print("summary size outlimit!!! cur_size:",len(summary_doc_content))
        summary_doc_content=summary_doc_content[0:4070]
    
    # return use_openai_api(summary_doc_content)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="summarizing this text:" + summary_doc_content + "in four sentences",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response["choices"][0]["text"].strip()
    summary = message.split("\n")
    summary = summary[-1]

    # return "Brexit negotiations will continue with other countries, including the US. Negotiations will determine British citizens' ability to work, travel, and access healthcare in the EU, as well as EU citizens' access in the UK."

    return summary



if __name__=='__main__':
    docpaths = [
        'p_articles/msn/en-ae/About 20 nations agree to send fresh military aid to Ukraine US says.txt',
        'p_articles/msn/en-ae/African leaders tell forum in Dubai why they did not condemn Russian invasion of Ukraine.txt',
        'p_articles/msn/en-ae/Allies promise to build a new Ukraine in 750bn revival from ashes of war.txt'
    ]
    summary = summarize_documents(docpaths)
    print("summary:", summary)