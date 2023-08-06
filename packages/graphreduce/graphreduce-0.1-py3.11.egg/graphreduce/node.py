#!/usr/bin/env python

# std lib
import abc
import datetime
import typing

# third party
import pandas as pd
from dask import dataframe as dd
import pyspark

# internal
from graphreduce.enum import ComputeLayerEnum, PeriodUnit



class GraphReduceNode(metaclass=abc.ABCMeta): 
    fpath : str
    fmt : str
    prefix : str
    date_key : str
    pk : str 
    feature_function : str
    compute_layer : ComputeLayerEnum
    spark_sqlctx : typing.Optional[pyspark.sql.SQLContext]
    cut_date : datetime.datetime
    compute_period_val : typing.Union[int, float]
    compute_period_unit : PeriodUnit
    has_labels : bool
    label_period_val : typing.Optional[typing.Union[int, float]]
    label_period_unit : typing.Optional[PeriodUnit] 

    def __init__ (
            self,
            fpath : str,
            fmt : str,
            pk : str = None,
            prefix : str = None,
            date_key : str = None,
            feature_function : str = None,
            compute_layer : ComputeLayerEnum = None,
            spark_sqlctx : pyspark.sql.SQLContext = None,
            cut_date : datetime.datetime = datetime.datetime.now(),
            compute_period_val : typing.Union[int, float] = 365,
            compute_period_unit : PeriodUnit  = PeriodUnit.day,
            has_labels : bool = False,
            label_period_val : typing.Optional[typing.Union[int, float]] = None,
            label_period_unit : typing.Optional[PeriodUnit] = None,
            ):
        """
Constructor
        """
        self.fpath = fpath
        self.fmt = fmt
        self.pk = pk
        self.prefix = prefix
        self.date_key = date_key
        self.feature_function = feature_function
        self.compute_layer = compute_layer
        self.spark_sqlctx = spark_sqlctx
        self.cut_date = cut_date
        self.compute_period_val = compute_period_val
        self.compute_period_unit = compute_period_unit
        self.has_labels = has_labels
        self.label_period_val = label_period_val
        self.label_period_unit = label_period_unit

    
    def do_data (
        self
    ) -> typing.Union[
        pd.DataFrame,
        dd.DataFrame,
        pyspark.sql.dataframe.DataFrame
    ]:
        """
Get some data
        """
        if self.compute_layer.value == 'pandas':
            if not hasattr(self, 'df') or (hasattr(self,'df') and not isinstance(self.df, pd.DataFrame)):
                self.df = getattr(pd, f"read_{self.fmt}")(self.fpath)
                self.df.columns = [f"{self.prefix}_{c}" for c in self.df.columns]
        elif self.compute_layer.value == 'dask':
            if not hasattr(self, 'df') or (hasattr(self, 'df') and not isinstance(self.df, dd.DataFrame
)):
                self.df = getattr(dd, f"read_{self.fmt}")(self.fpath)
                self.df.columns = [f"{self.prefix}_{c}" for c in self.df.columns]
        elif self.compute_layer.value == 'spark':
            if not hasattr(self, 'df') or (hasattr(self, 'df') and not isinstance(self.df, pyspark.sql.DataFrame)):
                self.df = getattr(self.spark_sqlctx.read, {self.fmt})(self.fpath)
                for c in self.df.columns:
                    self.df = self.df.withColumnRenamed(c, f"{self.prefix}_{c}")


    @abc.abstractmethod
    def do_filters (
        self
    ):
        """
do some filters on the data
        """
        pass
    

    @abc.abstractmethod
    def do_annotate(self):
        '''
        Implement custom annotation functionality
        for annotating this particular data
        '''
        return

    
    @abc.abstractmethod
    def do_post_join_annotate(self):
        '''
        Implement custom annotation functionality
        for annotating data after joining with 
        child data
        '''
        pass

     
    @abc.abstractmethod
    def do_clip_cols(self):
        return
            

    @abc.abstractmethod
    def do_reduce(self, reduce_key):
        """
Reduce operation or the node
        """
        pass
    
    
    @abc.abstractmethod
    def do_labels(self, reduce_key):
        pass
    
        
    def colabbr(self, col: str) -> str:
        return f"{self.prefix}_{col}"
    
    
    def prep_for_features(self):
        """
Prepare the dataset for feature aggregations / reduce
        """
        if self.cut_date and isinstance(self.cut_date, str) or isinstance(self.cut_date, datetime.datetime):
            if isinstance(self.df, pd.DataFrame) or isinstance(self.df, dd.DataFrame):
                return self.df[
                    (self.df[self.colabbr(self.date_key)] < self.cut_date)
                    &
                    (self.df[self.colabbr(self.date_key)] > (self.cut_date - datetime.timedelta(days=self.compute_period_val)))
                ]
            elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                return self.df.filter(
                    (self.df[self.colabbr(self.date_key)] < self.cut_date)
                    &
                    (self.df[self.colabbr(self.date_key)] > (self.cut_date - datetime.timedelta(days=self.compute_period_val)))
                )
        else:
            if isinstance(self.df, pd.DataFrame) or isinstance(self.df, dd.DataFrame):
                return self.df[
                    (self.df[self.colabbr(self.date_key)] < datetime.datetime.now())
                    &
                    (self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(days=self.compute_period_val)))
                ]
            elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                return self.df.filter(
                    self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(days=self.compute_period_val))
                )
    
    
    def prep_for_labels(self):
        """
        Prepare the dataset for labels
        """

        if self.cut_date and isinstance(self.cut_date, str) or isinstance(self.cut_date, datetime.datetime):
            if isinstance(self.df, pd.DataFrame):
                return self.df[
                    (self.df[self.colabbr(self.date_key)] > (self.cut_date))
                    &
                    (self.df[self.colabbr(self.date_key)] < (self.cut_date + datetime.timedelta(days=self.label_period_val)))
                ]
            elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                return self.df.filter(
                    (self.df[self.colabbr(self.date_key)] > (self.cut_date))
                    &
                    (self.df[self.colabbr(self.date_key)] < (self.cutDate + datetime.timedelta(days=self.label_period_val)))
                )
        else:
            if isinstance(self.df, pd.DataFrame):
                return self.df[
                    self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(days=self.label_period_val))
                ]
            elif isinstance(self.df, pyspark.sql.dataframe.DataFrame):
                return self.df.filter(
                    self.df[self.colabbr(self.date_key)] > (datetime.datetime.now() - datetime.timedelta(days=self.label_period_val))
                )
