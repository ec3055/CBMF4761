import pandas as pd

def expand_adj_matrix(df_path):

    df_adj = pd.read_csv(df_path, sep='\t', header=None, index_col=None)
    output_file = df_path.split(".")[0]+"_NEW.txt"
    output_txt_file = df_path.split(".")[0]+"_NEW.TF.list.txt"

    print(df_adj.shape)
    print(len(df_adj.columns))
    # Assuming the first row contains column names
    df_adj.columns = df_adj.iloc[0]
    # Reset index after setting columns
    df_adj = df_adj.iloc[1:].reset_index(drop=True)
    print(df_adj.shape)
    # Get gene target information
    df_target = pd.read_csv("/content/drive/MyDrive/deeptfni/TF_target_binary_matrix.csv")

    # Drop additional name column
    tf_names = df_adj.columns[1:]

    print(df_adj.columns)
    print(df_target.columns)

    # Filter TF columns from the target dataframe that match with TFs in the adjacency matrix
    matching_tfs = [tf for tf in tf_names if tf in df_target.columns]

    # Print TFs present in both dataframes
    print("TFs present in both dataframes:")
    print(matching_tfs)

    # Identify TF columns that exist in df_adj but not in df_target
    missing_tfs_adj = [tf for tf in tf_names if tf not in df_target.columns]
    # Identify TF columns that exist in df_target but not in df_adj
    missing_tfs_target = [tf for tf in df_target.columns if tf not in tf_names]

    # Print mismatched TFs
    print("\nTFs present in df_adj but missing in df_target:")
    print(missing_tfs_adj)
    print("\nTFs present in df_target but missing in df_adj:")
    print(missing_tfs_target)

    tfs = [tf for tf in tf_names if tf in df_target.columns]
    print(tfs)

    relevant_columns = [tf for tf in tf_names if tf in df_target.columns]
    print("relevant columns:",relevant_columns)

    # Filter the relevant columns from the target dataframe
    df_relevant = df_target[relevant_columns]
    print(df_relevant.columns)

    zero_rows = df_relevant[df_relevant.iloc[:, 1:].sum(axis=1) == 0]
    df_relevant = df_relevant[~df_relevant.index.isin(zero_rows.index)]

    # Filter for genes that interact with half or more of the adjacency TFs
    condition = (df_relevant.iloc[:, 1:] == 1).sum(axis=1) > (len(relevant_columns)/2)
    df_relevant = df_relevant[condition]
    df_relevant

    # Reorder columns of df_relevant to match df_adj
    df_relevant_reordered = df_relevant.reindex(columns=df_adj.columns, fill_value=0)

    # Extract gene names from df_target and assign as new column names
    gene_names = df_target.iloc[:, 0]

    # Assign gene names as new column names to df_relevant_reordered
    df_relevant_reordered.columns = ['Gene'] + list(df_relevant_reordered.columns[1:])
    df_relevant_reordered['Gene'] = gene_names
    df_relevant_reordered.reset_index(drop=True, inplace=True)
    df_relevant_reordered

    # Transpose df_relevant_reordered to have genes as columns
    df_transposed = df_relevant_reordered.set_index('Gene').T
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={'index': None}, inplace=True)

    # Drop 'None' column
    if None in df_transposed.columns:
        df_transposed.drop(columns=[None], inplace=True)

    # Convert index (column names) to a list of strings
    new_columns = [str(col) for col in df_transposed.columns]
    df_transposed.columns = new_columns

    df_combined = pd.concat([df_adj, df_transposed], axis=1)
    df_combined

    ############### STOP IF WANT DIRECTED ############### 
    df_combined = pd.concat([df_combined, df_relevant_reordered], ignore_index=True)

    column_to_update = 'TF'
    replacement_column = 'Gene'

    # Calculate length of the 'Gene' column
    # -1 due to Gene column
    gene_column_length = len(df_transposed.columns)-1
    # -1 due to TF column
    tf_column_length = len(df_adj.columns)+gene_column_length-1

    # Determine the number of indices from the end to replace
    num_indices_to_replace = gene_column_length

    # Calculate the indices to replace based on the length of the 'Gene' column
    indices_to_replace = list(range(tf_column_length - num_indices_to_replace, tf_column_length+1))
    print(indices_to_replace)

    # Let replacement happen
    df_combined.loc[indices_to_replace, column_to_update] = df_combined.loc[indices_to_replace, replacement_column]

    if 'Gene' in df_combined.columns:
        df_combined.drop(columns=['Gene'], inplace=True)

    # Fill NaN values with 0
    df_combined = df_combined.fillna(0)
    # Transpose df and reset the index to move column names to the first row
    df_combined.to_csv(output_file, sep='\t', index=False)
    # Read in again with index_col=0 for compatibility
    # This is final csv output
    df_ = pd.read_csv(output_file, sep="\t",index_col=0)

    tf_list = df_combined['TF'].tolist()
    
    # Output new TF list
    def write_list_to_txt(lst, file_path):
        with open(file_path, 'w') as f:
            for item in lst:
                f.write(str(item) + '\n')
        print(f"List successfully written to {file_path}")

    write_list_to_txt(tf_list, output_txt_file)

    return df_
