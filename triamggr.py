import sys
import json
import requests
import google.auth
from googleapiclient.discovery import build

# Terraform GCP ProviderのドキュメントURL
TERRAFORM_DOCS_URL = "https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources"

def get_terraform_resource_info(resource_name):
    """
    Terraformのリソース情報を取得する
    """
    url = f"{TERRAFORM_DOCS_URL}/{resource_name}.html"
    response = requests.get(url)

    if response.status_code == 200:
        return url  # TerraformのドキュメントURLを返す
    else:
        return None

def get_gcp_iam_permissions():
    """
    gcloud auth の認証情報を利用して GCP IAM API から必要な IAM 権限を取得する
    """
    credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    service = build("iam", "v1", credentials=credentials)

    # IAM ロールのリストを取得
    request = service.roles().list()
    response = request.execute()

    if "roles" in response:
        permissions = {}
        for role in response["roles"]:
            permissions[role["name"]] = role.get("includedPermissions", [])
        return permissions
    else:
        return None

def main():
    # 引数のチェック
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <terraform_resource_name>")
        sys.exit(1)

    resource_name = sys.argv[1]

    # Terraformのリソース情報を取得
    resource_info = get_terraform_resource_info(resource_name)
    if resource_info:
        print(f"\nTerraformリソース情報（{resource_name}）のドキュメントURL:")
        print(resource_info)
    else:
        print("Terraformのリソース情報が見つかりません。")

    # GCP IAM 権限情報を取得
    permissions = get_gcp_iam_permissions()
    if permissions:
        print("\n必要な IAM 権限リスト:")
        for role, perms in permissions.items():
            print(f"Role: {role}")
            for perm in perms:
                print(f"  - {perm}")
    else:
        print("GCP IAM 権限情報が取得できませんでした。")

if __name__ == "__main__":
    main()
