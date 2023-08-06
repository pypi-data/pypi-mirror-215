from twinthread import TwinThreadClient

username = 'brad.johnson@twinthread.com'
base_url = "https://dev.twinthread.com"

client = TwinThreadClient(base_url=base_url)
client.login(base_url)
client.set_context({"taskId": 7234, "assetModelId": 699})

data = client.get_input_data()

print(data)


