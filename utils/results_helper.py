import matplotlib.pyplot as plt


def plot_results_histograms(
        data_set_name,
        centrality_measure,
        results_data_frame,
        selected_columns,
        number_of_bins,
        step_size,
        save_to_disk=False
):
    """
    Plots the histograms for the selected columns.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_data_frame: Dataframe containing all results.
    :param selected_columns: The selected columns for which the histograms are plotted.
    :param number_of_bins: Number of bins for the histogram.
    :param step_size: Step size for creating the bins.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    bins = [i for i in range(0, number_of_bins * step_size + step_size, step_size)]

    results_data_frame_dict = results_data_frame.to_dict()

    for column_key in results_data_frame_dict.keys():
        if column_key in selected_columns:
            plt.title("{0}".format(column_key))
            plt.hist(list(results_data_frame_dict[column_key].values()), bins)
            plt.show()

            if save_to_disk:
                plt.savefig("./results/{0}/{1}/{0}_{2}_histogram".format(
                    data_set_name, centrality_measure, column_key))


def save_results_data_frame(data_set_name, centrality_measure, results_data_frame):
    """
    Creates a .csv file containing all the results

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_data_frame: Dataframe containing all results.
    :return: void
    """

    results_data_frame.to_csv(
        './results/{0}/{1}/{0}_results_{1}.csv'.format(data_set_name, centrality_measure),
        encoding='utf-16'
    )
    print(results_data_frame)
