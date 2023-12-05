# Inventionary 

Inventionary is the name of my capstone project. 
It is an AI powered service that proposes names for a company, product or service based on several questions that are asked to the user. 

## How does it work?

A user is prompted the following questions:

- What is the core purpose of your company/product/service?
- What sets your company/product/service apart from competitors?
- Describe your target audience (demographics, interests, behaviours, location, culture)?
- Choose up to 5 emotions that your {type} evokes. (Choose up to 5 from list)
- How long do you want the name to be? (Choose one from list)
- Are there any words or themes to include? (Optional)
- Are there any words or themes to avoid? (Optional)

The program takes the answers to these questions to determine the 3 best names for the service, product or company.
If the user is not satisfied, he or she can request other 3 name options. The user can request up to 3 retries to get new option names. 

### What happens internally?

With the questions' answers, we build a ChatGPT prompt that has a standard structure. This prompt is adaptable, for example, in case optional questions are not answered, the prompt does not include information on those aspects. 

```
# Structure of the prompt sent to ChatGPT
Propose 3 names for a {type} as a markdown enumerated list. Consider: 
- This is the core purpose of the {type}: {purpose}.
- This is what sets apart the {type} from competitors: {different}.
- The length of the name shall be {length}.
- The target market is: {target}.
- The personality of the {type} is: {personality}.
- The emotions that the {type} evokes are: {emotions}.
- Include the following words or themes: {include}. # May not be included
- Avoid the following words or themes: {avoid}. # May not be included
```

Once the user finishes answering, the ChatGPT prompt is submitted, and we print the result for the user to see. If the user requests other name options we submit another query to ChatGPT that includes the previous questions. 
This way we ensure that the context of the session is preserved.  

```
[
    {"role": "system", "content": "You are a skilled marketing expert"},
    {"role": "user", "content": [prompt1]}
    {"role": "assistant", "content": [answer1]}
    {"role": "user", "content": "Propose other 3 names"}
]
```
### Future work
The decision to make several calls to the API with the same type of information was not the wisest. 
Instead, I could have requested 3 sample answers for the same initial prompt. 
That would have reduced the time and cost of the application.

The updated/revised API call would look something like the code below and would be the only one sent to the API.
We would then ask the user if he/she would like to see another set of name options. 
If he/she does, we show another one from the set of previously returned answers, not making another query to the API.

```python
messages = """
[
    {"role": "system", "content": "You are a skilled marketing expert"},
    {"role": "user", "content": [prompt1]}
]
"""
self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, n=3)
```

## Setup

1. Place your API key within a `.env` file as `API_KEY=your_actual_key_here`.
2. If running on PyCharm you'll need to go to the "Run/Debug Configuration" of you `main.py` and select "Emulate terminal in output console"

