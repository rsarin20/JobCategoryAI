import os
import openai
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

# Initialize the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/', methods=['GET', 'POST'])
def generate_prompts():
    if request.method == 'POST':
        job_category = request.form['job_category']
        industry = request.form['industry']
        prompts = get_prompts(job_category, industry)

        # Store the prompts in a file
        with open('prompts.txt', 'w') as f:
            f.write('\n'.join(prompts))

        return redirect(url_for('success', job_category=job_category, industry=industry))  # Redirect to a success page

    return render_template('index.html')


@app.route('/success/<job_category>/<industry>')
def success(job_category, industry):
    with open('prompts.txt', 'r') as file:
        prompts = file.read()
    return render_template('index.html', job_category=job_category, industry=industry, prompts=prompts)


def get_prompts(job_category, industry):
    prompt = f"What are the most effective ChatGPT / Bard AI prompts that a {job_category} working in the {industry} industry should ask?"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=1
    )

    prompts = response.choices[0].text.strip().split('\n')
    return prompts


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
