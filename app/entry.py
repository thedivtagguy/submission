from contentful import Client

client = Client(
  '3qun4h5qq7tt',
  'OZAx8f-ZncEnqV27hwF_FBA9I3YxpXtxmFfb6n_bFi4',
  environment='master'  # Optional - it defaults to 'master'.
)

entry = client.entry('cGMSGyWttmfv1RVTaITE3')