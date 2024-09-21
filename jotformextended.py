import requests


class JotformExtendedClient:
    SUBDOMAINS = {
        "api": "api",
        "eu": "eu-api",
        "hipaa": "hipaa-api"
    }
    INTERNAL_SUBDOMAINS = {
        "api": "www",
        "eu": "eu",
        "hipaa": "hipaa"
    }
    DEFAULT_SUB = "api"
    EU_SUB = "eu-api"
    HIPAA_SUB = "hipaa-api"
    DEFAULT_INTERNAL = ""
    DEFAULT_EU = "eu"
    DEFAULT_HIPAA = "hipaa"

    # set base url based on selection
    # add types
    # function for downloading files

    def __init__(self, api_key="", subdomain="api", debug=False):
        self.__api_key = api_key
        self.__is_debug = debug
        self.__compliance = subdomain
        self.__base_url = f"https://{self.SUBDOMAINS[subdomain]}.jotform.com"
        self.__internal_base_url = "https://"
        self.__internal_base_url += f"{self.INTERNAL_SUBDOMAINS[subdomain]}"
        self.__internal_base_url += ".jotform.com/API"

    def make_request(self,
                     api_path: str,
                     method='GET',
                     params=None,
                     internal=False):
        # make check for api version
        headers = {
            "apiKey": self.__api_key
        }
        if internal:
            url = self.__internal_base_url + api_path
            headers["referer"] = self.__internal_base_url
        else:
            url = self.__base_url + api_path

        # do switch case
        if method == "GET":
            requests.get(url, headers=headers)
        elif method == "POST":
            pass
        elif method == "PUT":
            pass
        elif method == "DELETE":
            pass

    def get_user(self):
        return self.make_request("/user")

    def get_user_usage(self):
        return self.make_request("/user/usage")

# GET /user/submissions
    def get_user_submissions(self):
        return self.make_request("/user/submissions")

# GET /user/subusers
    def get_user_subusers(self):
        return self.make_request("/user/subusers")

# GET /user/folders
    def get_user_folders(self):
        return self.make_request("/user/folders")

# GET /user/reports
    def get_user_reports(self):
        return self.make_request("/user/reports")

# POST /user/register
    def post_user_register(self):
        return self.make_request("/user/register", method="POST")

# POST /user/login
    def post_user_login(self):
        return self.make_request("/user/login", method="POST")

# GET /user/logout
    def get_user_logout(self):
        return self.make_request("/user/logout")

# GET /user/settings
    def get_user_settings(self):
        return self.make_request("/user/settings")

# POST /user/settings
    def post_user_settings(self):
        return self.make_request("/user/settings", method="POST")

# GET /user/history
    def get_user_history(self):
        return self.make_request("/user/history")

# GET /user/forms
    def get_user_forms(self):
        return self.make_request("/user/forms")

# POST /user/forms
    def post_user_forms(self):
        return self.make_request("/user/forms", method="POST")

# PUT /user/forms
    def put_user_forms(self):
        return self.make_request("/user/forms", method="PUT")

# POST /form
    def post_form(self):
        return self.make_request("/form", method="POST")

# PUT /form
    def put_form(self):
        return self.make_request("/form", method="PUT")

# GET /form/{id}
    def get_form(self):
        return self.make_request("/form/{id}")

# DELETE /form/{id}
    def delete_form(self):
        return self.make_request("/form/{id}", method="DELETE")

# POST /form/{id}/clone
    def post_form_clone(self):
        return self.make_request("/form/{id}/clone", method="POST")

# GET /form/{id}/questions
    def get_form_questions(self):
        return self.make_request("/form/{id}/questions")

# POST /form/{id}/questions
    def post_form_questions(self):
        return self.make_request("/form/{id}/questions", method="POST")

# PUT /form/{id}/questions
    def put_form_questions(self):
        return self.make_request("/form/{id}/questions", method="PUT")

# GET /form/{id}/question/{qid}
    def get_form_question(self):
        return self.make_request("/form/{id}/question/{qid}")

# POST /form/{id}/question/{qid}
    def post_form_question(self):
        return self.make_request("/form/{id}/question/{qid}", method="POST")

# DELETE /form/{id}/question/{qid}
    def delete_form_question(self):
        return self.make_request("/form/{id}/question/{qid}", method="DELETE")

# GET /form/{id}/properties
    def get_form_properties(self):
        return self.make_request("/form/{id}/properties")

# POST /form/{id}/properties
    def post_form_properties(self):
        return self.make_request("/form/{id}/properties", method="POST")

# PUT /form/{id}/properties
    def put_form_properties(self):
        return self.make_request("/form/{id}/properties", method="PUT")

# GET /form/{id}/properties/{key}
    def get_form_properties(self):
        return self.make_request("/form/{id}/properties/{key}")

# GET /form/{id}/reports
    def get_form_reports(self):
        return self.make_request("/form/{id}/reports")

# POST /form/{id}/reports
    def post_form_reports(self):
        return self.make_request("/form/{id}/reports", method="POST")

# GET /form/{id}/files
    def get_form_files(self):
        return self.make_request("/form/{id}/files")

# GET /form/{id}/webhooks
    def get_form_webhooks(self):
        return self.make_request("/form/{id}/webhooks")

# POST /form/{id}/webhooks
    def post_form_webhooks(self):
        return self.make_request("/form/{id}/webhooks", method="POST")

# DELETE /form/{id}/webhooks/{whid}
    def delete_form_webhooks(self):
        return self.make_request("/form/{id}/webhooks/{whid}", method="DELETE")

# GET /form/{id}/submissions
    def get_form_submissions(self):
        return self.make_request("/form/{id}/submissions")

# POST /form/{id}/submissions
    def post_form_submissions(self):
        return self.make_request("/form/{id}/submissions", method="POST")

# PUT /form/{id}/submissions
    def put_form_submissions(self):
        return self.make_request("/form/{id}/submissions", method="PUT")
    
# GET /submission/{id}
    def get_submission(self):
        return self.make_request("/submission/{id}")

# POST /submission/{id}
    def post_submission(self):
        return self.make_request("/submission/{id}", method="POST")

# DELETE /submission/{id}
    def delete_submission(self):
        return self.make_request("/submission/{id}", method="DELETE")
    
