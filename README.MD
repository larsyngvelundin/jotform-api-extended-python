
# Unofficial Jotform API Extended Python Client

This is an unofficial API wrapper for Jotform in Python that includes additional endpoints and documentation.

## Information
The official documentation can be found here: [Jotform API Documentation](https://api.jotform.com/docs)

Additional documentation for the different endpoints are included in the docstrings of each function.

API coverage:

| Endpoints | [Jotform API](https://github.com/jotform/jotform-api-python/) | Extended |
|---|---|---|
| User | ✔️ | ✔️ |
| Form | ✔️ | ✔️ |
| Form Questions | ✔️ | ✔️ |
| Form Properties | ✔️ | ✔️ |
| Form Submissions | ✔️ | ✔️ |
| Form Webhooks | ✔️ | ✔️ |
| Form Reports | ✔️ | ✔️ |
| Submission | ✔️ | ✔️ |
| Report | ✔️ | ✔️ |
| Folder | ✔️ | ✔️ |
| System | ✔️ | ✔️ |
| Teams | ❌ | ✔️ |
| Apps | ❌ | ✔️ |
| Form Archive | ❌ | ✔️ |
| Submission Threads | ❌ | ✔️ |
| PDFs | ❌ | ✔️ |
| AI Agents | ❌ | ✔️ |
| SMTP | ❌ | ✔️ |

## Installing
You can install the extended client using:

      $ pip install jotform-extended

## Authentication
The Jotform API requires a Jotform API key. If you don't have one, you can follow [this guide](https://www.jotform.com/help/253-how-to-create-a-jotform-api-key/) to create one.

## Usage examples
Get user details:
```python
from jotformextended import JotformExtendedClient

jotform_api_key = "your_api_key"

jf = JotformExtendedClient(api_key=jotform_api_key)
user_details = jf.get_user()
print(user_details)
```
Get form details:
```python
from jotformextended import JotformExtendedClient

jotform_api_key = "your_api_key"
form_id = "your_form_id"

jf = JotformExtendedClient(api_key=jotform_api_key)
form_details = jf.get_form(form_id=form_id)
print(form_details)
```
Create a form:
```python
from jotformextended import JotformExtendedClient

jotform_api_key = "your_api_key"
form_details = {
    "properties[title]": "Form Title",
    "questions[0][type]": "control_head",
    "questions[0][text]": "Form Header",
    "questions[0][order]": "1",
    "questions[1][type]": "control_textbox",
    "questions[1][text]": "Text Box Label",
    "questions[1][order]": "2",
    "questions[1][required]": "Yes",
    "questions[1][readonly]": "No",
    "emails[0][type]": "notification",
    "emails[0][name]": "Notification 1",
    "emails[0][from]": "default",
    "emails[0][to]": "example@example.com",
    "emails[0][subject]": "New Submission Received",
}

jf = JotformExtendedClient(api_key=jotform_api_key)
response = jf.create_form(form=form_details)
print(f"Form ID: {response['content']['id']}")
print(f"Form URL: {response['content']['url']}")
```
