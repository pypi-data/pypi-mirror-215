import requests
from .helpers import *
from datetime import datetime

class Wrike:
    def __init__(self, base_url: str = "https://www.wrike.com/api/v4", perm_access_token: str = None, ssl_verify: bool = True) -> None:
        """Wrike object. This object defines the parameter every request requires including:
        the base_url, permanent access token, and ssl. This is required to make any api call 
        to Wrike.

        Args:
            base_url (str): Base URL for Wrike API requests.
            perm_access_token (str): Wrike Permanent Access Token.
            ssl_verify (bool): SSL.
        """
        self.base_url = base_url # Check if last character is '/', if so then remove
        self.ssl_verify = ssl_verify
        self.__headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + perm_access_token,
        }
        self.__upload_headers = {
            "content-type": "application/octet-stream",
            "X-Requested-With": "XMLHttpRequest",
            "Authorization": "Bearer " + perm_access_token,
        }
        self.reinitialize()
    
    def reinitialize(self):
        """
        Clears the wrike's object data cache
        """
        self._contacts = None
        self._custom_fields = None
        self._custom_statuses = None
        self._folders = None
        self._workflows = None

   # API Calls -----------------------------------------------
    def query(self, path: str) -> requests.models.Response:
        response = requests.get(
            self.base_url + path,
            headers=self.__headers,
            verify=self.ssl_verify
        )
        return response

    def create(self, path: str) -> requests.models.Response:
        response = requests.post(
            self.base_url + path,
            headers=self.__headers,
            verify=self.ssl_verify,
        )
        return response
    
    def update(self, path: str) -> requests.models.Response:
        response = requests.put(
            self.base_url + path,
            headers=self.__headers,
            verify=self.ssl_verify,
        )
        return response
    
    def delete(self, path: str) -> requests.models.Response:
        response = requests.delete(
            self.base_url + path,
            headers=self.__headers,
            verify=self.ssl_verify,
        )
        return response
    
    def create_files(self, path: str, file_name: str, data: bytes) -> requests.models.Response:
        self.__upload_headers["X-File-Name"] = file_name
        response = requests.post(
            self.base_url + path,
            headers=format(self.__upload_headers, file_name),
            data=data,
            verify=self.ssl_verify
        )
        return response
    
    def update_files(self, path: str, file_name: str, data: bytes) -> requests.models.Response:
        self.__upload_headers["X-File-Name"] = file_name
        response = requests.put(
            self.base_url + path,
            headers=format(self.__upload_headers, file_name),
            data=data,
            verify=self.ssl_verify
        )
        return response
    # --------------------------------------------------------- 

class Webhooks:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Webhooks allow you to subscribe to notifications about changes in Wrike 
        instead of having to rely on periodic polling. When webhooks are in place, 
        a small package of information (“payload”) is sent to your HTTP endpoint 
        when specific changes occur.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def create__folders_folderId_webhooks(self) -> requests.models.Response:
        """Creates a webhook for a target folder/project.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/webhooks"  + self.parameters
        return self.Wrike.create(payload)
    
    def create__spaces_spaceId_webhooks(self) -> requests.models.Response:
        """Creates a webhook for a target space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids + "/webhooks" + self.parameters
        return self.Wrike.create(payload)
    
    def create__webhooks(self) -> requests.models.Response:
        """Creates a webhook for a current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/webhooks" + self.parameters
        return self.Wrike.create(payload)
    
    def query__webhooks(self) -> requests.models.Response:
        """Returns a list of webhooks for current token.

        Returns:
            Requests Response: Response.
        """
        payload = "/webhooks"
        return self.Wrike.query(payload)
    
    def query__webhooks_webhookIds(self) -> requests.models.Response:
        """Returns information for the specified webhooks.

        Returns:
            Requests Response: Response.
        """
        payload = "/webhooks/" + self.ids
        return self.Wrike.query(payload)
    
    def update__webhooks_webhookId(self) -> requests.models.Response:
        """Modifies the webhooks state to suspend or resume. Suspended webhooks do not send notifications.

        Returns:
            Requests Response: Response.
        """
        payload = "/webhooks/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__webhooks_webhookId(self) -> requests.models.Response:
        """Deletes webhook by ID.

        Returns:
            Requests Response: Response.
        """
        payload = "/webhooks/" + self.ids
        return self.Wrike.delete(payload)

class Contacts:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Contacts method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__contacts(self) -> requests.models.Response:
        """List contacts of all users and user groups in current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts" + self.parameters
        return self.Wrike.query(payload)
    
    def query__contacts_contactIds(self) -> requests.models.Response:
        """List contacts of specified users and user groups.

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def query__contacts_contactIds_contacts_history(self) -> requests.models.Response:
        """Query Contacts fields history.

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts/" + self.ids + "/contacts_history" + self.parameters
        return self.Wrike.query(payload)
    
    def update__contacts_contactId(self) -> requests.models.Response:
        """Update contact of requesting user by ID (use 'Modify User' method to update other users). Account Admins may use this method to update group info by group ID. .

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts/" + self.ids + self.parameters
        return self.Wrike.update(payload)

class Users:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Users method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__users_userId(self) -> requests.models.Response:
        """Returns information about single user.

        Returns:
            Requests Response: Response.
        """
        payload = "/users/" + self.ids
        return self.Wrike.query(payload)
    
    def update__users_userId(self) -> requests.models.Response:
        """Update users by ID (accessible to Admins only).

        Returns:
            Requests Response: Response.
        """
        payload = "/users/" + self.ids + self.parameters
        return self.Wrike.update(payload)

class Groups:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Groups method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__groups_groupId(self) -> requests.models.Response:
        """Returns complete information about single group.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def query__groups(self) -> requests.models.Response:
        """Returns all groups in the account.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups/" + self.parameters
        return self.Wrike.query(payload)
    
    def create__groups(self) -> requests.models.Response:
        """Create group in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups" + self.parameters
        return self.Wrike.create(payload)
    
    def update__groups_bulk(self) -> requests.models.Response:
        """Update groups.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups_bulk" + self.parameters
        return self.Wrike.update(payload)
    
    def update__groups_groupId(self) -> requests.models.Response:
        """Update group by id.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__groups_groupId(self) -> requests.models.Response:
        """Delete group by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups/" + self.ids + self.parameters
        return self.Wrike.delete(payload)
        
class Invitations:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Invitations method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__invitations(self) -> requests.models.Response:
        """Get all invitations for current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/invitations" + self.parameters
        return self.Wrike.query(payload)
    
    def create__invitations(self) -> requests.models.Response:
        """Create an invitation into the current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/invitations" + self.parameters
        return self.Wrike.create(payload)
    
    def update__invitations_invitationId(self) -> requests.models.Response:
        """Update invitation by ID and/or resend invitation.

        Returns:
            Requests Response: Response.
        """
        payload = "/invitations/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__invitations_invitationId(self) -> requests.models.Response:
        """Delete invitation by ID.

        Returns:
            Requests Response: Response.
        """
        payload = "/groups/" + self.ids
        return self.Wrike.delete(payload)

class Account:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Account method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__account(self) -> requests.models.Response:
        """Returns current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/account" + self.parameters
        return self.Wrike.query(payload)
    
    def update__account(self) -> requests.models.Response:
        """Update current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/account" + self.parameters
        return self.Wrike.query(payload)
        
class Workflows:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Workflows method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)

    def query__workflows(self) -> requests.models.Response:
        """Returns list of workflows with custom statuses.

        Returns:
            Requests Response: Response.
        """
        payload = "/workflows"
        return self.Wrike.query(payload)
    
    def create__workflows(self) -> requests.models.Response:
        """Create workflow in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workflows" + self.parameters
        return self.Wrike.create(payload)
    
    def update__worflows_workflowId(self) -> requests.models.Response:
        """Update workflow or custom statuses.

        Returns:
            Requests Response: Response.
        """
        payload = "/workflows/" + self.ids + self.parameters
        return self.Wrike.update(payload)

class CustomFields:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Custom Fields method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)

    def query__customfields(self) -> requests.models.Response:
        """Returns a list of custom fields in current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/customfields"
        return self.Wrike.query(payload)
    
    def query__customfields_customfieldIds(self) -> requests.models.Response:
        """Returns complete information about specified custom fields.

        Returns:
            Requests Response: Response.
        """
        payload = "/customfields/" + self.ids
        return self.Wrike.query(payload)
    
    def create__customfields(self) -> requests.models.Response:
        """Create custom field in specified account.

        Returns:
            Requests Response: Response.
        """
        payload = "/customfields" + self.parameters
        return self.Wrike.create(payload)
    
    def update__customfields_customfieldId(self) -> requests.models.Response:
        """Modify custom field.

        Returns:
            Requests Response: Response.
        """
        payload = "/customfields/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
class FoldersProjects:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Folders & Projects method. Folders & projects are one of the main ways to organize, 
        manage, and report on work within Wrike. They both show up in the folder tree in the 
        left-hand Navigation panel of the Wrike Workspace. From the perspective of our data 
        model, projects are essentially folders with additional properties (owners, start & 
        end dates, and status). For instance, the Modify Tasks method allows you to include a 
        task in a specified folder by passing the folder ID in the corresponding parameter. 
        In the same way, you can pass a project ID to include a task in a project.In order to 
        maintain data integrity, it is not possible to run more than one operations in parallel.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)

    def query_folders(self) -> requests.models.Response:
        """Returns list of entries required to build a folder tree for the current account. 
        This list contains the virtual root and recycle bin folders for the account, which can 
        be used as root nodes for trees. Note: when any of query filter parameters are present 
        (e.g. descendants=false, metadata) response is switched to Folder model.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders" + self.parameters
        return self.Wrike.query(payload)

    
    def query__folders_folderId_folders(self) -> requests.models.Response:
        """Returns a list of tree entries for subtree of this folder. For root and recycle 
        bin folders, returns folder subtrees of root and recycle bin respectively.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/folders" + self.parameters
        return self.Wrike.query(payload)
    
    def query__spaces_spaceId_folders(self) -> requests.models.Response:
        """Returns list of entries for subtree of this space.

        Returns:
            Requests Response: Response
        """
        payload = "/spaces/" + self.ids + "/folders" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderIds_folders_history(self) -> requests.models.Response:
        """Query Folders fields history.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/folders_history" + self.parameters
        return self.Wrike.query(payload)
    
    def query_folders_folderIds(self) -> requests.models.Response:
        """Returns complete information about specified folders.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__folders_folderId_folders(self) -> requests.models.Response:
        """Create a folder within a folder. Specify virtual rootFolderId in order to 
        create a folder in the account root.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/folders" + self.parameters
        return self.Wrike.create(payload)
    
    def create__copy_folder_folderId(self) -> requests.models.Response:
        """Copy folder subtree, returns parent folder subtree.

        Returns:
            Requests Response: Response.
        """
        payload = "/copy_folder/" + self.ids + self.parameters
        return self.Wrike.create(payload)
    
    def create__copy_folder_async_folderId(self) -> requests.models.Response:
        """Copy folder subtree, returns async job.

        Returns:
            Requests Response: Response.
        """
        payload = "/copy_folder_async/" + self.ids + self.parameters
        return self.Wrike.create(payload)
    
    def update__folders_folderId(self) -> requests.models.Response:
        """Update folder.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def update__folders_folderIds(self) -> requests.models.Response:
        """Update folders.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__folders_folderId(self) -> requests.models.Response:
        """Move folder and all descendant folders and tasks to Recycle Bin unless 
        they have parents outside of deletion scope.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids
        return self.Wrike.delete(payload)

class Tasks:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Tasks method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__tasks(self) -> requests.models.Response:
        """Search among all tasks in current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_tasks(self) -> requests.models.Response:
        """Search among tasks in the folder.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/tasks" + self.parameters
        return self.Wrike.query(payload)
    
    def query__spaces_spaceId_tasks(self) -> requests.models.Response:
        """Search among tasks in space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids + "/tasks" + self.parameters
        return self.Wrike.query(payload)
    
    def query__tasks_taskIds(self) -> requests.models.Response:
        """Returns complete information about single or multiple tasks.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def query__tasks_taskIds_tasks_history(self) -> requests.models.Response:
        """Query Tasks fields history.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/tasks_history" + self.parameters
        return self.Wrike.query(payload)
    
    def create__folders_folderId_tasks(self) -> requests.models.Response:
        """Create task in folder. You can specify rootFolderId to create task in user's account root.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/tasks" + self.parameters
        return self.Wrike.create(payload)
    
    def update__tasks_taskId(self) -> requests.models.Response:
        """Update task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def update__tasks_taskIds(self) -> requests.models.Response:
        """Update tasks.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__tasks_taskId(self) -> requests.models.Response:
        """Delete task by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids
        return self.Wrike.delete(payload)
    
class Comments:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Comments method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__comments(self) -> requests.models.Response:
        """Get all comments in current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/comments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_comments(self) -> requests.models.Response:
        """Get folder comments.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/comments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__tasks_taskId_comments(self) -> requests.models.Response:
        """Get task comments.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/comments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__comments_commentIds(self) -> requests.models.Response:
        """Get single or multiple comments by their IDs.

        Returns:
            Requests Response: Response.
        """
        payload = "/comments/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__folders_folderId_comments(self) -> requests.models.Response:
        """Create a comment in the folder. The virtual Root and Recycle Bin folders cannot have comments.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/comments" + self.parameters
        return self.Wrike.create(payload)
    
    def create__tasks_taskId_comments(self) -> requests.models.Response:
        """Create comment in task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/comments" + self.parameters
        return self.Wrike.create(payload)
    
    def update__comments_commentId(self) -> requests.models.Response:
        """Update Comment by ID. A comment is available for updates only during the 5 minutes after creation.

        Returns:
            Requests Response: Response.
        """
        payload = "/comments/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__comments_commentId(self) -> requests.models.Response:
        """Delete comment by ID.

        Returns:
            Requests Response: Response.
        """
        payload = "/comments/" + self.ids
        return self.Wrike.delete(payload)

class Dependencies:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Dependencies method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__tasks_taskId_dependencies(self) -> requests.models.Response:
        """Get task dependencies.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/dependencies" + self.parameters
        return self.Wrike.query(payload)
    
    def query__dependencies_dependencyIds(self) -> requests.models.Response:
        """Returns complete information about single or multiple dependencies.

        Returns:
            Requests Response: Response.
        """
        payload = "/dependencies/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__tasks_taskId_dependencies(self) -> requests.models.Response:
        """Add dependency between tasks.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/dependencies" + self.parameters
        return self.Wrike.create(payload)
    
    def update__dependencies_dependencyId(self) -> requests.models.Response:
        """Change relationType of task dependency.

        Returns:
            Requests Response: Response.
        """
        payload = "/dependencies/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__dependencies_dependencyId(self) -> requests.models.Response:
        """Delete dependency between tasks.

        Returns:
            Requests Response: Response.
        """
        payload = "/dependencies/" + self.ids
        return self.Wrike.delete(payload)

class Timelogs:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Timelogs method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__timelogs(self) -> requests.models.Response:
        """Get all timelog records in current account.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelogs" + self.parameters
        return self.Wrike.query(payload)
    
    def query__contacts_contactId_timelogs(self) -> requests.models.Response:
        """Get all timelog records that were created by the user.

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts/" + self.ids + "/timelogs" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_timelogs(self) -> requests.models.Response:
        """Get all timelog records for a folder.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/timelogs" + self.parameters
        return self.Wrike.query(payload)
    
    def query__tasks_taskId_timelogs(self) -> requests.models.Response:
        """Get all timelog records for a task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/timelogs" + self.parameters
        return self.Wrike.query(payload)
    
    def query__timelog_categories_categoryId_timelogs(self) -> requests.models.Response:
        """Get all timelog records with specific timelog category.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelog_categories/" + self.ids + "/timelogs" + self.parameters
        return self.Wrike.query(payload)
    
    def query__timelogs_timelogIds(self) -> requests.models.Response:
        """Get timelog record by IDs.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelogs/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__tasks_taskId_timelogs(self) -> requests.models.Response:
        """Create timelog record for task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/timelogs" + self.parameters
        return self.Wrike.create(payload)
    
    def update__timelogs_timelogId(self) -> requests.models.Response:
        """Update timelog by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelogs/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__timelogs_timelogId(self) -> requests.models.Response:
        """Delete Timelog record by ID.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelogs/" + self.ids
        return self.Wrike.delete(payload)

class TimelogCategories:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Timelog Categories method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__timelog_categories(self) -> requests.models.Response:
        """Get timelog categories in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/timelog_categories"
        return self.Wrike.query(payload)
    
class Attachments:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Attachments method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__attachments(self) -> requests.models.Response:
        """Return all Attachments of account tasks and folders.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_attachmants(self) -> requests.models.Response:
        """Returns all Attachments of a folder.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/attachments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__tasks_taskId_attachments(self) -> requests.models.Response:
        """Returns all Attachments of a task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/attachments" + self.parameters
        return self.Wrike.query(payload)
    
    def query__attachments_attachmentIds(self) -> requests.models.Response:
        """Returns complete information about multiple attachments.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def query__attachments_attachmentId_download(self) -> requests.models.Response:
        """Returns attachment content. It can be accessed via /attachments/id/download/name.ext URL. 
        In this case, 'name.ext' will be returned as the file name.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids + "/download"
        return self.Wrike.query(payload)
    
    def query__attachments_attachmentId_preview(self) -> requests.models.Response:
        """Returns Preview for the attachment. The preview can be accessed via /attachments/id/preview/name.ext 
        URL. In this case, 'name.ext' will be returned as the file name.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids + "/preview" + self.parameters
        return self.Wrike.query(payload)
    
    def query__attachments_attachmentId_url(self) -> requests.models.Response:
        """Public URL to an attachment from Wrike or an external service. The link for attachment 
        from Wrike is valid for 24 hours from when you make the request.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids + "/url"
        return self.Wrike.query(payload)
    
    def create__folders_folderId_attachments(self, file_name: str, data: bytes) -> requests.models.Response:
        """Add an attachment to a folder.

        Args:
            file_name (str): Name and extension of file being uploaded.
            data (bytes): Data in bytes.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/attachments"
        return self.Wrike.create_files(payload, file_name, data)
    
    def create__tasks_taskId_attachments(self, file_name: str, data: bytes) -> requests.models.Response:
        """Add an attachment to a task.

        Args:
            file_name (str): Name and extension of file being uploaded.
            data (bytes): Data in bytes.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/attachments"
        return self.Wrike.create_files(payload, file_name, data)
    
    def update__attachments_attachmentId(self, file_name: str, data: bytes) -> requests.models.Response:
        """Update previously uploaded Attachment with new version.

        Args:
            file_name (str): Name and extension of file being uploaded.
            data (bytes): Data in bytes.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids + self.parameters
        return self.Wrike.update_files(payload, file_name, data)
    
    def delete__attachments_attachmentId(self) -> requests.models.Response:
        """Delete Attachment by ID.

        Returns:
            Requests Response: Response.
        """
        payload = "/attachments/" + self.ids
        return self.Wrike.delete(payload)
    
class Version:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Version method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__version(self) -> requests.models.Response:
        """Returns current API version info.

        Returns:
            Requests Response: Response.
        """
        payload = "/version"
        return self.Wrike.query(payload)

class IDs:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """IDs method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__ids(self) -> requests.models.Response:
        """Convert APIv2 legacy IDs to APIv4 format for specific entity type.

        Returns:
            Requests Response: Response.
        """
        payload = "/ids" + self.parameters
        return self.Wrike.query(payload)

class Colors:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Colors method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__colors(self) -> requests.models.Response:
        """Get color name - code mapping.

        Returns:
            Requests Response: Response.
        """
        payload = "/colors"
        return self.Wrike.query(payload)

class Spaces:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Spaces method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__spaces(self) -> requests.models.Response:
        """Returns a list of spaces.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces" + self.parameters
        return self.Wrike.query(payload)

    def query__spaces_spaceId(self) -> requests.models.Response:
        """Returns info about a space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__spaces(self) -> requests.models.Response:
        """Create a space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces" + self.parameters
        return self.Wrike.create(payload)
    
    def update__spaces(self) -> requests.models.Response:
        """Update a space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__spaces_spaceId(self) -> requests.models.Response:
        """Delete a space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids
        return self.Wrike.delete(payload)

class DataExport:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Data Export method. Data Export API allows you to export all account data for future 
        import to third-party analytics tools (e.g. Tableau or PowerBI). The data is stored in 
        tables, which are connected using foreign key identifiers (like in a relational database). 
        Each table is stored as a separate .csv file, and the API returns a link for each file.

        The CSV file links require authorization similar to all other API methods.

        Documentation for Data Export schema and tables can be found here.

        Data Export takes time to be generated. If it’s the first time you generate a Data Export, 
        a 202 response code is returned and generation starts automatically, so you can access your 
        Export later. After the first time, the Export is automatically updated every day, and a new 
        Export is available through API.

        The API is available to account owners and admins on Enterprise plan with the right to “Export 
        account data”.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__data_export(self) -> requests.models.Response:
        """Get last completed Data Export.

        Returns:
            Requests Response: Response.
        """
        payload = "/data_export"
        return self.Wrike.query(payload)
    
    def query__data_export_exportId(self) -> requests.models.Response:
        """Get Data Export specified by id.

        Returns:
            Requests Response: Response.
        """
        payload = "/data_export/" + self.ids
        return self.Wrike.query(payload)
    
    def query__data_export_schema(self) -> requests.models.Response:
        """Get data export schema specified by version.

        Returns:
            Requests Response: Response.
        """
        payload = "/data_export_schema" + self.parameters
        return self.Wrike.query(payload)
    
    def create__data_export(self) -> requests.models.Response:
        """Forces new data export generation (if it is not in progress already). 202 code is 
        returned in case new export generation is started. Data export can be requested no sooner 
        than 1 hour after last successful data export. If there is fresh data export already, 200 
        code and latest export in format similar to [GET] /data_export is returned.

        Returns:
            Requests Response: Response.
        """
        payload = "/data_export"
        return self.Wrike.create(payload)

class AuditLog:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Audit Log method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__audit_log(self) -> requests.models.Response:
        """Get Audit Log Reports, that contains audit trail for actions in the account. 
        Available to Enterprise admins with "Create user activity reports" right.

        Returns:
            Requests Response: Response.
        """
        payload = "/audit_log" + self.parameters
        return self.Wrike.query(payload)

class AccessRoles:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Access Roles.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__access_roles(self) -> requests.models.Response:
        """Access roles.

        Returns:
            Requests Response: Response.
        """
        payload = "/access_roles"
        return self.Wrike.query(payload)

class AsyncJob:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Async Job method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__async_job_jobId(self) -> requests.models.Response:
        """Get Async job specified by id.

        Returns:
            Requests Response: Response.
        """
        payload = "/async_job/" + self.ids
        return self.Wrike.query(payload)

class Approvals:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Approvals method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__approvals(self) -> requests.models.Response:
        """Reads approvals by filter. When no filter parameters passed returns all approvals shared with a user.

        Returns:
            Requests Response: Response.
        """
        payload = "/approvals" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_approvals(self) -> requests.models.Response:
        """Reads all approvals on folder/project.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/approvals"
        return self.Wrike.query(payload)
    
    def query__tasks_taskId_approvals(self) -> requests.models.Response:
        """Reads all approvals on task.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/approvals"
        return self.Wrike.query(payload)
    
    def query__approvals_approvalIds(self) -> requests.models.Response:
        """Reads approvals by ids.

        Returns:
            Requests Response: Response.
        """
        payload = "/approvals/" + self.ids
        return self.Wrike.query(payload)
    
    def create__folders_folderId_approvals(self) -> requests.models.Response:
        """Create an approval for folder/project. Creates approval in draft status when no 
        approvers assigned. Otherwise creates in pending status. Approvals created via API 
        will not be affected by workflow automation, e.g. task status will not be 
        automatically transitioned when approval finishes.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/approvals"
        return self.Wrike.query(payload)
    
    def create__tasks_taskId_approvals(self) -> requests.models.Response:
        """Create an approval for task. Creates approval in draft status when no approvers 
        assigned. Otherwise creates in pending status. Approvals created via API will not 
        be affected by workflow automation, e.g. task status will not be automatically 
        transitioned when approval finishes.

        Returns:
            Requests Response: Response.
        """
        payload = "/tasks/" + self.ids + "/approvals"
        return self.Wrike.query(payload)
    
    def update__approvals_approvalId(self) -> requests.models.Response:
        """Update approval.

        Returns:
            Requests Response: Response.
        """
        payload = "/approvals/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__approvals_approvalId(self) -> requests.models.Response:
        """Cancel approval.

        Returns:
            Requests Response: Response.
        """
        payload = "/approvals/" + self.ids
        return self.Wrike.delete(payload)

class WorkSchedules:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Work Schedules method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__workschedules(self) -> requests.models.Response:
        """Returns list of all work schedules in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules" + self.parameters
        return self.Wrike.query(payload)
    
    def query__workschedules_workscheduleId(self) -> requests.models.Response:
        """Get work schedule by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules/" + self.ids + self.parameters
        return self.Wrike.query(payload)
    
    def create__workschedules(self) -> requests.models.Response:
        """Create schedule in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules" + self.parameters
        return self.Wrike.query(payload)
    
    def update__workschedules_workscheduleId(self) -> requests.models.Response:
        """Create work schedule in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__workschedules_workscheduleId(self) -> requests.models.Response:
        """Delete work schedule from account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules/" + self.ids
        return self.Wrike.delete(payload)

class CopyWorkSchedules:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Copy Work Schedule method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def create__workschedules_workscheduleId_duplicate(self) -> requests.models.Response:
        """Duplicate work schedule in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules/" + self.ids + "/duplicate" + self.parameters
        return self.Wrike.create(payload)

class WorkSchedulesExceptions:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Work Schedule Exceptions method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__workschedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Get exception by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "workschedule_exclusions/" + self.ids
        return self.Wrike.query(payload)
    
    def query__workschedule_exclusions_exclusionId_workschedule_exclusions(self) -> requests.models.Response:
        """Get all exceptions for given schedule.

        Returns:
            Requests Response: Response.
        """
        payload = "workschedule_exclusions/" + self.ids + "/workschedule_exclusions" + self.parameters
        return self.Wrike.query(payload)

    def create__workschedules_workscheduleId_workschedule_exclusions(self) -> requests.models.Response:
        """Create exception for given schedule.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedules/" + self.ids + "/workschedule_exclusions" + self.parameters
        return self.Wrike.create(payload)
    
    def update__workschedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Update exception by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedule_exclusions/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__workschedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Delete exception by id.

        Returns:
            Requests Response: Response.
        """
        payload = "/workschedule_exclusions/" + self.ids
        return self.Wrike.delete(payload)

class UserSchedulesExceptions:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """User Schedule Exceptions.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__user_schedule_exclusions(self) -> requests.models.Response:
        """Get exceptions for given users and date range.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_schedule_exclusions" + self.parameters
        return self.Wrike.query(payload)
    
    def query__user_schedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Get exception by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_schedule_exclusions/" + self.ids
        return self.Wrike.query(payload)
    
    def create__user_schedule_exclusions(self) -> requests.models.Response:
        """Create new exception for given user.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_schedule_exclusions" + self.parameters
        return self.Wrike.create(payload)
    
    def update__user_schedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Update exception for given user.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_schedule_exclusions/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__user_schedule_exclusions_exclusionId(self) -> requests.models.Response:
        """Delete exception.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_schedule_exclusions/" + self.ids
        return self.Wrike.delete(payload)

class Bookings:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Bookings method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)

    def query__bookings_bookingIds(self) -> requests.models.Response:
        """Get bookings list.

        Returns:
            Requests Response: Response.
        """
        payload = "/bookings/" + self.ids
        return self.Wrike.query(payload)
    
    def query__bookings(self) -> requests.models.Response:
        """Returns list of all bookings in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/bookings" + self.parameters
        return self.Wrike.query(payload)
    
    def query__folders_folderId_bookings(self) -> requests.models.Response:
        """Get bookings from folder.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/bookings" + self.parameters
        return self.Wrike.query(payload)
    
    def create__folders_folderId_bookings(self) -> requests.models.Response:
        """Create Booking.

        Returns:
            Requests Response: Response.
        """
        payload = "/folders/" + self.ids + "/bookings" + self.parameters
        return self.Wrike.create(payload)
    
    def update__bookings_bookingId(self) -> requests.models.Response:
        """Update Booking.

        Returns:
            Requests Response: Response.
        """
        payload = "/bookings/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__bookings_bookingId(self) -> requests.models.Response:
        """Delete booking by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/bookings/" + self.ids
        return self.Wrike.delete(payload)

class JobRoles:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Job Roles method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__jobroles(self) -> requests.models.Response:
        """Returns list of all job roles in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/jobroles"
        return self.Wrike.query(payload)
    
    def query__jobroles_jobroleIds(self) -> requests.models.Response:
        """Get job roles list.

        Returns:
            Requests Response: Response.
        """
        payload = "/jobroles/" + self.ids
        return self.Wrike.query(payload)
    
    def create__jobroles(self) -> requests.models.Response:
        """Create Job Role.

        Returns:
            Requests Response: Response.
        """
        payload = "/jobroles" + self.parameters
        return self.Wrike.create(payload)
    
    def update__jobroles_jobroleId(self) -> requests.models.Response:
        """Create Job Role.

        Returns:
            Requests Response: Response.
        """
        payload = "/jobroles/" + self.ids + self.parameters
        return self.Wrike.update(payload)
    
    def delete__jobroles_jobroleId(self) -> requests.models.Response:
        """Delete job role by Id.

        Returns:
            Requests Response: Response.
        """
        payload = "/jobroles/" + self.ids
        return self.Wrike.delete(payload)

class Placeholders:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Placeholders method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__placeholders(self) -> requests.models.Response:
        """Returns list of all placeholders in account.

        Returns:
            Requests Response: Response.
        """
        payload = "/placeholders"
        return self.Wrike.query(payload)
    
    def query_placeholders_placeholderIds(self) -> requests.models.Response:
        """Get placeholders list.

        Returns:
            Requests Response: Response.
        """
        payload = "/placeholders/" + self.ids
        return self.Wrike.query(payload)

class FolderBlueprints:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Folder Blueprints method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__folder_blueprints(self) -> requests.models.Response:
        """Folder Blueprints tree.

        Returns:
            Requests Response: Response.
        """
        payload = "/folder_blueprints"
        return self.Wrike.query(payload)
    
    def create__folder_blueprints_blueprintId_launch_asyn(self) -> requests.models.Response:
        """Folder Blueprint Launch, returns async job.

        Returns:
            Requests Response: Response.
        """
        payload = "/folder_blueprints/" + self.ids + "/launch_async" + self.parameters
        return self.Wrike.create(payload)

class TaskBlueprints:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Task Blueprints method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__task_blueprints(self) -> requests.models.Response:
        """Task Blueprints.

        Returns:
            Requests Response: Response.
        """
        payload = "/task_blueprints"
        return self.Wrike.query(payload)
    
    def create__task_blueprints_blueprintId_launch_asyn(self) -> requests.models.Response:
        """Task Blueprint Launch, returns async job.

        Returns:
            Requests Response: Response.
        """
        payload = "/task_blueprints/" + self.ids + "/launch_async" + self.parameters
        return self.Wrike.create(payload)

class EDiscovery:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """EDiscovery method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def create__ediscovery_search(self) -> requests.models.Response:
        """Search entities for eDiscovery report.

        Returns:
            Requests Response: Response.
        """
        payload = "/ediscovery_search" + self.parameters
        return self.Wrike.create(payload)

class HourlyRates:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Hourly Rates method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def update__contacts_contactIds_hourly_rates_provision(self) -> requests.models.Response:
        """Provision hourly rates to users. Max 100 users per request.

        Returns:
            Requests Response: Response.
        """
        payload = "/contacts/" + self.ids + "/hourly_rates_provision" + self.parameters
        return self.Wrike.update(payload)

class CustomItemTypes:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """Custom Item Types method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__custom_item_types(self) -> requests.models.Response:
        """Returns all custom item types that belong to the whole account.

        Returns:
            Requests Response: Response.
        """
        payload = "/custom_item_types" + self.parameters
        return self.Wrike.query(payload)
    
    def query__spaces_spaceId_custom_item_types(self) -> requests.models.Response:
        """Returns all custom item types that belong to the specific space.

        Returns:
            Requests Response: Response.
        """
        payload = "/spaces/" + self.ids + "/custom_item_types" + self.parameters
        return self.Wrike.query(payload)
    
    def query__custom_item_types_typeIds(self) -> requests.models.Response:
        """Returns custom item type(s) for specified type ID(s).

        Returns:
            Requests Response: Response.
        """
        payload = "/custom_item_types/" + self.ids
        return self.Wrike.query(payload)
    
    def create__custom_item_types_typeId_instantiate(self) -> requests.models.Response:
        """Create work using the specific custom item type.

        Returns:
            Requests Response: Response.
        """
        payload = "/custom_item_types/" + self.ids + "/instantiate"  +self.parameters
        return self.Wrike.create(payload)

class UserTypes:
    def __init__(self, Wrike: Wrike,  ids: (list or str) = None, parameters: dict = None) -> None:
        """User Types method.

        Args:
            Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            ids (list or str, optional): API request URI string id(s). Defaults to None.
            parameters (dict, optional): API request parameter(s). Defaults to None.
        """
        self.Wrike = Wrike
        self.ids = convert_ids(ids)
        self.parameters = convert_parameters(parameters)
    
    def query__user_types(self) -> requests.models.Response:
        """User types.

        Returns:
            Requests Response: Response.
        """
        payload = "/user_types"
        return self.Wrike.query(payload)

class CloudContentConnector:
    """The Wrike Cloud Content Connector allows you to integrate Wrike with any digital asset management 
    tool or cloud storage through API. Wrike users have the ability to pick assets from DAM or upload 
    approved assets to DAM through Wrike. The platform provides a set of API methods already supported by 
    Wrike that can be implemented on the DAM side for integration. The DAM vendor should implement the 
    connector first in order for end-users to be able to use integrations.
    """
    class Assets:
        def __init__(self, Wrike: Wrike, parameters: dict = None) -> None:
            """Assets method for Cloud Content Connector.

            Args:
                Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
                parameters (dict, optional): API request parameter(s). Defaults to None.
            """
            self.Wrike = Wrike
            self.parameters = convert_parameters(parameters)

        def query__find_assets(self) -> requests.models.Response:
            """Search assets by a text query

            Returns:
                Requests Response: Response.
            """
            payload = "/find-assets" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_asset(self) -> requests.models.Response:
            """Get whole asset model with versions.

            Returns:
                Requests Response: Response.
            """
            payload = "/get-asset" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_download_url(self) -> requests.models.Response:
            """Get a link to original content of an asset version. This link must NOT require 
            authentication. Wrike will not store that link, it can be expiring. Preferably 
            contains a disposition header set for download.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-download-url" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_thumnail_url(self) -> requests.models.Response:
            """Get a link to an image thumbnail of an asset version. This link must NOT require 
            authentication. Wrike will not store that link, it can be expiring.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-thumbnail-url" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_view_url(self) -> requests.models.Response:
            """Get a link to a rendition of an asset version. This link must NOT require 
            authentication. Wrike will not store that link, it can be expiring. Response 
            depends on asset type.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-view-url" + self.parameters
            return self.Wrike.query(payload)

    class Attributes:
        def __init__(self, Wrike: Wrike, parameters: dict = None) -> None:
            """Attributes method for Cloud Content Connector.

            Args:
                Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
                parameters (dict, optional): API request parameter(s). Defaults to None.
            """
            self.Wrike = Wrike
            self.parameters = convert_parameters(parameters)

        def query__find_tags(self) -> requests.models.Response:
            """Search tags by query.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/find-tags" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_all_attributes(self) -> requests.models.Response:
            """Get the whole metadata schema.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-all-attributes"
            return self.Wrike.query(payload)
        
        def query__get_assets_attribute_values(self) -> requests.models.Response:
            """Return values of attribute for an active version of an asset.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-asset-attribute-values" + self.parameters
            return self.Wrike.query(payload)

    class Features:
        def __init__(self, Wrike: Wrike) -> None:
            """Features method for Cloud Content Connector.

            Args:
                Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
            """
            self.Wrike = Wrike
            # self.parameters = convert_parameters(parameters)

        def query__get_dam_features(self) -> requests.models.Response:
            """Returns available features with respective endpoints.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-dam-features"
            return self.Wrike.query(payload)

    class Folders:
        def __init__(self, Wrike: Wrike, parameters: dict = None) -> None:
            """Folders method for Cloud Content Connector.

            Args:
                Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
                parameters (dict, optional): API request parameter(s). Defaults to None.
            """
            self.Wrike = Wrike
            self.parameters = convert_parameters(parameters)
        
        def query__get_folder(self) -> requests.models.Response:
            """Fetches properties of a specific folder, called whenever a user selects or enters a folder.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-folder" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_folder_items(self) -> requests.models.Response:
            """Get items inside a folder.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-folder-items" + self.parameters
            return self.Wrike.query(payload)
        
        def query__get_folder_roots(self) -> requests.models.Response:
            """Get all roots, meaning different hierarchies or folders a user has access to, i.e. collections, 
            brands, lightboxes, categories. Called every time user opens

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-folder-roots"
            return self.Wrike.query(payload)

    class Meta:
        def __init__(self, Wrike: Wrike) -> None:
            """Folders method for Cloud Content Connector.

            Args:
                Wrike (Wrike): Initialize Wrike object. This is used to POST, GET, PUT, and DELETE.
                parameters (dict, optional): API request parameter(s). Defaults to None.
            """
            self.Wrike = Wrike
            # self.parameters = convert_parameters(parameters)
        
        def query__get_current_users(self) -> requests.models.Response:
            """Get current user.

            Returns:
                requests.models.Response: Response.
            """
            payload = "/get-current-user"
            return self.Wrike.query(payload)
        
        def query__meta(self):
            """Does not require authorization. This handler details the exact means of connecting Wrike and DAM. 
            It will be the first handler that will be called from Wrike side. Url of this handler provided by DAM 
            and entered by account administrator in Wrike UI during setting conection as edpoint url.

            Returns:
                _type_: Response.
            """
            payload = "/meta"
            return self.Wrike.query(payload)

class SpecialSyntax:
    def __init__(self) -> None:
        """Initialize the Special Syntax constructor. The Special Syntax constructor
        cleans and formats allowable Wrike HTML.
        """
        pass
    
    def clean_description(self,  html: str) -> str:
        """Task description can be set and received in HTML format with a limited set of tags.
        Cleans description html to strip any HTML tags that are not allowed including
        ["br", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "b", "em", "i", "u", "s", 
        "span", "a", "img", "ol", "ul", "li", "table", "tr", "td"].

        Args:
            html (str): Input a HTML string to clean.

        Returns:
            str: Cleaned HTML string.
        """

        if html == None:
            return ValueError
        else:
            tags = [
                "br", "h1", "h2", "h3", "h4", "h5", "h6",
                "strong", "b", "em", "i", "u", "s", 
                "span", "a", "img", "ol", "ul", "li",
                "table", "tr", "td"
            ]
            return clean_html(tags, html)
    
    def clean_comment(self,  html: str) -> str:
        """Comments can be set and received in HTML format with a limited set of tags.
        Cleans comment html to strip any HTML tags that are not allowed including
        ["br", "a", "blockquote"].

        Args:
            html (str): Input a HTML string to clean.

        Returns:
            str: Cleaned HTML string.
        """
        if html == None:
            return ValueError
        else:
            tags = [
                "br", "a", "blockquote"
            ]
            return clean_html(tags, html)
    
    def mention(self, userID: str, userName: str) -> str:
        """Generate an @mention for a comment.

        Args:
            userID (str): Wrike User Id.
            userName (str): Wrike Username associated with Wrike User Id.

        Returns:
            str: <a class="stream-user-id avatar" rel="userID">@John Doe</a>
        """
        return f'<a class="stream-user-id avatar" rel="{userID}">@{userName}</a>'
    
    def followers(self) -> str:
        """Generate an @followers for a comment.

        Returns:
            str: <a class="stream-user-id avatar quasi-contact" rel="@followers">@followers</a>
        """
        return '<a class="stream-user-id avatar quasi-contact" rel="@followers">@followers</a>'

    def assignees(self) -> str:
        """Generate an @assignees for a comment.

        Returns:
            str: <a class="stream-user-id avatar quasi-contact" rel="@assignees">@assignees</a>
        """
        return '<a class="stream-user-id avatar quasi-contact" rel="@assignees">@assignees</a>'
    
    def quote_comment(self, commentId: str,  userId: str, timestamp: datetime = datetime.timestamp(datetime.now())) -> str:
        """Quote a comment.

        Args:
            commentId (str): Wrike comment id.
            userId (str): Writke user id of comment.
            timestamp (datetime, optional): Timestamp Defaults to current timestampe (datetime.timestamp(datetime.now())).

        Returns:
            str: <blockquote data-entrytype="comment" data-entryid="${Comment ID}" data-user="${User ID}" data-date="${timestamp}">
        """
        return f'<blockquote data-entrytype="comment" data-entryid="{commentId}" data-user="{userId}" data-date="{timestamp}">'
    
    def quote_description(self, entrytype: str, entityId: str, title: str, quoted_part: str) -> str:
        """Quote a description part.

        Args:
            entrytype (str): Entry type. Only valid values are "task" or "folder".
            entityId (str): Task or Folder id.
            title (str): Task or Folder title.
            quoted_part (str): Quoted description part.

        Returns:
            str: <blockquote data-entrytype="[task|folder]" data-entryid="${Task or Folder ID}" data-title="${Task or Folder title}">Quoted description part</blockquote>
        """
        if entrytype.lower() == "task" or entrytype.lower() == "folder":
            return f'<blockquote data-entrytype="{entrytype.lower()}" data-entryid="{entityId}" data-title="{title}">{quoted_part}</blockquote>'
        else:
            return ValueError