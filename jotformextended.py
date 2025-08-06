import json
import requests
from typing import Optional, Dict, Any


class JotformExtendedClient:
    """Extended Jotform API client for Python"""

    SUBDOMAINS = {"api": "api", "eu": "eu-api", "hipaa": "hipaa-api"}
    INTERNAL_SUBDOMAINS = {"api": "www", "eu": "eu", "hipaa": "hipaa"}

    def __init__(self, api_key: str, subdomain: str = "api", debug: bool = False):
        """Initialize an Extended Jotform API client.

        Args:
            api_key (str): Jotform API key.
            subdomain (str, optional): Subdomain to use for API calls; determines the datacenter (default: 'api').
                Available options are:
                    - 'api': Default subdomain for general Jotform API calls.
                    - 'eu': Use for accounts on the European Datacenter.
                    - 'hipaa': Use for HIPAA-compliant accounts.
            debug (bool, optional): Enable debug output (default: False).
        """
        self.__api_key = api_key
        self.__is_debug = debug
        self.__base_url = f"https://{self.SUBDOMAINS[subdomain]}.jotform.com"
        self.__internal_base_url = "https://"
        self.__internal_base_url += f"{self.INTERNAL_SUBDOMAINS[subdomain]}"
        self.__internal_base_url += ".jotform.com/API"

    def _make_request(
        self,
        api_path: str,
        method: str = "GET",
        params: Optional[Dict[str, str]] = None,
        internal: bool = False,
    ):
        """Send an HTTP request to the specified API endpoint.

        Args:
            api_path (str): Relative API path (e.g., "/user/submissions").
            method (str, optional): HTTP method to use ('GET', 'POST', etc.). Defaults to 'GET'.
            params (dict, optional): HTTP query parameters to include in the request. Defaults to None.
            internal (bool, optional): If True, use the internal base URL and set a referer header. Defaults to False.

        Returns:
            dict: Parsed JSON response from the API.
        """
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
        Retrieves account details for the current Jotform user.

        Returns:
            dict: A dictionary containing user account details, such as:
                - account type
                - avatar URL
                - name
                - email
                - website URL
        """
        return self._make_request("/user")

    def get_usage(self):
        """
        Retrieves current monthly usage statistics for the user's account.

        Returns:
            dict: A dictionary containing usage details, including:
                - total and remaining submissions
                - form count
                - agent usage
                - API usage
        """
        return self._make_request("/user/usage")

    def get_user_submissions(self):
        """
        Retrieves a list of submissions made by the current Jotform account.

        Returns:
            dict: A dictionary containing a list of submission records submitted by the user.
        """
        return self._make_request("/user/submissions")

    def get_user_subusers(self):
        """
        Retrieves a list of sub-users associated with this Jotform account.

        Note:
            This feature is only available on legacy plans that were grandfathered to keep it.
            Other accounts will receive a 401 Unauthorized error.

        Returns:
            dict: A dictionary containing the list of sub-user accounts.
        """
        return self._make_request("/user/subusers")

    def get_user_folders(self):
        """
        Retrieves a list of folders in the current Jotform account.

        Returns:
            dict: A dictionary containing folder information for the user.
        """
        return self._make_request("/user/folders")

    def get_user_reports(self):
        """
        Retrieves a list of reports associated with the current Jotform account.

        Returns:
            dict: A dictionary containing information about the user's reports.
        """
        return self._make_request("/user/reports")

    def login(
        self, username: str, password: str, app_name: str = "", access: str = "full"
    ):
        """
        Logs in a user with the provided credentials.

        Args:
            username (str): The username of the Jotform account.
            password (str): The password for the account.
            app_name (str, optional): The name of the application making the login request. Defaults to an empty string.
            access (str, optional): The access level requested, e.g., "full" (default) or "readOnly".

        Returns:
            dict: The response from the login API, typically including authentication tokens or user info.
        """
        payload: dict[str, Any] = {
            "username": username,
            "password": password,
            "appName": app_name,
            "access": access,
        }
        return self._make_request("/user/login", method="POST", params=payload)

    def logout(self):
        """
        Logs out the current user from the Jotform account.

        Returns:
            dict: The response from the logout API, typically indicating success or failure.
        """
        return self._make_request("/v1/user/logout")

    def get_user_settings(self):
        """
        Retrieves settings for the current Jotform account, such as username, time zone, email, and account status.

        Returns:
            dict: A dictionary containing user settings and account details.
        """
        return self._make_request("/user/settings")

    def update_user_settings(self, settings: dict[str, str]):
        """
        Updates the settings for the current Jotform account.

        Args:
            settings (dict[str, str]): A dictionary of user settings to update, where keys are setting names and values are the corresponding new values.
                The available keys can be obtained from the `get_user_settings` method.

        Returns:
            dict: The response from the API indicating the result of the update operation.
        """
        return self._make_request("/user/settings", method="POST", params=settings)

    def get_user_history(self):
        """
        Retrieve the user activity log for the current Jotform account.

        Returns:
            dict: Parsed JSON response from the API containing the user activity log and related details.
        """
        return self._make_request("/user/history")

    def get_user_forms(self):
        """
        Retrieve a list of forms owned by the current Jotform account.

        Returns:
            dict: Parsed JSON response from the API containing the list of forms and their details.
        """
        return self._make_request("/user/forms")

    def create_form(self, form: dict[str, str]):
        """
        Create a new form with the specified properties, questions, and email notifications.

        Args:
            form (dict[str, str]): A dictionary containing the form's properties, questions, and emails to be set at creation.
                Example structure:
                    {
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

        Returns:
            dict: Parsed JSON response from the API containing details of the newly created form, including the Form ID.
        """
        return self._make_request("/form", method="POST", params=form)

    def get_form(self, form_id: str | int):
        """
        Get basic information about a form.

        Args:
            form_id (str or int): ID of the form.

        Returns:
            dict: A dictionary containing the parsed JSON response from the API.
        """
        return self._make_request(f"/form/{form_id}")

    def trash_form(self, form_id: str | int):
        """
        Move a form to the trash, where it will be automatically deleted after 30 days.

        Args:
            form_id (str or int): The ID of the form to move to trash.

        Returns:
            dict: Parsed JSON response from the API.
        """
        return self._make_request(f"/form/{form_id}", method="DELETE")

    def clone_form(self, form_id: str | int):
        """
        Create a clone of an existing form.

        Args:
            form_id (str or int): The ID of the form to clone.

        Returns:
            dict: Parsed JSON response from the API, containing details of the cloned form, including the Form ID.
        """
        return self._make_request(f"/form/{form_id}/clone", method="POST")

    def get_form_fields(self, form_id: str | int):
        """
        Retrieve all fields and their properties for a specific form.

        Args:
            form_id (str or int): The ID of the form whose fields are being requested.

        Returns:
            dict: Parsed JSON response from the API, containing a list of form fields and their properties.
        """
        return self._make_request(f"/form/{form_id}/questions")

    def add_form_field(self, form_id: str | int, field: dict[str, str]):
        """
        Add a new field to a form.

        Args:
            form_id (str or int): The ID of the form to which the field will be added.
            field (dict[str, str]): Dictionary containing the field properties to add.
                Example structure:
                    {
                        "question[type]": "control_head",
                        "question[text]": "Form Title",
                        "question[order]": "1",
                        "question[name]": "myheader",
                    }

        Returns:
            dict: Parsed JSON response from the API confirming the addition and details of the new field.
        """
        return self._make_request(
            f"/form/{form_id}/questions", method="POST", params=field
        )

    def get_form_field(self, form_id: str | int, field_id: str | int):
        """
        Retrieve properties of a specific field within a form.

        Args:
            form_id (str or int): The ID of the form containing the field.
            field_id (str or int): The ID of the specific field whose properties are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the properties of the specified field.
        """
        return self._make_request(f"/form/{form_id}/question/{field_id}")

    def update_form_field(
        self, form_id: str | int, field_id: str | int, field_details: dict[str, str]
    ):
        """
        Update the properties of a specific field within a form.

        Args:
            form_id (str or int): The ID of the form containing the field to update.
            field_id (str or int): The ID of the field to be updated.
            field_details (dict[str, str]): A dictionary containing the updated field properties.
                Example structure:
                    {
                        "question[text]": "New label text",
                        "question[order]": "2",
                    }

        Returns:
            dict: Parsed JSON response from the API confirming the update and showing the updated field details.
        """
        return self._make_request(
            f"/form/{form_id}/question/{field_id}", method="POST", params=field_details
        )

    def delete_form_field(self, form_id: str | int, field_id: str | int):
        """
        Delete a specific field from a form.

        Args:
            form_id (str or int): The ID of the form containing the field to delete.
            field_id (str or int): The ID of the field to be deleted.

        Returns:
            dict: Parsed JSON response from the API confirming the deletion.
        """
        return self._make_request(
            f"/form/{form_id}/question/{field_id}", method="DELETE"
        )

    def get_form_properties(self, form_id: str | int):
        """
        Retrieve the properties of a specific form.

        Args:
            form_id (str or int): The ID of the form whose properties are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the properties of the form.
        """
        return self._make_request(f"/form/{form_id}/properties")

    def update_form_properties(self, form_id: str | int, properties: dict[str, str]):
        """
        Update the properties of a specific form.

        Args:
            form_id (str or int): The ID of the form to update.
            properties (dict[str, str]): A dictionary of form properties to update.
                Example structure:
                    {
                        "properties[background]": "#FFEEDD",
                        "properties[title]": "New Form Title",
                        "properties[thankurl]": "http://www.newthankyoupage.com",
                        "properties[activeRedirect]": "thankurl",
                    }

        Returns:
            dict: Parsed JSON response from the API confirming the update and showing the updated form properties.
        """
        return self._make_request(
            f"/form/{form_id}/properties", method="POST", params=properties
        )

    def get_form_property(self, form_id: str | int, property: str):
        """
        Retrieve a specific property of a form by its key.

        Args:
            form_id (str or int): The ID of the form whose property is being requested.
            property (str): The key/name of the property to retrieve.

        Returns:
            dict: Parsed JSON response from the API containing the value of the specified form property.
        """
        return self._make_request(f"/form/{form_id}/properties/{property}")

    def get_form_reports(self, form_id: str | int):
        """
        Retrieve a list of reports associated with a specific form.

        Args:
            form_id (str or int): The ID of the form whose reports are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the list of reports and their details.
        """
        return self._make_request(f"/form/{form_id}/reports")

    def create_report(
        self,
        form_id: str | int,
        report_title: str,
        report_type: str,
        fields: Optional[str] = None,
    ):
        """
        Create a report for a specific form.

        Args:
            form_id (str or int): The ID of the form for which the report is created.
            report_title (str): The title of the report.
            report_type (str): The type of report to create. Supported types are:
                'csv', 'excel', 'grid', 'table', 'rss'.
            fields (Optional[str], optional): Comma-separated string specifying which fields to include in the report. Defaults to None. Example: "ip,dt,1,3,4"

        Returns:
            dict: Parsed JSON response from the API containing details of the created report.
        """
        report_data: dict[str, Any] = {
            "title": report_title,
            "list_type": report_type,
            "fields": fields,
        }
        return self._make_request(
            f"/form/{form_id}/reports", method="POST", params=report_data
        )

    def get_form_files(self, form_id: str | int):
        """
        Retrieve a list of files uploaded through a form's submissions.

        Args:
            form_id (str or int): The ID of the form whose uploaded files are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the list of uploaded files and their details.
        """
        return self._make_request(f"/form/{form_id}/files")

    def get_form_webhooks(self, form_id: str | int):
        """
        Retrieve a list of webhooks on a specific form.

        Args:
            form_id (str or int): The ID of the form whose webhooks are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the list of webhooks and their details.
        """
        return self._make_request(f"/form/{form_id}/webhooks")

    def add_form_webhook(self, form_id: str | int, webhook_url: str):
        """
        Add a webhook URL to a specific form.

        Args:
            form_id (str or int): The ID of the form to which the webhook will be added.
            webhook_url (str): The URL of the webhook to add.

        Returns:
            dict: Parsed JSON response from the API confirming the addition of the webhook and containing its details.
        """
        payload = {"webhookURL": webhook_url}
        return self._make_request(
            f"/form/{form_id}/webhooks", method="POST", params=payload
        )

    def delete_form_webhook(self, form_id: str | int, webhook_id: str | int):
        """
        Delete a specific webhook from a form.

        Args:
            form_id (str or int): The ID of the form from which the webhook will be deleted.
            webhook_id (str or int): The ID of the webhook to delete.

        Returns:
            dict: Parsed JSON response from the API confirming the deletion of the webhook.
        """
        return self._make_request(
            f"/form/{form_id}/webhooks/{webhook_id}", method="DELETE"
        )

    def get_form_submissions(self, form_id: str | int):
        """
        Retrieve submissions of a specific form.

        Args:
            form_id (str or int): The ID of the form whose submissions are being requested.

        Returns:
            dict: Parsed JSON response from the API containing the form submissions.
        """
        return self._make_request(f"/form/{form_id}/submissions")

    def create_submission(self, form_id: str | int, submission_data: dict[str, str]):
        """
        Create a new submission for a specific form.

        Args:
            form_id (str or int): The ID of the form to which the submission will be added.
            submission_data (dict[str, str]): A dictionary containing the submission field data.
                Each key is a field identifier in the format "submission[field_id]", and each value is the submitted value.

                Example structure:
                    {
                        "submission[2]": "Lorem",
                        "submission[3]": "Ipsum",
                        "submission[4]": "100",
                    }

        Returns:
            dict: Parsed JSON response from the API confirming the creation of the submission and containing its details, including Submission ID.
        """
        return self._make_request(
            f"/form/{form_id}/submissions", method="POST", params=submission_data
        )

    def get_submission(self, submission_id: str | int):
        """
        Retrieve a specific submission by its ID.

        Args:
            submission_id (str or int): The ID of the submission to retrieve.

        Returns:
            dict: Parsed JSON response from the API containing the details of the specified submission.
        """
        return self._make_request(f"/submission/{submission_id}")

    def update_submission(
        self, submission_id: str | int, submission_data: dict[str, str]
    ):
        """
        Update the details of a specific submission.

        Args:
            submission_id (str or int): The ID of the submission to update.
            submission_data (dict[str, str]): A dictionary containing the updated submission field data.
                Each key is a field identifier in the format "submission[field_id]", and each value is the updated field value.

                Example structure:
                    {
                        "submission[2]": "new answer",
                    }

        Returns:
            dict: Parsed JSON response from the API confirming the update and containing the updated submission details.
        """
        return self._make_request(
            f"/submission/{submission_id}", method="POST", params=submission_data
        )

    def delete_submission(self, submission_id: str | int):
        """
        Permanently delete a specific submission.

        Note:
            The submission will NOT be moved to trash; it will be permanently deleted.

        Args:
            submission_id (str or int): The ID of the submission to delete.

        Returns:
            dict: Parsed JSON response from the API confirming the deletion of the submission.
        """
        return self._make_request(f"/submission/{submission_id}", method="DELETE")

    def get_report(self, report_id: str | int):
        """
        Retrieve the details of a specific report by its ID.

        Args:
            report_id (str or int): The ID of the report to retrieve.

        Returns:
            dict: Parsed JSON response from the API containing the details of the specified report.
        """
        return self._make_request(f"/report/{report_id}")

    def delete_report(self, report_id: str | int):
        """
        Permanently delete a specific report.

        Note:
            The report will NOT be moved to trash; it will be permanently deleted.

        Args:
            report_id (str or int): The ID of the report to delete.

        Returns:
            dict: Parsed JSON response from the API confirming the deletion of the report.
        """
        return self._make_request(f"/report/{report_id}", method="DELETE")

    def get_folder(self, folder_id: str):
        """
        Retrieve a specific folder and its contents.

        Args:
            folder_id (str): The ID of the folder to retrieve.

        Returns:
            dict: Parsed JSON response from the API containing details of the folder and its contents.
        """
        return self._make_request(f"/folder/{folder_id}")

    def create_folder(
        self,
        folder_name: str,
        parent_folder_id: Optional[str] = None,
        folder_color: Optional[str] = None,
    ):
        """
        Create a new folder with the specified name, optionally under a parent folder, and with a specified folder color.

        Args:
            folder_name (str): The name of the folder to create.
            parent_folder_id (str, optional): The ID of the parent folder under which to create the new folder.
                If None, the folder will be created at the root level. Defaults to None.
            folder_color (str, optional): A hex color code (e.g., "#FFFFFF") to assign to the folder. Defaults to None.

        Returns:
            dict: Parsed JSON response from the API containing details of the created folder.
        """
        payload: dict[str, Any] = {
            "name": folder_name,
            "parent": parent_folder_id,
            "color": folder_color,
        }
        return self._make_request("/folder", method="POST", params=payload)

    def delete_folder(self, folder_id: str):
        """
        Permanently delete a specific folder.

        Args:
            folder_id (str): The ID of the folder to delete.

        Returns:
            dict: Parsed JSON response from the API confirming the deletion of the folder.
        """
        return self._make_request(f"/folder/{folder_id}", method="DELETE")

    def get_plan(self, plan_name: str):
        """
        Retrieve usage limits and pricing details for a specific plan.

        Args:
            plan_name (str): The name of the plan whose usage limits and pricing are being requested.
                Supported values are: "FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM".

        Returns:
            dict: Parsed JSON response from the API containing usage limits, pricing, and other details of the specified plan.
        """
        return self._make_request(f"/system/plan/{plan_name}")

    def get_apps(self):
        """
        Retrieve a list of apps with basic information available for the current Jotform account.

        Returns:
            dict: Parsed JSON response from the API containing the list of apps and their basic details.
        """
        return self._make_request("/user/portals")

    def get_app(self, app_id: str | int):
        """
        Retrieve detailed information about a specific app.

        Args:
            app_id (str or int): The ID of the app to retrieve.

        Returns:
            dict: Parsed JSON response from the API containing detailed information about the specified app.
        """
        return self._make_request(f"/portal/{app_id}")

    def archive_form(self, form_id: str | int):
        """
        Archive a specific form.

        Args:
            form_id (str or int): The ID of the form to be archived.

        Returns:
            dict: Parsed JSON response from the API confirming the form has been archived.
        """
        return self._make_request(f"/form/{form_id}/archive?archive=1", method="POST")

    def unarchive_form(self, form_id: str | int):
        """
        Unarchive a form.
        """
        return self._make_request(f"/form/{form_id}/archive?archive=0", method="POST")

    def get_submission_thread(self, submission_id: str | int):
        """
        Get the thread of a submission.
        """
        return self._make_request(f"/submission/{submission_id}/thread")

    def generate_pdf(
        self,
        form_id: str | int,
        submission_id: str | int,
        pdf_id: Optional[str | int] = None,
        download: Optional[str | int] = 0,
    ):
        """
        Generate a submission PDF.
        """
        pdf_data: dict[str, Any] = {
            "formid": form_id,
            "submissionid": submission_id,
            "reportid": pdf_id,
            "download": download,
        }
        return self._make_request("/generatePDF", params=pdf_data)

    def get_agents(self):
        """
        Get a list of AI Agents on this Jotform account.
        """
        return self._make_request("/ai-agent-builder/agents")

    def get_agent(self, agent_id: str):
        """
        Get an AI Agent.
        """
        return self._make_request(f"/ai-agent-builder/agents/{agent_id}")

    def get_sender_emails(self):
        """
        Get sender emails on this Jotform account.
        """
        return self._make_request("/smtpConfig/user/all")
