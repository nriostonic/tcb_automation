import json
import os
import boto3
import requests

# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests#
# Parameters

TONIC_URL = "https://tonic-qa.texascapitalbank.com"


class TonicSession:
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._session = requests.Session()
        self._api_key = api_key
        self._session.headers.update({"Authorization": "Apikey {}".format(api_key)})

    def _get_url(self, api_snippet):
        return "{}{}".format(self._base_url, api_snippet)

    def generate_data(self, workspace_id):
        generate_data_url = self._get_url("/api/generateData/start")
        params = {"workspaceId": workspace_id}

        r = self._session.post(generate_data_url, params=params)

        if r.ok:
            print("Data generation started")
        else:
            r.raise_for_status()

    def generate_data_status(self, workspace_id):
        generate_data_status_url = self._get_url("/api/generateData")
        params = {"workspaceId": workspace_id}

        r = self._session.get(generate_data_status_url, params=params)

        if r.ok:
            print(json.dumps(r.json(), indent=2))
        else:
            r.raise_for_status()

    def get_workspaces(self):
        workspace_list_url = self._get_url("/api/workspace/search")

        r = self._session.get(workspace_list_url)

        if r.ok:
            return r.json()
        else:
            r.raise_for_status()

    def get_filegroups(self, workspace_id):
        get_filegroups_url = self._get_url("/api/FileGroup")

        params = {"workspaceId": workspace_id}

        r  = self._session.get(get_filegroups_url, params=params)

        if r.ok:
            print(json.dumps(r.json(), indent=2))
            return r.json()
        else:
            r.raise_for_status()


    def update_filegroup(self, id, name, workspace_id, bucketName, files_list, quoteChar, nullChar, escapeChar, delimitChar, header):
        update_filegroup_url = self._get_url("/api/FileGroup")
        headers = { 'accept': 'text/plain' , 'Content-Type': 'application/json'}
        print("files list")
        print(files_list)
        files_data = []
        for file in files_list:
            file_entry = {"bucketKeyPair": {
              "bucketName": bucketName,
              "key": file
            }}
            files_data.append(file_entry)

        data = {
            "id": id,
            "name": name,
            "workspaceId": workspace_id,
            "escapeChar": escapeChar,
            "quoteChar": quoteChar,
            "hasHeader": header,
            "delimiter": delimitChar,
            "nullChar": nullChar,
            "files": files_data
        }

        print(data)

        r  = self._session.put(update_filegroup_url, headers=headers, data=json.dumps(data))

        if r.ok:
            print("filegroup updated")
        else:
            r.raise_for_status()



def get_recent_files_from_s3(bucket_name, folder_path, file_type, num_files=5):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # Create a list to hold the filepaths of the most recent files
    filepaths_list = []

     # List all objects in the specified folder
    for obj in bucket.objects.filter(Prefix=folder_path):
        # Check if the object is of the desired file type
        if obj.key.endswith(file_type):
            # Add the object key (file path) to the list
            filepaths_list.append(obj.key)

    # Sort the filepaths list based on the last modified date (newest first)
    filepaths_list.sort(key=lambda x: bucket.Object(x).last_modified, reverse=True)

    # Get the X number of most recent filepaths
    recent_filepaths = filepaths_list[:num_files]

    return recent_filepaths




if __name__ == "__main__":


    client = boto3.client('secretsmanager')

    AWS_RESOURCE = client.get_secret_value(
        SecretId='tonic_qa_api_token',
    )
    TONIC_API_KEY = json.loads(AWS_RESOURCE['SecretString'])['apikey']

    session = TonicSession(TONIC_URL, TONIC_API_KEY)

    with open('parameter.json') as json_queue:
      file_contents = json_queue.read()
    parsed_json = json.loads(file_contents)
    
    deID_Queue = parsed_json['queue']
    for workspace in deID_Queue:
        workspaceId = workspace['WORKSPACE_ID']
        bucketName = workspace['BUCKET']
        folderPath = workspace['FOLDER_PATH']
        numberFiles = workspace['NUMBER_OF_FILES']
        filetype = ""


        print("before get filegruup")

        filegroupList = session.get_filegroups(workspaceId)
        for filegroup in filegroupList:
            fileType = filegroup.get('fileType')
            escapeChar = filegroup.get('escapeChar')
            nullChar = filegroup.get('nullChar')
            delimChar = filegroup.get('delimiter')
            quoteChar = filegroup.get('quoteChar')
            id = filegroup.get('id')
            name = filegroup.get('name')
            header = filegroup.get('hasHeader')
            endsWith = '.' + fileType.lower()
            updatedFiles = get_recent_files_from_s3(bucketName, folderPath, endsWith, numberFiles)
            session.update_filegroup(id, name, workspaceId, bucketName, updatedFiles, quoteChar, nullChar, escapeChar, delimChar, header)
        print('finished updating filegroups')
        session.generate_data(workspaceId)
