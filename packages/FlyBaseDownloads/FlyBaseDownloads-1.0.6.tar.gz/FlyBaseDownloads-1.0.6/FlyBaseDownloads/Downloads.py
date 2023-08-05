#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:04:19 2023

@author: javiera.quiroz
"""


import pandas as pd
import fnmatch
import gzip
from ftplib import FTP
import re
import csv
import obonet
import json
import os


class Downloads():
    
    def __init__(self, url):
        
        self.url = url
        
    def download_file(self):
        
        url = self.url
        
        ftp = FTP(url.split('/')[2])
        ftp.login()
        directory_path = '/'.join(url.split('/')[3:-1])
        
        ftp.cwd(directory_path)
        
        remote_files = ftp.nlst()
        
        filtered_files = list(fnmatch.filter(remote_files, url.split('/')[-1]))
        
        files = []
        for file in filtered_files:
            file_path = '../' + file
            if not os.path.exists(file):
                with open(file_path, 'wb') as local_file:
                    ftp.retrbinary('RETR ' + file, local_file.write)
        
                files.append(file)
            else:
                files.append(file)
        
        ftp.quit()
        if len(files) > 0:
            return files
        else:
            print('Failed to download the file')
            return []
        
    
    
    
    def open_file_tsv(self, file_path, header):
        a = []

        if re.search(r'gz', file_path):
            
            try: 
                with gzip.open('../' + file_path, 'rt') as file:
                   df = pd.read_csv(file, sep='\t', header=header)
                   a.append(df)
                return (a[0])
            
            except: 
                try:
                    with gzip.open('../' + file_path, 'rt') as file:
                        df = csv.reader(file, delimiter='\t')
                        a.append(pd.DataFrame(df))
                
                    df = a[0]
                    columns = df.iloc[header, :].tolist()
        
                    df = df.iloc[header + 1:, :]
                    
                    df.columns = columns
                    df = df.dropna(axis='columns')
                  
  
                    return (df)
                except:
                    print('Failed to download the file') 
                    
    def open_file_json(self, file_path):
        
        a = []

        if re.search(r'gz', file_path):
            
            try: 
                with gzip.open('../' + file_path, 'rt') as file:
                    d = json.load(file)
                    d_ = d['data']
                    data = pd.DataFrame(d_)
                    a.append(data)
                   
            except:
                try:
                    with gzip.open('../' + file_path, 'rt') as file:
                        return json.load(file)
                except:
                    print('Failed to download the file') 
            
        
        return a[0]
                    
    def open_obo(self, file_path):
    
        a = []
        
        try:
            if re.search(r'gz', file_path):
                with gzip.open('../' + file_path, 'rt') as file:
                   if re.search(r'obo', file_path):
                       
                      graph = obonet.read_obo(file)
                      
                      a.append(graph)

            return a[0]
        
        except:
            print('Failed to download the file') 
            
    def open_fb(self, file_path,start_line, columns):
        a = []

        if re.search(r'gz', file_path):
            
            try:
                with gzip.open('../' + file_path, 'rt') as file:
                    df = csv.reader(file, delimiter='\t')
                    a.append(pd.DataFrame(df))
            
                df = a[0]
                
                df = df.iloc[start_line:, :-2]
                df.columns = columns
              

                return (df)
                            
            except:
                    print('Failed to download the file') 
        
    
    def get(self, header = None):
        
        files = []
        
        try:
            files = self.download_file()
        except:
            print('Failed to download the file') 
        patron = r"##?\s?\w+"
        
        def df_r(df):
            if re.search(r"FB\w{9}", df.columns[0]):
                df_columns = pd.DataFrame(df.columns).T

                df.columns = range(len(df.columns))
                
               
                df = pd.concat([df_columns, df], ignore_index=True, axis = 0)
            
            if re.search(patron, df.iloc[-1,0]):
                df = df.iloc[:-1, :]
            
            return df
        
        
        if len(files) > 0:
            if re.search('.obo', self.url):
                return self.open_obo(files[0])
            elif re.search('.json', self.url):
                try:
                    return df_r(self.open_file_json(files[0]))
                    
                except:
                    try:
                        df = self.open_file_json(files[0])
                        df = pd.concat([df.drop(['driver'], axis=1), df['driver'].apply(pd.Series)], axis=1)

                        df = df.replace({None: pd.NA})
                        return df_r(df)
                    except:
                        return self.open_file_json(files[0])
                    
            else:
                return df_r(self.open_file_tsv(files[0], header))
        
    
