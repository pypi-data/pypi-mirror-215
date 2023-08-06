import numpy as np
import pandas as pd
from datetime import datetime
import holidays
from utility.tele_logger import logger
from datahandler.datahandler import DataHandler
from utility.resources import *
import os
# import shutil
import sys


dict_regioni = {

                        30: 'Lombardia',190: 'Sicilia',50: 'Veneto',80: 'Emilia-Romagna',120: 'Lazio',200: 'Sardegna',

                        150: 'Campania',10: 'Piemonte',42: 'Trento',70: 'Liguria',130: 'Abruzzo',100: 'Umbria',

                        180: 'Calabria',160: 'Puglia',110: 'Marche',90: 'Toscana',20: "Valle D'Aosta",170: 'Basilicata',

                         60: 'Friuli-Venezia-Giulia',41: 'Bolzano',140: 'Molise'

                         }

dict_spec = {
                "Cardiologia": 2,"Chirurgia Vascolare": 5, "Endocrinologia": 9,
                "Neurologia": 15, "Oculistica": 16, "Ortopedia": 19,
                "Ginecologia": 20, "Otorinolaringoiatra": 21, "Urologia": 25,
                "Dermatologia": 27, "Fisiatria": 12,"Gastroenterologia": 10,"Oncologia": 18,"Pneumologia": 22
            }

dict_spec_reversed = {v:k for k,v in dict_spec.items()}



def get_path_and_make_root(folder_name = str) -> str:

    """ Creates the folder where data used to feed the model will be saved

    Parameters
    folder_name: str
        Name of the folder to create

    Returns
    -------
    str:
       path of the folder where data will be saved 
        
    
    """
    
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.split(os.path.split(path)[0])[0] + "/data/output/"
    
    os.makedirs(path + folder_name, exist_ok=True)
    return path + folder_name


def code_to_name(cod: pd.Series, convers_dict: dict) -> pd.Series:
    """
    The function generates a new column converting the code number into a meaningful string

    Parameters
    ----------
    cod: pd.Series
       The code number column
    convers_dict: dict
        The mapping dictionary from code to string

    Returns
    -------
        pd.Series
        Returns the modified column based on the mapping dictionary
    """
    return cod.apply(lambda i: convers_dict[int(i)])

def generating_target(df: pd.DataFrame,
                      col_index: list,
                      target_col: str) -> pd.DataFrame:
        
        """ Creates the timeseries target

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the fixed ennuple and date column used to generate timeseries 

        col_index: list
            column names identifying the columns to  aggregate on

        target_col: str
            column name identifying the target (e.g.: id_teleconsulto)

        Returns
        -------
        grouped_df: pd.DatFrame 
            Dataframe with the aggregation

        """
        
        grouped_df = df.groupby(col_index).agg(target = (target_col,"count")).reset_index()

        return grouped_df

def from_timestamp_to_date(df: pd.Series) -> pd.Series:
        """  
        Extract the date from datetime

        Parameters
        ----------
        df: pandas.Series 
            Pandas.series object identifying datetime to convert

        Returns
        -------
        to_date: pandas.Series 
            pandas.Series datetime64[ns] object identifying date

        """  

        # to_date = df.dt.date
        to_date = pd.to_datetime(df.dt.date)

        return to_date
    
    
def resample_date(df: pd.DataFrame,
                  s: str) -> pd.DataFrame:

        """Creates the entire daily time series in a fixed datetime range 

        Parameters
        ----------
        df: pd.DataFrame
           pandas DataFrame from which resample time-series data

        Returns
        -------
        s: pd.DataFrame 
           Resampled time-series data

        """
        
        return df.set_index('timeline').resample(s).sum().reset_index()

class NotEnoughDataPoints(Exception):
    """Thrown when the data points inside the dataframe are less than or equal to 1"""
    pass

class Preprocessing_Prophet:

    @log_exception(logger)
    def __init__(self,
                #  df: pd.DataFrame,
                 raw_filename: str = None,
                 regione: str = None,
                 asl: str = None,
                 branca: str = None,
                 to_delete = False
                 ):
    
        """
        Preprocessing class

        Parameters
        ----------
        df: pd.DataFrame
        The original dataframe
            
        regione: str
        name of the first level of hierarchy. It could be None, meaning Italy, or one from Italian regions name
        
        asl: str
        name of the second level of hierarchy, valued only if "regione" is not None, indicating an "asl"
        of the specified region

        branca: str
        name of the third level of hierarchy, valued only if both "regione" and "asl"  aren't None, indicating
        a medical branch of the specified region-asl pair

        to_delete: bool
        Flag to set files overwriting

        """

        global dict_regioni
        global dict_spec_reversed

        if raw_filename == None:
            for f in os.listdir(os.path.join(DataHandler().data_folder, 'input')):
                if f.endswith('.parquet'):
                    raw_filename = f
                    break

        path = get_path_and_make_root(folder_name =  "prophet/")
        
        self.path = path
        self.regione = [regione.title() if regione !=None else regione][0]
        self.asl = [asl.upper() if asl!= None else asl][0]
        self.branca = [branca.title() if branca !=None else branca][0]
        self.to_delete = to_delete

        self.params = {}
        self.params = GetConfiguration("input_parameters_prophet")
        # self.df = df
        self.df = DataHandler().read(filename=raw_filename, folder='input')
        self.df["regione"] = code_to_name(self.df[self.params["spatial_hierarchy"]],dict_regioni)
        self.df["specializzazioni"] = code_to_name(self.df[self.params["specialty_index"]],dict_spec_reversed)


        return 

    def generating_files_according_to_hierarchy(self) -> list:

        """Create folders and data files according to the specified input hierarchy 

        Returns:
        list: 
            list of created-folders paths
        """

        if all( x is None for x in [self.regione, self.asl, self.branca]):
            os.makedirs(self.path, exist_ok=True)
            path_to_save = self.path
            path_list = []
            path_list += self.making_subfolders_writing_files(
                                                    self.df,
                                                    path_to_save,
                                                    to_delete = self.to_delete
                                                    )

            path_list += self.making_subfolders_writing_files(
                                                    self.df,
                                                    path_to_save,
                                                    "regione",
                                                    to_delete=self.to_delete)

        elif self.regione != None and self.asl == None:
            os.makedirs(self.path + self.regione + "/", exist_ok=True)
            path_list=[]
            path_to_save = self.path + self.regione + "/"
            df_ = self.df[self.df["regione"]==self.regione].reset_index(drop=True)

            path_list += self.making_subfolders_writing_files(
                                        df_,
                                        path_to_save,
                                        filename=self.regione + ".parquet",
                                        to_delete = self.to_delete)
            
            path_list += self.making_subfolders_writing_files(
                                                    df_,
                                                    path_to_save,
                                                    self.params["spatial_sub_hierarchy"],
                                                    to_delete = self.to_delete)
            
        elif self.regione != None and self.asl != None:
            os.makedirs(self.path + self.regione +"/"+ self.asl + "/", exist_ok=True)
            path_list=[]
            path_to_save = self.path + self.regione + "/" + self.asl + "/"
            df_ = self.df[(self.df["regione"]==self.regione) & \
                        (self.df[self.params["spatial_sub_hierarchy"]]==self.asl)].reset_index(drop=True)
            if df_.shape[0] <=1:
                logger.error("No enough data: check your input")
                raise NotEnoughDataPoints

            path_list += self.making_subfolders_writing_files(
                                        df_,
                                        path_to_save,
                                        filename=self.asl + ".parquet",
                                        to_delete = self.to_delete)
            
            path_list += self.making_subfolders_writing_files(
                                                    df_,
                                                    path_to_save,
                                                    "specializzazioni",
                                                     to_delete = self.to_delete)
        return path_list

    def making_subfolders_writing_files(self,
                                    df_: pd.DataFrame,
                                    path: str,
                                    hier_col: str = None,
                                    to_delete: bool = False,
                                    filename = "Italia.parquet") -> list:
        
        """Writes a pandas DataFrame into the selected folder. Supported extension is parquet

        Parameters
        ---------- 
        df_: pd.DataFrame
        Dataframe from which to generate the timeseries 

        path: str
        path to the root folder where to generate subfolders and save files
            
        hier_col: str 
        Column name indicating the hierarchy level for which to create folders.

        filename: str
        If hier_col is not specified, filename of the parquet to save


        Returns:
            list: 
                list of created-folders paths
        """
        path_list = []
        DH = DataHandler()
        if hier_col != None:

            list_dir_to_make = list(df_[hier_col].unique())
            for folder in list_dir_to_make:
                os.makedirs(path + folder + "/", exist_ok=True)
                file_to_save = path + folder + "/" + folder + ".parquet"
                isExisting = os.path.exists(file_to_save)

                if not isExisting:
                    temp = df_[df_[hier_col] == folder].reset_index(drop=True)
                    df_sub = self.execute(temp)
                    logger.info('non cè niente ->' + file_to_save)
                    DH.write(df_sub, file_to_save)
                elif isExisting == True and to_delete == True:
                    os.remove(file_to_save)
                    temp = df_[df_[hier_col] == folder].reset_index(drop=True)
                    df_sub = self.execute(temp)
                    logger.info('cè qualcosa ->' +file_to_save)
                    DH.write(df_sub, file_to_save)
                else:
                    continue
                path_list.append(path + folder + "/")
                

        else:
            isExisting = os.path.exists(path + filename)
            if not isExisting:
                subdf = self.execute(df_)
                logger.info('non cè niente ->' + path + '------' + filename)
                DH.write(subdf, path + filename)
            elif isExisting == True and to_delete == True:
                os.remove(path + filename)
                subdf = self.execute(df_)
                logger.info('cè qualcosa ->' + path + '------' + filename)
                DH.write(subdf, path + filename)
            else: 
                pass     
            path_list.append(path)
    
        return path_list   

    @log_exception(logger)
    def execute(self, df : pd.DataFrame) -> pd.DataFrame:
        
        """
        Sequential call of class function to generate the timeseries dataframe according to specified hierarchies and time span

        Returns:
            df_ts: pd.DataFrame 
                DataFrame identifying the timeseries generated according to specified hierarchies and time span
        """

        logger.info('STEP 1 - Starting preparing data', important = True)
        
        logger.info('STEP 1 - Extracting date from datetime column')
        df[self.params['col_index'] + '_date'] = from_timestamp_to_date(df[self.params['col_index'] ])

        logger.info('STEP 1 - Generating the timeseries target')
        df_target = generating_target(df, [self.params['col_index']+"_date"], self.params['target_col'])
        df_target.columns = ['timeline','target']

        logger.info('STEP 1 - Creating the entire timeline to complete the target')
        df_calendar = pd.DataFrame(resample_date(df_target, "D")['timeline'])

        df_ts = pd.merge(df_calendar, df_target, how='left', on="timeline")
        
        logger.info('STEP 1 - Generating the complete timeseries', important = True)

        if self.params['timeline_level'][0].upper() != "D":
            df_ts = self.resample_date(df_ts, self.params['timeline_level'][0].upper() )
        else:
            pass 

        #logger.info('STEP 1 - Filling Missing Values', important = True)
        #df_ts['filled_target'] = list(self.handling_missing_values(df_ts.timeline,df_ts.target))
        # df_ts.name = self.filename

        # Rename timeline to timestamp
        df_ts.rename(columns={'timeline':'Timestamp', 'target':'Target'}, inplace=True)

        return df_ts

    def find_time_range(self,timeline:pd.Series) -> tuple:
        """
        The function finds the range of the timeline provided in input

        Parameters
        ----------
        timeline: pd.Series (dtype: datetime64[ns])
            The timeline series.
        Returns
        -------
            Tuple
            The range of the timeline (minimum date, maximum date)
        """
        start_date, end_date = timeline.min(), timeline.max()
        return start_date, end_date

    def generate_holidays(self,start_date: datetime, end_date: datetime, aggregation_frequency: str = 'D') -> pd.Series:
        """
        The function generates a series containing 1s for holidays and 0s vice-versa 
        (Saturdays and Sundays are considered holidays)

        Parameters
        ----------
        start_date: datetime
            Starting date of interest
        end_date: datetime
            End date of interest
        aggregation_frequency: str, optional
            Time aggregation frequency (default: 'D' -> Days) 
            
        Returns
        -------
            pd.Series 
            Series containing 1s for holidays and 0s vice-versa
        """
        italy_holidays = holidays.Italy()
        holidays_list = []
        current_date = start_date

        while current_date <= end_date:
            if current_date in italy_holidays or current_date.weekday() == 5 or current_date.weekday() == 6:
                holidays_list.append(1)
            else:
                holidays_list.append(0)

            current_date += np.timedelta64(1, aggregation_frequency)

        return pd.Series(holidays_list)
    

    def imputation_missing_target_holidays(self, holidays: pd.Series, target: pd.Series) -> pd.Series:
        """
        The function substitutes the missing values in target with 0s for the holidays.

        Parameters
        ----------
        holidays : pd.Series
            represents holidays with 1s and 0s vice-versa. 
        target : pd.Series
            represents the target

        Returns
        -------
        pd.Series
            series with 0s where there are missing values corresponding to holidays.

        """
        modified_target = target.copy()
        missing_indices = modified_target[modified_target.isna()].index

        for index in missing_indices:
            if holidays.iloc[index] == 1:
                modified_target.iloc[index] = 0

        return pd.Series(modified_target)

    def fill_missing_values(self, timeline: pd.Series, target: pd.Series,) -> pd.Series:
        """
        Estimates the target missing values

        Parameters:
            target: pd.Series 
            The target variable series
            timeline: pd.Series
            The timeline series

        Returns:
            pd.Series 
            The series with the imputation for the missing values
        """
        if target.isnull().sum() == 0:
            # No missing values in the series, return the original series
            return target
        
        df_intermediate = pd.DataFrame({'timeline': timeline, 'target': target})
        df_intermediate.set_index('timeline', inplace=True)
        target_interp = df_intermediate['target'].interpolate(method='time')
        return target_interp

    def handling_missing_values(self,timeline: pd.Series, target: pd.Series) -> pd.Series:
        """
        The function estimates and corrects the missing values in the target series

        Parameters
        ----------
        timeline: datetime
            it's the timeline series
        target: pd.Series
            The target variable series

        Returns
        -------
            the target series with the imputation of the missing values
        """
        if target.isnull().sum() == 0:
            return target
        else:
            date_range = self.find_time_range(timeline)
            holidays = self.generate_holidays(date_range[0], date_range[1])
            target_holidays_imputation = self.imputation_missing_target_holidays(holidays, target)
            final_target = self.fill_missing_values(timeline,target_holidays_imputation)
            return final_target

     
