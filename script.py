import sys
import os
import datetime
from openai import OpenAI

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        return f"Error reading file: {e}"

def audit_solidity_files(directory):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    client = OpenAI()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sol"):
                print(file)
                file_path = os.path.join(root, file)
                solidity_code = read_file(file_path)

                if solidity_code.startswith("Error reading file"):
                    print(solidity_code)
                    continue

                try:
                    completion = client.chat.completions.create(
                        seed=1337,
                        response_format={ "type": "json_object" },
                        model="gpt-4-1106-preview", #gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert human software developer with many decades of experienced who works on filecoin and are the best and most skilled in code reviews and audits for Solidity. This code is written for the IPC interplanetary consensu project a project associated with filecoin and ipfs. There are tests for this file as well with good code coverage. We are hiring an external auditor to begin to audit the code. before they begin we need to pre-audit and do an internal audit on the code. You have a very important job where you have to provide green, yellow and red status to assist the human pre-auditors who work on IPC. You need to declare if there are any blockers and immediate concerns about the code (red), things that are yellow that should be investigated, and check things off that are green that pass your audit. Provide detailed, actionable feedback."},
                            {"role": "user", "content": """Review and audit this Solidity code. please omit any comments along the lines of 'Ensure that these external contracts and dependencies have been thoroughly audited and are trusted.' as we are ensuring that every dependency is audited. contract dependencies in this repository have been thoroughly audited and are trusted. 
                            please give your response in the format of json similar to:
                            {filename : x,
                            summary: x,
                            red : [x,x,x],
                            yellow: [x,x,x],
                            green:[x,x,x]
                            }
                            for summary provide  an executive final summary
                            for red provider any blockers and red issues
                            for yellow provide any immediate concerns 
                            everything else worth noting goes in green

                            here is the solidity code:\n\n""" + solidity_code}
                        ]
                    )
                    response_content = completion.choices[0].message.content
                except Exception as e:
                    response_content = f"Error while calling OpenAI API: {e}"

                output_file = f"{root}/audit_{os.path.splitext(file)[0]}_{timestamp}.txt"
                with open(output_file, 'w') as output:
                    output.write(response_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    audit_solidity_files(directory)

if __name__ == "__main__":
    main()

