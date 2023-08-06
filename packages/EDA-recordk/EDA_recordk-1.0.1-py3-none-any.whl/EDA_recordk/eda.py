import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


class EDA:
    def __init__(self, data):
        self.data = data
        self.summary()
        self.missing_values()
        self.unique_values(self.data.columns)
        self.correlation_matrix()
        self.histogram(self.data.columns)
        self.box_plot()

    # 데이터 요약을 보는 함수
    def summary(self):
        print('Data Summary')
        print(self.data.describe())
        print('=' * 25)
        print('Data info:')
        print(self.data.info())
        print('=' * 25)

    def unique_values(self, columns):

        for column in columns:
            print(f'Unique values in {column}:')
            if self.data[column].dtype in ['int64', 'float64']:
                print(np.sort(self.data[column].unique()))
            else:
                print(self.data[column].unique())
            print('=' * 25)

    # 결측치 확인
    def missing_values(self):
        print('Missing Values:')
        print(self.data.isna().sum())
        print('=' * 25)

    def preprocessing(self):
        missing_columns = self.data.columns[self.data.isnull().any()].tolist()
        sel = '0'
        for i in missing_columns:
            print(f'Missing columns : {i} \n dtype : {self.data[i].dtype} \n cnt:{self.data[i].isna().sum()}')
            print('=' * 25)
            num = ['int64', 'float64']
            if self.data[i].dtype in num:
                sel = input('1. mode \n 2. mean \n 3. median')
            else:
                sel = input('1. mode \n 4. find_str_nan')
            self.show(sel, i)

    def show(self, sel, i):
        f = False
        while f:
            if sel == '1':
                self.mode(i)
                f = True
            elif sel == '2':
                self.mean(i)
                f = True
            elif sel == '3':
                self.median(i)
                f = True
            elif sel == '4':
                self.find_str()
                f = True
            else:
                sel = input('press 1~4 plz')
        print('complete!')

    def mode(self, i):
        self.data[i].fillna(self.data[i].mode()[0], inplace=True)

    def mean(self, i):
        self.data[i].fillna(self.data[i].mean(), inplace=True)

    def median(self, i):
        self.data[i].fillna(self.data[i].median(), inplace=True)

    def find_str(self):
        # 결측치 중에 nan이라고 문자로 되어있는 경우가 있어서 그 값을 찾음
        find_str_nan = input('find_str_nan? Y/N')
        nan_col = []
        n = ['NaN', 'NAN', 'nan']
        if find_str_nan.lower() == 'y':
            print('str nan')
            print('=' * 25)
            for column in self.data.columns:
                cnt = 0
                index_list = []
                for i, value in enumerate(self.data[column]):
                    if str(value) in n:
                        cnt += 1
                        index_list.append(i)
                        if cnt > 0:
                            nan_col.append(column)
                            print(f'{column}: str_nan {cnt} row: {index_list}')

        elif find_str_nan.lower() == 'n':
            pass
        else:
            print('plz press N or Y')
        change = input('chage to np.NaN ? Y/N')
        if change.lower() == 'y':
            for i in nan_col:
                self.data[i][self.data[i].isin(n)] = np.NaN
        elif change.lower() == 'n':
            pass
        else:
            print('plz press N or Y')

    #heatmap
    def correlation_matrix(self):
        corr_matrix = self.data.corr()
        print('Correlation Matrix:')
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()

    def histogram(self, columns):
        self.data[columns].hist()
        plt.tight_layout()
        plt.show()

    def box_plot(self):
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.data)
        plt.title('Box Plot')
        plt.show()

    def drop_outlier(self):
        # 변수 타입 확인
        continuous_vars = []
        for column in self.data.columns:
            if self.data[column].dtype in ['int64', 'float64']:
                continuous_vars.append(column)

            # 이상치 제거
            if len(continuous_vars) > 0:
                z_scores = np.abs(stats.zscore(self.data[continuous_vars]))
                threshold = 3
                filtered_data = self.data.copy()
                filtered_data[continuous_vars] = filtered_data[continuous_vars][(z_scores < threshold).all(axis=1)]
                filtered_data.dropna(subset=continuous_vars, inplace=True)
            else:
                filtered_data = self.data.copy()

            # 이상치 제거한 boxplot
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=filtered_data)
            plt.title('Box Plot')
            plt.show()
            self.data = filtered_data
