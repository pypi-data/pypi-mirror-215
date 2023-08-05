# WrikePy
WrikePy is a Python Wrapper for the [Wrike.com](https://www.wrike.com/) API.

## Getting Started
### Import WrikePy
```python
from WrikePy import *
```
### Initialize API
Every Wrike API call requires a Wrike object parameter in order to send a request.
```python
wrike = Wrike(base_url, perm_access_token, ssl_verify)
```
 - The **base_url** parameter is the base URL for every Wrike API
   request. The default value is "https://www.wrike.com/api/v4". 
 - The **perm_access_token** parameter is the API key that you generate from your Wrike account (Apps & Integrations >  API). The default value is "None".
  - The **ssl_verify** parameter is a security feature that comes
   with secure urls. The default value is "True".
### Wrike API
The format of WrikePy mirrors that of the [Wrike API](https://developers.wrike.com/) documentation methods. WrikePy includes a class for each API method and a function for each API call type. As an example, the following will get a folders and/or projects from within a folder...
```python
folders = FoldersProjects(wrike, ["folderId"], {"paramKey": "paramValue"}).query__folders_folderId_folders()
```
### Function Naming Conventions
Functions following the naming conventions put forth in the API documentation.
| Name | Request Type |
|--|--|
| query__ | GET |
| create__ | POST |
| update__ | PUT |
| delete__ | DELETE |
| create_files__ | POST (Upload Files) |
| update_files__ | PUT (Update Files) |
