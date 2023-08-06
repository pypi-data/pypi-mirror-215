import numpy as np
import pandas as pd
import gpflow


class WindowGenerator:
    """Generates windows of input and label data from a given dataframe.

        Args:
            input_width (int): Width of the input window.
            label_width (int): Width of the label window.
            shift (int): Number of steps to shift the window.
            label_columns (list): List of column names to be used as labels (default: None).

        Attributes:
            data (numpy.ndarray or None): Data values of the dataframe.
            label_columns_indices (dict or None): Dictionary mapping label column names to indices.
            input_width (int): Width of the input window.
            label_width (int): Width of the label window.
            shift (int): Number of steps to shift the window.
            total_window_size (int): Total size of the window including both input and label.
            label_columns (list): List of column names to be used as labels.
            input_slice (slice): Slice object for selecting input data from the window.
            input_indices (numpy.ndarray): Array of indices for selecting input data from the window.
            label_start (int): Starting index of the label data in the window.
            labels_slice (slice): Slice object for selecting label data from the window.
            label_indices (numpy.ndarray): Array of indices for selecting label data from the window.

        Methods:
            split_window(index): Splits the window into input and label data for the given index.
            make_dataset(dataframe): Creates the dataset by splitting the dataframe into input and label data.

        """
    def __init__(self,
                 input_width: int,
                 label_width: int,
                 shift: int,
                 label_columns: list = None) -> None:

        self.data = None
        self.label_columns_indices = None
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.total_window_size = input_width + shift

        self.label_columns = label_columns

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, self.total_window_size)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def split_window(self,
                     index: int = 0) -> tuple:

        features = self.data
        inputs = features[index + self.input_indices]
        labels = features[index + self.label_indices]

        if self.label_columns is not None:
            labels = np.stack(
                [labels[:, self.label_columns_indices[name]] for name in self.label_columns],
                axis=-1
            )

        return inputs, labels

    def make_dataset(self, dataframe: pd.DataFrame) -> tuple:

        self.label_columns_indices = {name: j for j, name in
                                      enumerate(dataframe.columns)}
        self.data = dataframe.values
        n_samples, n_feats = dataframe.shape
        real_samples = n_samples - self.total_window_size + 1

        x_data = np.empty(
            shape=(real_samples, n_feats * self.input_width)
        )
        y_data = np.empty(
            shape=(real_samples, self.label_columns.__len__() * self.label_width)
        )

        for index in range(real_samples):
            inputs, labels = self.split_window(index=index)
            x_data[index] = inputs.ravel()
            y_data[index] = labels.ravel()

        return x_data, y_data

    def __repr__(self):
        label_columns = ", ".join(str(label) for label in self.label_columns)
        return ("\033[1mWindow Information\033[0m\n"
                f"Total window size: {self.total_window_size}\n"
                f"Input indices: {self.input_indices}\n"
                f"Label indices: {self.label_indices}\n"
                f"Label column name(s): {label_columns}\n")


def load_data(filename):
    """Loads data from an Excel file.

     Args:
         filename (str): Name of the Excel file.

     Returns:
         pandas.DataFrame: Loaded data.

     """
    return pd.read_excel(
        io="./" + filename + ".xlsx"
    ).fillna(0.0)


def normalize_data(dataframe: pd.DataFrame) -> tuple:
    """Normalizes the data by subtracting the mean and dividing by the standard deviation.

        Args:
            dataframe (pandas.DataFrame): Input data.

        Returns:
            tuple: Tuple containing the normalized data, mean, and standard deviation.

        """
    mean = dataframe.mean()
    std = dataframe.std()
    norm_dataset = (dataframe - mean) / std
    norm_dataset.fillna(0.0, inplace=True)

    return norm_dataset, mean.to_numpy(), std.to_numpy()


class HydroGPower:
    """HydroGPower class for training and predicting using GP models.

    Args:
        filename (str): Name of the data file.
        horizont (int): Prediction horizon.
        M (int): Number of inducing points.
        seed (int): Random seed for reproducibility.

    Attributes:
        horizont (int): Prediction horizon.
        data_mean (numpy.ndarray): Mean values of the input data.
        data_std (numpy.ndarray): Standard deviation values of the input data.
        norm_data (pandas.DataFrame): Normalized input data.
        train_data (tuple): Tuple containing the training input and label data.
        gp_model (gpflow.models.SVGP): GP model for prediction.

    Methods:
        train_model(): Trains the GP model.
        predict(filename="results"): Performs prediction and saves the results to an Excel file.

    """
    def __init__(
            self,
            filename,
            horizont,
            M,
            seed=None
    ):
        self.horizont = horizont
        rng = np.random.default_rng(seed)
        data = load_data(filename)

        # Normalize data
        self.norm_data, self.data_mean, self.data_std = normalize_data(data)

        # Create time widowing
        window = WindowGenerator(
            input_width=1,
            label_width=horizont,
            shift=horizont,
            label_columns=data.columns
        )

        # Create dataset
        X, Y = window.make_dataset(self.norm_data)
        self.train_data = (X, Y)
        N, P = Y.shape
        D = X.shape[1]

        # Crate the GPModel
        Z = rng.choice(X, size=M, replace=False)  # Get initial inducing points
        kernel_list = [gpflow.kernels.SquaredExponential(lengthscales=[1] * D) for _ in range(P)]
        kernel = gpflow.kernels.SeparateIndependent(kernel_list)
        iv = gpflow.inducing_variables.SharedIndependentInducingVariables(
            gpflow.inducing_variables.InducingPoints(Z)
        )
        self.gp_model = gpflow.models.SVGP(kernel, gpflow.likelihoods.Gaussian(), inducing_variable=iv,
                                           num_latent_gps=P)
        print(window)

    def train_model(self):
        loss = gpflow.models.training_loss_closure(self.gp_model, self.train_data)
        opt = gpflow.optimizers.Scipy()
        opt.minimize(loss, self.gp_model.trainable_variables,
                     method="l-bfgs-b")

    def predict(self, filename="results"):
        X_test = self.norm_data.iloc[-1:].values
        y_mean_norm, y_var_norm = self.gp_model.predict_y(X_test)
        y_mean = self.data_std * y_mean_norm.numpy().reshape(self.horizont, -1) + self.data_mean
        y_std = self.data_std * np.sqrt(y_var_norm.numpy().reshape(self.horizont, -1))

        index_range = [i + 1 for i in range(self.horizont)]
        df_mean = pd.DataFrame(y_mean, columns=self.norm_data.columns, index=index_range)
        df_mean.index.name = "Day ahead"
        df_std = pd.DataFrame(y_std, columns=self.norm_data.columns, index=index_range)
        df_std.index.name = "Day ahead"

        try:
            with pd.ExcelWriter("./" + filename + ".xlsx",
                                mode='a', if_sheet_exists="replace") as writer:
                df_mean.to_excel(writer, sheet_name="mean")
                df_std.to_excel(writer, sheet_name="std")
        except FileNotFoundError:
            with pd.ExcelWriter("./" + filename + ".xlsx",
                                mode='w') as writer:
                df_mean.to_excel(writer, sheet_name="mean")
                df_std.to_excel(writer, sheet_name="std")
        print(f"\033[1mResults saved at {filename}.xlsx file.\033[0m\n")


def main():
    hydrogpower = HydroGPower(
        filename="dataset_example",
        horizont=5,
        M=2,
        seed=1234
    )
    hydrogpower.train_model()
    hydrogpower.predict()


if __name__ == "__main__":
    main()
