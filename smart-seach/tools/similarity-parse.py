
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict


def sentence(data_json, sentence_input):

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Print the primary keys
    for index, key in enumerate(data_json['keys']):

        parent_key = data_json['keys'][index]
        sentence_src = data_json['topics'][parent_key]['field_contexto']

        # Compute embedding for both lists
        input = model.encode(sentence_input, convert_to_tensor=True)
        source = model.encode(sentence_src, convert_to_tensor=True)
        score = util.pytorch_cos_sim(input, source)
        print("parent_key: " + parent_key + " score: " + str(score))

    return 0

def numbers_in_interval(numbers_list, lower_bound, upper_bound):
    result = []
    for number in numbers_list:
        if lower_bound <= number <= upper_bound:
            result.append(number)
    return result


def range_score():
    numbers_list = [0.52, 0.57, 0.51, 0.510,
                    0.8, 0.8300, 0.25, 0.25, 1.3, 2.1, 2.35]
    limits = [
        (0.0, 0.1),
        (0.1, 0.2),
        (0.2, 0.3),
        (0.3, 0.4),
        (0.4, 0.5),
        (0.5, 0.6),
        (0.6, 0.7),
        (0.7, 0.8),
        (0.8, 0.9),
        (0.9, 1.0)
    ]

    selected_ranges = defaultdict(list)

    for lower_limit, upper_limit in limits:
        numbers_in_range = numbers_in_interval(
            numbers_list, lower_limit, upper_limit)
        if len(numbers_in_range) >= 2:
            selected_ranges[(lower_limit, upper_limit)
                            ].extend(numbers_in_range)

    if selected_ranges:
        max_group = max(selected_ranges.items(), key=lambda x: len(x[1]))
        max_range = max_group[0]
        max_numbers = max_group[1]
        max_count = len(max_numbers)
    else:
        max_range = None
        max_numbers = []
        max_count = 0

    print(f"Selected ranges with at least 2 numbers: {selected_ranges}")
    print(f"Maximum group range: {max_range}")
    print(f"Numbers in the maximum group: {max_numbers}")
    print(f"Count of numbers in the maximum group: {max_count}")

# Define a function to interact with the AI model
