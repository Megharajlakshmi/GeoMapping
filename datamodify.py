# Read the input file
def transform_log_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_num, line in enumerate(infile):
            # Process the header line
            if line_num == 0:
                outfile.write(line.replace(';', ',').strip() + '\n')
                continue

            # Split the line into columns using ';'
            columns = line.strip().split(';')

            # Extract and clean the first column (time)
            time_parts = columns[0].split(' - ')
            if len(time_parts) == 2:
                columns[0] = time_parts[1]

            # Join the columns with ',' and write to the output file
            transformed_line = ', '.join(col.strip() for col in columns)
            outfile.write(transformed_line + '\n')

input_file = 'data/log_input.txt'
output_file = 'log_output.txt'

transform_log_file(input_file, output_file)

print(f"Transformed log file saved to {output_file}")