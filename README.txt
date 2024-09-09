Aim:
Use the python script to help fill-in information on the 1st page of the EpiInfo form.

How to:
- Ensure Python programming language is installed on the computer system.
- Open a command line interface (bash, powershett, cmd, etc).
- Activate the virtual environment under the 'venv' directory'.
	- For bash, use the command './venv/Scripts/activate'
	- For CMD or Powershell, use the command 'source venv/Scripts/activate'
- Install the dependancies if not installed already.
	- Use the command 'python -m pip install -r requirements.txt'
- Edit the text document 'type_template.txt' to suit the entry data in your form.
	- Every character in the 'type_template.txt' is 'typed' by the keyboard when the main script is activated. Enter information in sequence as the script will type it.
	- Look at the text document 'type_template - example.txt' for inspiration.
- To run the script, enter the command 'python cli.py start-keyboard-listener'.
- To close the keyboard listener and the script, alternate between the following keyboard commands a few time 'ctrl+c' and 'ctrl+z'. The script should eventually close.