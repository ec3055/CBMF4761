import pandas as pd
import argparse
import numpy as np
import random

def concatenate_rows(df1_file, df2_file, df3_file):
    # Load df3 (RNAseq read counts) from csv
    # print(df3.head())
    df3 = pd.read_csv(df3_file,index_col=None)
    print(df3.columns)
    # Load df1 (TF RP score matrix) from txt
    df1 = pd.read_csv(df1_file, sep='\t', header=None, index_col=None)
    # Set df1 columns as index
    # First row contains column names
    df1.columns = df1.iloc[0]
    # Reset index after setting columns
    df1 = df1.iloc[1:].reset_index(drop=True)
    print(df1.columns)

    # Load df2 (initial adjacency matrix) from txt
    df2 = pd.read_csv(df2_file, sep='\t', header=None, index_col=None)
    df2.columns = df2.iloc[0]
    df2 = df2.iloc[1:].reset_index(drop=True)
    print(df2.columns)

    # Get the first string column from df2
    matching_values = df2.iloc[:, 0].astype(str).tolist()

    # Find indices in df3_filtered where the first column values contain any matching_values
    indices = []
    for value in matching_values:
        first_match_index = df3.iloc[:, 0].str.find(value)
        if not first_match_index.empty:
            first_match_index = first_match_index.idxmax()  # Get the index of the first match
            indices.append(first_match_index)

    # Find indices in df3_filtered where any substring of matching_values is contained in the first column
    selected_rows_df3 = df3.loc[indices, :]
    print(selected_rows_df3.iloc[:, 0])

    # Get the column names from df1
    df1_columns = df1.columns.tolist()

    # Filter columns in df3 to only include those present in df1
    df3_filtered = selected_rows_df3[selected_rows_df3.columns.intersection(df1_columns)]

    # Check for column count mismatch between df1 and df3_filtered
    if len(df1_columns) != len(df3_filtered.columns):
        print("cols in df1:",len(df1.columns))
        print("cols in df3:",len(df3_filtered.columns))
        # Get columns present in df1 but missing in df3
        missing_columns = [col for col in df1.columns if col not in df3_filtered]
        print(f"Columns missing in df1 vs df3: {missing_columns}")

        # Get columns in df3 missing in df1 (should not happen due to filtering)
        extra_columns = [col for col in df3_filtered.columns if col not in df1_columns]
        print(f"Unexpected columns in df3: {extra_columns}")

     # Filter columns in df3 to match df1
     df3_columns = df3_filtered.columns.tolist()
     df1_columns = df1.columns.tolist()
     if len(df1_columns) != len(df3_columns):
         if len(df3_columns) < len(df1_columns):
             sampled_columns = random.sample(selected_rows_df3.columns, len(df1_columns))
             df3_filtered = df3_filtered[sampled_columns]

     if len(df1_columns) != len(df3_filtered.columns):
         raise AssertionError("Column count mismatch between df1 and df3")

    # Exclude the first column
    # Reset index of selected rows from df3_filtered to align with df2
    df3_filtered = df3_filtered.reset_index(drop=True)

    # Drop first row
    df3_filtered = df3_filtered.iloc[:, 1:]
    print(df3_filtered.head())
    print("df1 shape:",df1.shape)
    print("df3 shape:",df3_filtered.shape)
    
    # Assert that the shape of selected_rows_df3 matches df1
    assert df3_filtered.shape[0] == df1.shape[0], "Shape mismatch between selected_rows_df3 and df1"

    # Concatenate selected rows from df3_filtered horizontally with df1
    concatenated_df = pd.concat([df1, df3_filtered], axis=1)

    # Drop non-numeric columns (if needed)
    print("concatenated cols before:",len(concatenated_df.columns))
    concatenated_df = concatenated_df.select_dtypes(include=[np.number])  # Select only numeric columns
    print("concatenated cols after:",len(concatenated_df.columns))

    return concatenated_df

def concatenate(base_dir, sample_type):
    df1_file = "{}/{}/10_{}_TF_rp_score.txt".format(base_dir, sample_type, sample_type)
    df2_file = "{}/Adjacency_matrix/{}.txt".format(base_dir, sample_type)
    sample = sample_type.split("_")
    df3_name = sample[0] + "_RNA_" + sample[2]
    df3_file = "{}/RNAseq/{}.csv".format(base_dir, df3_name)
    result_df = concatenate_rows(df1_file, df2_file, df3_file)
    return result_df

# if __name__ == "__main__":

#     # Parse command-line arguments
#     parser = argparse.ArgumentParser(description="Concatenate rows based on matching values from two dataframes")
#     # parser.add_argument("df1_file", type=str, help="Path to first matrix file (TF RP score)")
#     # parser.add_argument("df2_file", type=str, help="Path to second matrix file (adjacency matrix)")
#     # parser.add_argument("df3_file", type=str, help="Path to third dataframe file (RNAseq score)")
#     parser.add_argument("basedir", type=str, help="base dir")
#     parser.add_argument("sample_type", type=str, help="sample type")

#     args = parser.parse_args()

#     # ex. basedir, sample_type
#     # Call concatenate_rows function with provided arguments
#     try:
#         df1_file = "{}/{}/10_{}_TF_rp_score.txt".format(args.basedir, args.sample_type, args.sample_type)
#         df2_file = "{}/Adjacency_matrix/{}.txt".format(args.basedir, args.sample_type)
#         # ALS_RNA_Astro.csv
#         sample = args.sample_type.split("_")
#         df3_name = sample[0] + "_RNA_" + sample[2]
#         df3_file = "{}/RNAseq/{}.csv".format(args.basedir, df3_name)
#         result_df = concatenate_rows(df1_file, df2_file, df3_file)
#         print(result_df)
#     except AssertionError as e:
#         print(f"AssertionError occurred: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
