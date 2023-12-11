import sys
from openai import OpenAI

def read_solidity_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_solidity_file>")
        sys.exit(1)

    solidity_file_path = sys.argv[1]
    solidity_code = read_solidity_file(solidity_file_path)

    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert human software developer with many decades of experienced who works on filecoin and are the best and most skilled in code reviews and audits for Solidity. This code is written for the IPC interplanetary consensu project a project associated with filecoin and ipfs. There are tests for this file as well with good code coverage. We are hiring an external auditor to begin to audit the code. before they begin we need to pre-audit and do an internal audit on the code. You have a very important job where you have to provide green, yellow and red status to assist the human pre-auditors who work on IPC. You need to declare if there are any blockers and immediate concerns about the code (red), things that are yellow that should be investigated, and check things off that are green that pass your audit. Provide detailed, actionable feedback."},
                {"role": "user", "content": f"Review and audit this Solidity code. please omit any comments along the lines of 'Ensure that these external contracts and dependencies have been thoroughly audited and are trusted.' as we are ensuring that every dependency is audited. here is the solidity code:\n\n{solidity_code}"}
            ]
        )
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        sys.exit(1)

    if completion.choices:
        response = completion.choices[0].message
        print("\n=== OpenAI Response ===\n")
        print(response.content)
    else:
        print("No response received from OpenAI API.")

if __name__ == "__main__":
    main()

