import json
import argparse
import sys


def classify_field(field_name):
    """Classifies field name into 'boolean', 'list', or 'text'."""
    if field_name.startswith('fl_'):
        return 'boolean'
    if field_name.startswith('ls_'):
        return 'list'
    return 'text'


def compare_records(predicted_record, target_record):
    """Compares fields between a predicted and a target record."""
    results = {
        'boolean': {'correct': 0, 'total': 0},
        'list': {'correct': 0, 'total': 0},
        'text': {'correct': 0, 'total': 0},
    }

    if not isinstance(predicted_record, dict) or not isinstance(target_record, dict):
        print("Warning: Skipping a record because 'content' is not a dictionary.", file=sys.stderr)
        return results

    all_fields = set(predicted_record.keys()) | set(target_record.keys())

    for field in all_fields:
        field_type = classify_field(field)
        results[field_type]['total'] += 1

        pred_val = predicted_record.get(field)
        target_val = target_record.get(field)

        if pred_val == target_val:
            results[field_type]['correct'] += 1

    return results


def main():
    """Main function to load data, run evaluation, and save summary."""
    parser = argparse.ArgumentParser(description="Compare predicted and target JSON datasets.")
    parser.add_argument("predicted_file", help="Path to the predicted JSON file.")
    parser.add_argument("target_file", help="Path to the target (ground truth) JSON file.")
    args = parser.parse_args()

    # Load the list of results from each file
    with open(args.predicted_file, 'r', encoding='utf-8') as f:
        predicted_data = json.load(f)
    with open(args.target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)

    if len(predicted_data) != len(target_data):
        sys.exit("Error: Predicted and target datasets have different numbers of records.")

    # --- MODIFICATION START ---

    # Initialize aggregate results
    total_results = {
        'boolean': {'correct': 0, 'total': 0},
        'list': {'correct': 0, 'total': 0},
        'text': {'correct': 0, 'total': 0},
    }

    # Loop through each record in the lists
    for pred_item, target_item in zip(predicted_data, target_data):
        # Extract the 'content' dictionary from each item
        predicted_content = pred_item.get('content')
        target_content = target_item.get('content')

        # Compare the content and get the results for this record
        record_results = compare_records(predicted_content, target_content)

        # Add the results to the aggregate totals
        for field_type, counts in record_results.items():
            total_results[field_type]['correct'] += counts['correct']
            total_results[field_type]['total'] += counts['total']

    # Calculate and store final accuracies in a dictionary
    summary = {}
    print("--- Evaluation Summary ---")
    for field_type, counts in total_results.items():
        if counts['total'] > 0:
            accuracy = counts['correct'] / counts['total']
            summary[f'{field_type}_accuracy'] = accuracy
            print(f"✔️ {field_type.capitalize()} Fields Accuracy: {accuracy:.2%}")
        else:
            summary[f'{field_type}_accuracy'] = 1.0
            print(f"⚠️ No {field_type.capitalize()} fields found.")

    # Save summary to a file for DVC to track
    output_path = 'data/metrics/metrics.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)

    print(f"\nMetrics saved to {output_path}")

    # --- MODIFICATION END ---


if __name__ == "__main__":
    main()