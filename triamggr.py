import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Terraform GCP ProviderのドキュメントURL
TERRAFORM_DOCS_URL = "https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources"

# GCP IAM ロールのAPIエンドポイント
GCP_IAM_ROLES_URL = "https://cloudresourcemanager.googleapis.com/v1/organizations/ORG_ID:getIamPolicy"

# 認証情報のJSONファイル（GCPのサービスアカウントキー）
SERVICE_ACCOUNT_FILE = "service-account.json"

def get_terraform_resource_info(resource_name):
    """
    Terraformのリソース情報を取得する
    """
    url = f"{TERRAFORM_DOCS_URL}/{resource_name}.html"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text  # TerraformのドキュメントページをHTMLで取得
    else:
        return None

def get_gcp_iam_permissions():
    """
    GCP IAM API を使用して、必要な IAM 権限を取得する
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

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
    # 調べたいTerraformのリソース名
    resource_name = input("Terraformリソース名を入力（例: google_compute_instance）: ")

    # Terraformのリソース情報を取得
    resource_info = get_terraform_resource_info(resource_name)
    if resource_info:
        print(f"\nTerraformリソース情報（{resource_name}）のドキュメントURL:")
        print(f"{TERRAFORM_DOCS_URL}/{resource_name}.html")
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

