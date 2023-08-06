import numpy as np
import pandas as pd
from prophet import Prophet
from typing_extensions import Self
import pickle
from utility.tele_logger import logger
from utility.resources import log_exception, GetConfiguration
from datahandler.datahandler import DataHandler
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
import itertools

def cv_prophet(param_grid:dict, df: pd.DataFrame, horizon: int = 120) -> dict:
    """
    Performs the cross validation on a given set of parameters' grid

    Parameters
    ----------
    param_grid: dict
        The parameters grid space
    df: pd.DataFrame
        The dataframe on which the cross validation is applied (can be global or train set)
        It must be in the format ('Timestamp', 'target')
    horizon: int, optional
        The horizon for the predictions in evaluate the performance of the cross validation, by default 30

    Returns
    -------
        the dictionary of the best parameters
    """
    mapes = []
    rmses = []
    keys, values = zip(*param_grid.items())
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
    for params in permutations_dicts:
        m =  Prophet_model(params)
        m.model.add_country_holidays('IT')
        m.fit(df)
        df_cv = cross_validation(m.model, horizon = horizon)
        df_p = performance_metrics(df_cv, rolling_window = 1)
        mapes.append(df_p['mape'].values[0])
        rmses.append(df_p['rmse'].values[0])

    weights = [0.5, 0.5]  # Weights assigned to RMSE and MAPE respectively
    composite_metric = weights[0] * np.array(rmses) + weights[1] * np.array(mapes)
    best_params_index = np.argmin(composite_metric)
    best_params = permutations_dicts[best_params_index]
    return best_params


class Prophet_model:
    def __init__(self, dic_param:dict) -> None:
        """
        The class instanciate the prophet model

        Parameters
        ----------
        dic_param: dict
            Dictionary representing the best model parameters 
        """
        logger.info('STEP 2 - Initializing the model class', important = True)
        self.model = Prophet(**dic_param)

    @log_exception(logger)
    def fit(self,
            df: pd.DataFrame, timeline: str = 'Timestamp', target: str = 'Target') -> Self:
        """
        _summary_

        Parameters
        ----------
        df: pd.DataFrame
            It's the DataFrame resulting from preprocessing.py (columns: ['timeline', 'target', 'filled'])
        timeline: str, optional
            timeline column name, by default 'Timeline'
        target: str, optional
            target column name, by default 'Target' (possible values: 'target', 'filled')

        Returns
        -------
            None
        """
        # The input dataset must be in the format output of preprocessing.py
        try:
            assert np.all(np.array(list(df.columns)) == np.array([timeline, target])), "Assertion Error!"
        except AssertionError as e:
            e.args += (f'The columns of the dataset should be {timeline}|{target}|',)
            raise e

        # The df must contain 2 columns ('ds', 'y')
        df_ = df[[timeline,target]].copy()
        df_.columns = ['ds', 'y']
        self.df = df_
        logger.info('STEP 2 - Training the model', important = True)
        self.model.fit(self.df)
        
    def future_dataset(self,
                dic_param: dict) -> pd.DataFrame:
        """
        Generation of the dataset for future forecasting
        The resulting dataset has 1 column: 'ds'

        Parameters
        ----------
        dic_param: dict
            Dictionary of the future parameters (e.g. 'periods', 'freq')

        Returns
        -------
            pd.DataFrame
            The dataframe for the forecasting in the future
        """
        logger.info('STEP 2 - Creation of the future dataset for forecasting')
        return self.model.make_future_dataframe(**dic_param)

    @log_exception(logger)
    def predict(self,
                df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict method 

        Parameters
        ----------
        df: pd.DataFrame
        The dataframe on which the prediction is applied. 
        Possible formats: ('ds') or ('ds', 'y')
            
        Returns
        -------
            pd.DataFrame
            The prophet dataframe for predictions
        """
        # The dataset should be either 2 columns ('ds','y') or 1 column ('ds')
        try:
            assert np.all(np.array(list(df.columns)) == np.array(['ds', 'y'])) or np.all(np.array(list(df.columns)) == np.array(['ds'])), "Assertion Error!"
        except AssertionError as e:
            e.args += ('The columns of the dataset for predicting must be (ds|y) or (ds)',)
            raise e

        logger.info('STEP 2 - Prediction phase')
        return self.model.predict(df)

    @classmethod    
    def save(self,
             path: str,
             model : Prophet = None) -> None:
        r"""Store algorithm to file.
        Parameters
        ----------
        path : str
            path of the file where the algorithm must be stored.
        """
        logger.info('STEP 2 - Saving the model in the ".pkl" format', important = True)

        if model == None:
            model = self.model

        with open(path, 'wb') as file:
            pickle.dump(model, file)

    @log_exception(logger)
    def save_model_results(self, df: pd.DataFrame, filename: str, folder: str = 'models') -> None:
        """
        Method to save the prophet dataframe to file

        Parameters
        ----------
        df: pd.DataFrame
        Dataframe to be saved if 'preprocessed == False'

        filename: str, optional
            filename of the output dataframe to be saved
        
        folder: str, optional
        the folder of ./data in which the results must be saved, default: 'models'

        preprocessed: bool, optional
        It's a flag to specify if the dataset already in the format to be saved ('Timestamp', 'Id_pred', 'Pred_mean', 'Sigma', 'Pi_lower_95', 'Pi_upper_95')
        If False, the dataset is the result of the prophet model and it will be processed
        Returns
        -------
            None
        """
        logger.info('STEP 2 - Saving the model result')
        DH = DataHandler()
        try:
            preproc_df = df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            preproc_df['id_pred'] = ('_').join(filename.split('.')[0].split('_')[:-1])
            preproc_df.columns = ['Timestamp', 'Pred_mean', 'Pi_lower_95', 'Pi_upper_95', 'Id_pred']
            sigma_column = (preproc_df['Pi_upper_95'].copy() - preproc_df['Pi_lower_95'].copy())/2
            preproc_df['Sigma'] = sigma_column
            # sort
            new_preproc_df = preproc_df[['Timestamp', 'Id_pred' ,'Pred_mean', 'Sigma', 'Pi_lower_95', 'Pi_upper_95']]
            # conversion dtype
            new_preproc_df[list(new_preproc_df.columns)[2:]] = new_preproc_df[list(new_preproc_df.columns)[2:]].astype(int) 
        except Exception as e:
            print('The Error is ', e)
            print('Check if the Dataset is the one resulted from prophet predict')
            raise
        DH.write(new_preproc_df, filename = filename, folder = folder)

    @classmethod
    def load(cls,
             path: str) -> Self:
        r"""Load algorithm from file.
        Parameters
        ----------
        path : str
            Path to the file where the algorithm must be stored.
        """
        logger.info('STEP 2 - Loading the model', important = True)
        with open(path, 'rb') as file:
            model_file = pickle.load(file)
        loaded_model = cls({})
        loaded_model.model = model_file
    
        return loaded_model
