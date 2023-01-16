import openai
from flask import Flask, request, render_template, redirect

server = Flask(__name__)
server.config.from_pyfile('conf.py')


def get_completion(question):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{question}\n",
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.9,
            stop=None
        )
    except Exception as e:
        print(e)
        return e
    return response["choices"][0].text

@server.route('/chat', methods=['GET', 'POST'])
def get_request_json():
    if request.method == 'POST':
        if len(request.form['question']) < 1:
            return render_template(
                server.config['TEMPLATE'], question="null", res="问题不能为空")
        question = request.form['question']
        print("======================================")
        print("Recieved:", question)
        res = get_completion(question)
        print("Q：\n", question)
        print("A：\n", res)

        return render_template(server.config['TEMPLATE'], question=question, res=str(res))
    
    return render_template(server.config['TEMPLATE'], question=0)

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=80)
