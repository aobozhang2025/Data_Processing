import os

from DataHandler.DataService import DataService
from Util.Util import Util

if __name__ == "__main__":
    # Initialize the client
    deepseek = DataService(
        base_url='https://api-inference.modelscope.cn/v1/',
        api_key='ae779497-79d0-4b1e-888d-1ee262e3900e',
        model='deepseek-ai/DeepSeek-R1-0528'
    )

    prompt = 'Imagine you are a chemist that is a professional in synthesizing catalysts, please summarize what catalyst is synthesized and the synthesis procedures with all the details from the following paragraph: '

    current_directory = os.getcwd()
    directory = current_directory + '\\paragraphs\\'
    files = Util.get_files_in_directory(directory)

    for file in files:
        result = Util.read_doi_paper_file(file)
        question = prompt + '\n\n' + result['content']
        reason, answer = deepseek.get_response(question)

        file_name = current_directory + '\\answers\\' + result['doi'] + '.txt'
        to_write = 'question: \n\n' + question + '\n\nreasoning: \n\n' + reason + '\n\nanswer: \n\n' + answer
        Util.save_string_to_file(to_write, file_name)
