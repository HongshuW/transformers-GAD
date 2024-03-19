import torch


def get_reweigh_factor():
    p_1_1 = 3.175825986545533e-05
    p_1_0 = 2.0020976080559194e-05
    p_2_1_given_1 = 0.17334003746509552
    p_2_0_given_1 = 0.22081588208675385
    p_2_0_given_0 = 0.25583988428115845
    p_3_1_given_11 = 0.2095051109790802
    p_3_0_given_11 = 0.06769692897796631
    p_3_1_given_10 = 0.1298251450061798
    p_3_0_given_10 = 0.11201044172048569
    p_3_0_given_00 = 0.21392203867435455

    # Calculating P values using the corrected interpretation for time steps
    P_111 = p_1_1 * p_2_1_given_1 * p_3_1_given_11
    P_110 = p_1_1 * p_2_1_given_1 * p_3_0_given_11
    P_101 = p_1_1 * p_2_0_given_1 * p_3_1_given_10
    P_100 = p_1_1 * p_2_0_given_1 * p_3_0_given_10
    P_000 = p_1_0 * p_2_0_given_0 * p_3_0_given_00

    # Calculating w^s values
    w_s_r = P_111 + P_110 + P_101 + P_100 + P_000
    w_s_a = (p_2_1_given_1) * ((p_3_1_given_11) + (p_3_0_given_11)) + (p_2_0_given_1) * (
            (p_3_1_given_10) + (p_3_0_given_10))
    w_s_b = (p_3_1_given_11) + (p_3_0_given_11)
    w_s_c = (p_3_1_given_10) + (p_3_0_given_10)
    w_s_d = p_2_0_given_0 * p_3_0_given_00
    w_s_e = p_3_0_given_00
    w_s_R = w_s_r
    w_s_T = (w_s_a + w_s_b + w_s_c) / 3
    w_s_Z = (w_s_d + w_s_e) / 2
    # Building the dictionary
    success_rates = {
        "root": w_s_r,
        "a": w_s_a,
        "b": w_s_b,
        "c": w_s_c,
        "d": w_s_d,
        "e": w_s_e,
        "R": w_s_R,
        "T": w_s_T,
        "Z": w_s_Z
    }

    # Display the success rates
    for non_terminal, success_rate in success_rates.items():
        print(f"{non_terminal}: {success_rate}")

    theta_1_1 = w_s_a / w_s_r
    theta_1_0 = w_s_d / w_s_r
    theta_2_1_given_1 = w_s_b / w_s_a
    theta_2_0_given_1 = w_s_c / w_s_a
    theta_2_0_given_0 = w_s_e / w_s_d
    theta_3_1_given_11 = 1 / w_s_b
    theta_3_0_given_11 = 1 / w_s_b
    theta_3_1_given_10 = 1 / w_s_c
    theta_3_0_given_10 = 1 / w_s_c
    theta_3_0_given_00 = 1 / w_s_e

    # Input IDs
    id_1 = 28740
    id_0 = 28734

    # Mapping input IDs to theta values
    sequence_to_theta = {
        (id_1,): theta_1_1,
        (id_0,): theta_1_0,
        (id_1, id_1): theta_2_1_given_1,
        (id_1, id_0): theta_2_0_given_1,
        (id_0, id_0): theta_2_0_given_0,
        (id_1, id_1, id_1): theta_3_1_given_11,
        (id_1, id_1, id_0): theta_3_0_given_11,
        (id_1, id_0, id_1): theta_3_1_given_10,
        (id_1, id_0, id_0): theta_3_0_given_10,
        (id_0, id_0, id_0): theta_3_0_given_00,
    }

    avg_sequence_to_theta = {
        (id_1,): w_s_R,
        (id_0,): w_s_R,
        (id_1, id_1): w_s_T,
        (id_0, id_0): w_s_Z,
        (id_1, id_1, id_1): w_s_T,
        (id_1, id_1, id_0): w_s_T,
        (id_1, id_0, id_1): w_s_T,
        (id_1, id_0, id_0): w_s_T,
        (id_0, id_0, id_0): w_s_Z,
    }
    return sequence_to_theta, avg_sequence_to_theta, w_s_R, w_s_T, w_s_Z

def get_theta_for_token(input_ids, token_id, w_s_R, w_s_T, w_s_Z):
    # TODO: Implement a method to get theta for a specific token, only apply for 01 strings
    generated_start_idx = 24
    # Ensure there's at least one generated token
    if input_ids.size(1) > generated_start_idx:
        # Extract the first generated token ID for each sequence in the batch
        first_generated_token_ids = input_ids[:, generated_start_idx]

        # Initialize an empty tensor for theta values
        theta = torch.empty(first_generated_token_ids.size(0), dtype=torch.float)

        # Loop over each token to determine the correct theta value
        for i, token_id in enumerate(first_generated_token_ids):
            if token_id == 28740:
                theta[i] = w_s_T
            elif token_id == 28734:
                theta[i] = w_s_Z
            else:
                # If the token ID does not match any expected value, raise an error
                raise ValueError(f"Unexpected input ID: {token_id.item()}")
    else:
        # If there are no generated tokens, use the default w_s_R for all sequences in the batch
        theta = torch.full((input_ids.size(0),), w_s_R, dtype=torch.float)

    return theta

if __name__ == "__main__":
    tensor = torch.tensor([[ 1739,   264, 10865, 13892, 28723, 26075,   264,  5509, 10136,  1423,
               302,  3575, 28705, 28770, 28804,  6055,   346,  1347,   272,  7138,
              1423,  1671, 13268, 28723]])

    # Get the length of the sequence
    length = tensor.size(1)
    start_idx = 24
    generated_ids = tensor[:, start_idx:]  # '1' refers to the second dimension

    print("generated_ids:", generated_ids)
    print("length:", length)
    sequence_to_theta, avg_sequence_to_theta, w_s_R, w_s_T, w_s_Z = get_reweigh_factor()
    print("sequence_to_theta:", sequence_to_theta)
    print("avg_sequence_to_theta:", avg_sequence_to_theta)
    print("w_s_R:", w_s_R)
    print("w_s_T:", w_s_T)
    print("w_s_Z:", w_s_Z)

    # Get the theta values for the generated tokens
    theta = get_theta_for_token(tensor, 28740, w_s_R, w_s_T, w_s_Z)
    print("theta:", theta)

