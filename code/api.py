import requests

from requestInfo import RequestInfo
from login import login
from get_vdc_id import get_vdc_id
from get_vapp_vm import get_vm_href
from get_vapp_vm import get_vm_id
from get_vapp_vm import get_list_vm_info
from get_vapp_id import get_vapp_uuid

def write_payload_to_file(client, vapp_uuid, vapp_name, vm_list, affinity_rule_name):
    vapp_uuid = get_vapp_uuid(client, vapp_name)
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<root:VmAffinityRule xmlns:root="http://www.vmware.com/vcloud/v1.5">
    <root:Name>sondx12-test</root:Name>
    <root:IsEnabled>true</root:IsEnabled>
    <root:IsMandatory>true</root:IsMandatory>
    <root:Polarity>Anti-Affinity</root:Polarity>
    <root:VmReferences>
        <root:VmReference href="https://hn01vcd.fptcloud.com/api/vApp/vm-ebeffabb-1dff-4b91-bcbe-1f070798adc1" id="vm-ebeffabb-1dff-4b91-bcbe-1f070798adc1" name="sondx12-etu123qw-master-r567wqe1" type="com.vmware.vcloud.entity.vm" />
        <root:VmReference href="https://hn01vcd.fptcloud.com/api/vApp/vm-1436ed7d-a6f3-48eb-89ed-3b886bfd3a42" id="vm-1436ed7d-a6f3-48eb-89ed-3b886bfd3a42" name="sondx12-etu123qw-worker-dloi12er" type="com.vmware.vcloud.entity.vm" />
    </root:VmReferences>
</root:VmAffinityRule>
    """
    file= open(r'payload.txt', 'w')
    file.write(payload)
    file.close()
    for vm in vm_list:
        vm_href = get_vm_href(client, vapp_uuid, vm)
        vm_id = get_vm_id(client, vapp_uuid, vm)
        payload = f"""<root:VmReference href="{vm_href}" id="{vm_id}" name="{vm}" type="com.vmware.vcloud.entity.vm" />
    """
        file = open(r"payload.txt", "a")
        file.write("\t")
        file.write(payload)
        file.close()
    payload = """</root:VmReferences>
</root:VmAffinityRule>"""
    file = open(r"payload.txt", "a")
    file.write(payload)
    file.close()

def anti_affinity_rule(client, vdc_id, vapp_uuid, vapp_name, affinity_rule_name, vm_list):
    write_payload_to_file(client, vapp_uuid, vapp_name, vm_list, affinity_rule_name)
    uri = client.get_api_uri()
    url = f"{uri}/vdc/{vdc_id}/vmAffinityRules/"
    
    file = open(r"payload.txt", "r")
    payload = file.read()
    file.close()

    params = RequestInfo(client)
    resp = requests.post(
        url,
        headers=params.xml_headers,
        data=payload,
        verify=False,
    )
    
    print("response...", resp)
    if not resp.ok:
        raise Exception(resp.content)
    return url

def update_anti_affinity_rule(client, vdc_id, vapp_uuid, vapp_name, affinity_rule_name, vm_list):
    write_payload_to_file(client, vapp_uuid, vapp_name, vm_list, affinity_rule_name)
    uri = client.get_api_uri()
    url = f"{uri}/vdc/{vdc_id}/vmAffinityRules/"
    
    file = open(r"payload.txt", "r")
    payload = file.read()
    file.close()

    params = RequestInfo(client)
    resp = requests.put(
        url,
        headers=params.xml_headers,
        data=payload,
        verify=False,
    )
    
    print("response...", resp)
    if not resp.ok:
        raise Exception(resp.content)
    return 


def main():
    client = login("000023-xplat", "phongvd8", "phongvd8@xplat", "https://hn01vcd.fptcloud.com", "35.0")
    vdc_id = get_vdc_id(client, "XPLAT-VPC")
    vapp_uuid = get_vapp_uuid(client, "sondx12-etu123qw")
    vm_list = ["sondx12-etu123qw-master-r567wqe1", "sondx12-etu123qw-worker-dloi12er"]
    # write_payload_to_file(client, vapp_uuid, "phongvd8", vm_list, "test")
    anti_affinity_rule(client, vdc_id, vapp_uuid, "sondx12-etu123qw", "sondx12-test", vm_list)


if __name__ == '__main__':
    main()
