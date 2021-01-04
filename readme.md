# Dialog Annotator Web

This is a project to let MTurkers evaluate the dialogs. 

## How to setup

Make sure to have Python 3 installed, and run commands below to set up.

```bash
$ python -m venv ./env
$ source ./env/bin/activate
(env)$ pip install -r requirements.txt
```
```cmd
$ python -m venv env
$ env\Scripts\activate.bat
(ent) $ pip install -r requirements.txt
```
## How to develop

To run development server, run the command below.

```bash
(env)$ FLASK_ENV=development python main.py
```

## How to run in production mode

To run this web app in production mode, run the command below.
```bash
(env)$ sh run.sh
```
```cmd
set FLASK_APP=main
set FLASK_ENV=development
flask run
```
Try http://localhost:5000 on a web browser.

## Prepare the source data

### Contexts

Dialog *contexts* must be prepared in `./data/contexts`. 
Each file represents one context, and should have a filename in a form `{context_id}.json`. Context ID can be any string that does not include `__` as a substring. 
A JSON object in a context file includes one dialog and multiple candidates to put at the end of the dialog. The dialog and all candidates should be in markdown format. Here is an example of a context JSON object.

```json
{
    "cause": "shoot",
    "effect": "sadness",
    "id": "anli-3e883840-d18a-4531-a72f-d12b24d2bee5",
    "sent_formatted": "The Latah County Sheriff's Office tells the Moscow-Pullman Daily News that the Moscow man was **shot** Monday near Dreary by a 72-year-old Potlatch man."
}
```

### Questions

Questions for each *context* should be prepared in `./data/questions.json`. 
The JSON object should be an array that has many quetion objects. 
A question object should have `id`, `text`, `mintext`, and `maxtext`.
Here is an example of a questions JSON array.

```json
[
    {
        "id": "strength",
        "text": "How strongly S is likely to cause S'?",
        "mintext": "Impossible",
        "maxtext": "Strong",
        "option": {
            "1": "Impossible",
            "2": "Weak",
            "3": "Modest",
            "4": "Strong"
        }
    }
]
```

## Results

Participants who submitted the answer will get a code that looks like: 

`under_slack_talk_{user_id_with_16_digits_and_letters}`

The results are saved in `./output/response/{isValid}_{question_id}__res__{user_id}.json`. 

```json
{
    "cause": "hurt", // C
    "edited": "Such a move could also irritate the outgoing district attorney, Robert M. Morgenthau, because it could give pain to the chance of his preferred candidate,", // S'
    "effect": "pain", // E
    "isValid": true, // result of validate question
    "original": "Such a move could also irritate the outgoing district attorney, Robert M. Morgenthau, because it could **hurt** the chances of his preferred candidate,", // S
    "qid": "anli-83252bf3-4142-4a49-9253-184d78f7347b", // question id
    "strength": "1", // how strongly S is likely to cause S'?
    "timestamp": "1608221867748", // timestamp when submitted
    "uid": "brs6rj8jey4zpa49",
    "validator": { // validate question
        "answer": { // turker's answer
            "edited": "deficiency", // turker's answer (S')
            "strength": "2" // turker's answer (strength)
        },
        "intend": { // intedned answer
            "edited": "deficiency", // same as C
            "strength": "2" // intended strength
        }
    },
    "wid": "dskdkslg" // worker id
}
```

**NOTE**

There may be participants who got the code `pass_no_132v82389a823l3133id112`. 
These participants have not passed the validity check and answered wrong to one or more validity check questions.

## Configs

Modify the value of a global variable `context_count_per_user` in `./main.py` if you need to.



