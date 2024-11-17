import json

def delete_keys_from_json(file_path, keys_to_remove, output_file=None):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Function to recursively remove keys
    def remove_keys(obj, keys):
        if isinstance(obj, dict):
            return {k: remove_keys(v, keys) for k, v in obj.items() if k not in keys}
        elif isinstance(obj, list):
            return [remove_keys(item, keys) for item in obj]
        else:
            return obj
    
    # Remove specified keys
    modified_data = remove_keys(data, keys_to_remove)
    
    # Save the modified JSON
    output_file = output_file or file_path  # Save to the same file if no output file is specified
    with open(output_file, 'w') as file:
        json.dump(modified_data, file, indent=4)

    print(f"Keys {keys_to_remove} removed and saved to {output_file}")

# Example usage:
file_path = "/home/jordina/Desktop/datathon24/datathon_participants.json"  # Replace with your JSON file path
keys_to_remove = ["email", "year_of_study", "interests", "objective", "preferred_languages", "availability", "programming_skills", "interest_in_challanges"]  # Replace with keys you want to remove
output_file = "example_modified.json"  # Optional: Specify a different output file

delete_keys_from_json(file_path, keys_to_remove, output_file)
