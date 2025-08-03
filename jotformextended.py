import json
import requests
from typing import Optional, Dict, Any


class JotformExtendedClient:
    """Extended Jotform API client for Python"""

    SUBDOMAINS = {"api": "api", "eu": "eu-api", "hipaa": "hipaa-api"}
    INTERNAL_SUBDOMAINS = {"api": "www", "eu": "eu", "hipaa": "hipaa"}
    # DEFAULT_SUB = "api"
    # EU_SUB = "eu-api"
    # HIPAA_SUB = "hipaa-api"
    # DEFAULT_INTERNAL = ""
    # DEFAULT_EU = "eu"
    # DEFAULT_HIPAA = "hipaa"

    # set base url based on selection
    # add types
    # function for downloading files

    def __init__(self, api_key: str, subdomain: str = "api", debug: bool = False):
        """Initialize a new instance of the Extended Jotform API client

        Args:
            api_key (str): Jotform API key.

            subdomain (str, optional): Which subdomain to use for API calls. This will depend on the datacenter your Jotform account uses. These are the available options are `api`, `eu`, `hipaa`.
                `api` (default): The default subdomain for Jotform API calls.
                `eu`: Used by accounts that are on the European Datacenter.
                `hipaa`: Used by accounts that have HIPAA compliance enabled.

            debug (bool, optional): Enabled debug output, `False` by default.
        """
        self.__api_key = api_key
        self.__is_debug = debug
        # self.__compliance = subdomain
        self.__base_url = f"https://{self.SUBDOMAINS[subdomain]}.jotform.com"
        self.__internal_base_url = "https://"
        self.__internal_base_url += f"{self.INTERNAL_SUBDOMAINS[subdomain]}"
        self.__internal_base_url += ".jotform.com/API"

    def make_request(
        self,
        api_path: str,
        method: str = "GET",
        params: Optional[Dict[str, str]] = None,
        internal: bool = False,
    ):
        # make check for api version
        headers = {"apiKey": self.__api_key}
        if internal:
            url = self.__internal_base_url + api_path
            headers["referer"] = self.__internal_base_url
        else:
            url = self.__base_url + api_path
        if params:
            response = requests.request(
                method=method, url=url, headers=headers, params=params
            )
        else:
            response = requests.request(method=method, url=url, headers=headers)

        if self.__is_debug:
            print(f"Request URL: {url}")
            print(f"Method: {method}")

        return json.loads(response.text)

    def get_user(self):
        """
        Get user account details for this Jotform user. Including user account type, avatar URL, name, email, website URL.
        """
        return self.make_request("/user")

    def get_usage(self):
        """
        Get monthly usage for submissions, forms, agents, and API.
        """
        return self.make_request("/user/usage")

    def get_user_submissions(self):
        """
        Get list of submissions made by this Jotform account.
        """
        return self.make_request("/user/submissions")

    def get_user_subusers(self):
        """
        Get list of sub users of this Jotform account.

        NOTE:
            This is only available on legacy plans that were grand-fathered to keep this feature. Other accounts will receive 401.
        """
        return self.make_request("/user/subusers")

    def get_user_folders(self):
        """
        Get list of folders on this Jotform account.
        """
        return self.make_request("/user/folders")

    def get_user_reports(self):
        """
        Get list of reports on this Jotform account.
        """
        return self.make_request("/user/reports")

    def login(
        self, username: str, password: str, app_name: str = "", access: str = "full"
    ):
        """
        Login with given details
        """
        payload: dict[str, Any] = {
            "username": username,
            "password": password,
            "appName": app_name,
            "access": access,
        }
        return self.make_request("/user/login", method="POST", params=payload)

    def logout(self):
        """
        Log out
        """
        return self.make_request("/v1/user/logout")

    def get_user_settings(self):
        """
        Get settings for this Jotform account.
        """
        return self.make_request("/user/settings")

    def update_user_settings(self, settings: dict[str, str]):
        """
        Update user settings
        """
        return self.make_request("/user/settings", method="POST", params=settings)

    def get_user_history(self):
        """
        Get user activity log for this Jotform account.
        """
        return self.make_request("/user/history")

    def get_user_forms(self):
        """
        Get forms owned by this Jotform account.
        """
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

    def get_form(self, form_id: str | int):
        """
        Get basic information about a form.
        """
        return self.make_request(f"/form/{form_id}")

    def trash_form(self, form_id: str | int):
        """
        Move a form to trash where it will be automatically deleted after 30 days.
        """
        return self.make_request(f"/form/{form_id}", method="DELETE")

    def clone_form(self, form_id: str | int):
        """
        Clone a form.
        """
        return self.make_request(f"/form/{form_id}/clone", method="POST")

    def get_form_fields(self, form_id: str | int):
        """
        Get fields and their properties.
        """
        return self.make_request(f"/form/{form_id}/questions")

    # POST /form/{id}/questions
    def post_form_questions(self):
        return self.make_request("/form/{id}/questions", method="POST")

    # PUT /form/{id}/questions
    def put_form_questions(self):
        return self.make_request("/form/{id}/questions", method="PUT")

    def get_form_field(self, form_id: str | int, field_id: str | int):
        """
        Get properties for a specific field.
        """
        return self.make_request(f"/form/{form_id}/question/{field_id}")

    # POST /form/{id}/question/{qid}
    def post_form_question(self):
        return self.make_request("/form/{id}/question/{qid}", method="POST")

    def delete_form_field(self, form_id: str | int, field_id: str | int):
        """
        Delete a field.
        """
        return self.make_request(
            f"/form/{form_id}/question/{field_id}", method="DELETE"
        )

    def get_form_properties(self, form_id: str | int):
        """
        Get properties of a form.
        """
        return self.make_request(f"/form/{form_id}/properties")

    # POST /form/{id}/properties
    def post_form_properties(self):
        return self.make_request("/form/{id}/properties", method="POST")

    # PUT /form/{id}/properties
    def put_form_properties(self):
        return self.make_request("/form/{id}/properties", method="PUT")

    def get_form_property(self, form_id: str | int, key: str):
        """
        Get a specific property of a form.
        """
        return self.make_request(f"/form/{form_id}/properties/{key}")

    def get_form_reports(self, form_id: str | int):
        """
        Get list of reports of a form.
        """
        return self.make_request(f"/form/{form_id}/reports")

    # POST /form/{id}/reports
    def post_form_reports(self):
        return self.make_request("/form/{id}/reports", method="POST")

    def get_form_files(self, form_id: str | int):
        """
        Get list of files uploaded in a form's submissions.
        """
        return self.make_request(f"/form/{form_id}/files")

    def get_form_webhooks(self, form_id: str | int):
        """
        Get list of webhooks of a form.
        """
        return self.make_request(f"/form/{form_id}/webhooks")

    def add_form_webhook(self, form_id: str | int, webhook_url: str):
        """
        Add a webhook to a form.
        """
        payload = {"webhookURL": webhook_url}
        return self.make_request(
            f"/form/{form_id}/webhooks", method="POST", params=payload
        )

    def delete_form_webhook(self, form_id: str | int, webhook_id: str | int):
        """
        Delete a webhook on a form.
        """
        return self.make_request(
            f"/form/{form_id}/webhooks/{webhook_id}", method="DELETE"
        )

    def get_form_submissions(self, form_id: str | int):
        """
        Get submissions of a form.
        """
        return self.make_request(f"/form/{form_id}/submissions")

    # POST /form/{id}/submissions
    def post_form_submissions(self):
        return self.make_request("/form/{id}/submissions", method="POST")

    # PUT /form/{id}/submissions
    def put_form_submissions(self):
        return self.make_request("/form/{id}/submissions", method="PUT")

    def get_submission(self, submission_id: str | int):
        """
        Get a submission.
        """
        return self.make_request(f"/submission/{submission_id}")

    # POST /submission/{id}
    def post_submission(self):
        return self.make_request("/submission/{id}", method="POST")

    def delete_submission(self, submission_id: str | int):
        """
        Delete a submission.

        Note: It will NOT be trashed, it will be permanently deleted.
        """
        return self.make_request(f"/submission/{submission_id}", method="DELETE")

    def get_report(self, report_id: str | int):
        """
        Get a report.
        """
        return self.make_request(f"/report/{report_id}")

    def delete_report(self, report_id: str | int):
        """
        Delete a report.

        Note: It will NOT be trashed, it will be permanently deleted.
        """
        return self.make_request(f"/report/{report_id}", method="DELETE")

    def get_folder(self, folder_id: str):
        """
        Get a folder and its contents.
        """
        return self.make_request(f"/folder/{folder_id}")

    def create_folder(
        self,
        folder_name: str,
        parent_folder_id: Optional[str] = None,
        folder_color: Optional[str] = None,
    ):
        """
        Create a folder.
        """
        payload: dict[str, Any] = {
            "name": folder_name,
            "parent": parent_folder_id,
            "color": folder_color,
        }
        return self.make_request("/folder", method="POST", params=payload)

    # PUT /folder/{id}

    def delete_folder(self, folder_id: str):
        """
        Delete a folder.
        """
        return self.make_request(f"/folder/{folder_id}", method="DELETE")

    def get_plan(self, plan_name: str):
        """
        Get usage limits and pricing for a plan.
        """
        return self.make_request(f"/system/plan/{plan_name}")
