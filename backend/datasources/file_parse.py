import pandas as pd

chunk_size = 100000  # Adjust this based on your memory capacity
output_file = 'filtered_data.csv'

# Open the output file in append mode
with open(output_file, 'a', newline='') as f:
    for chunk in pd.read_csv('backend/datasources/companyfacts.csv', chunksize=chunk_size):
        # Filter the chunk
        filtered_chunk = chunk[chunk['entityName'] == 'MORGAN STANLEY']

        # Write the filtered chunk to the file
        filtered_chunk.to_csv(f, header=False, index=False)

        # If you want to see progress, print how many rows we've read
        print(f'{chunk.index[-1]} rows completed')
        

# If you want headers in the output file, and it's the first time writing to it, set header=True
