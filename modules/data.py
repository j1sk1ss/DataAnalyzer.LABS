import pandas as pd
import statistics
import math
import numpy as np

import scipy.stats as sps
from scipy.stats import shapiro
from scipy.stats import chisquare

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from modules.common import get_lists, get_dispersion


class Data:
    def __init__(self, dataframe):
        self.results = None
        self.model = None
        self.target = 'Luminosity(L/Lo)'

        if dataframe is not None:
            self.data_body = dataframe
            self.data_names = list(self.data_body.columns.values)
            self.data_lists = get_lists(self.data_body)
            self.target = self.data_body.columns[0]
        else:
            self.data_body = None
            self.data_names = []
            self.data_lists = [[]]

    def normalize(self):
        numeric_data_frame = self.data_body.apply(pd.to_numeric, errors='coerce')
        self.data_body = (numeric_data_frame - numeric_data_frame.min()) / (
                numeric_data_frame.max() - numeric_data_frame.min())

    def get_power(self):
        return len(self.data_body)

    def get_average(self, power):
        answer = {}
        for j in range(len(self.data_body.iloc[0])):
            column_average = 0
            for i in range(len(self.data_body)):
                column_average += float(self.data_body.iloc[i].iloc[j])

            answer[self.data_names[j]] = column_average / power

        return answer

    def get_sample_mean(self, power):
        average = []
        for j in range(len(self.data_body.iloc[0])):
            column_average = 0
            for i in range(len(self.data_body)):
                column_average += float(self.data_body.iloc[i].iloc[j])

            average.append(column_average)

        answer = {}
        for i in range(len(average)):
            answer[self.data_names[i]] = average[i] / power

        return answer

    def get_median(self):
        answer = {}
        for i in range(len(self.data_lists)):
            answer[self.data_names[i]] = statistics.median(self.data_lists[i])

        return answer

    def get_mode(self):
        answer = {}
        for i in range(len(self.data_lists)):
            answer[self.data_names[i]] = statistics.mode(self.data_lists[i])

        return answer

    def get_scope(self):
        answer = {}
        for i in range(len(self.data_lists)):
            min_value = min(self.data_lists[i])
            max_value = max(self.data_lists[i])
            answer[self.data_names[i]] = {
                'Максимальное значение': max_value,
                'Минимальное значение': min_value,
                'Ампитуда': max_value - min_value
            }

        return answer

    def get_dispersion(self, average, power):
        answer = {}
        for j in range(len(self.data_lists)):

            # X ^ 2
            powered_list = []
            for i in self.data_lists[j]:
                powered_list.append(i ** 2)

            # (X - mx) ^ 2
            temp_list = []
            for i in range(len(self.data_lists[j])):
                temp_list.append((self.data_lists[j][i] - average[j]) ** 2)

            # Dispersion
            dispersion = get_dispersion(power, self.data_lists[j], average[j])
            dispersion_sec = statistics.variance(self.data_lists[j], xbar=average[j])

            answer[self.data_names[j]] = {
                'Первая формула дисперсии': dispersion,
                'Вторая формула дисперсии': dispersion_sec
            }

        return answer

    def get_standard_deviation(self, average, power):
        answer = {}
        for i in range(len(self.data_lists)):
            std = statistics.stdev(self.data_lists[i])
            std_second = math.sqrt(get_dispersion(power, self.data_lists[i], average[i]))

            answer[self.data_names[i]] = {
                'Первая формула стандартного отклонения': std,
                'Вторая формула стандартного отклонения': std_second
            }

        return answer

    def get_variation(self, std, average):
        answer = {}
        for i in range(len(self.data_lists)):
            answer[self.data_names[i]] = (std[i] / average[i]) * 100.0

        return answer

    def get_quartile(self):
        answer = {}
        for i in range(len(self.data_lists)):
            down_quartile = np.quantile(self.data_lists[i], 0.25)
            upper_quartile = np.quantile(self.data_lists[i], 0.75)
            answer[self.data_names[i]] = {
                'Верхний квартиль': upper_quartile,
                'Нижний квартиль': down_quartile
            }

        return answer

    def get_kurtosis(self):
        answer = {}
        for i in range(len(self.data_lists)):
            answer[self.data_names[i]] = sps.kurtosis(self.data_lists[i], bias=False)

        return answer

    def get_asymmetry(self):
        answer = {}
        for i in range(len(self.data_lists)):
            answer[self.data_names[i]] = sps.skew(self.data_lists[i], bias=False)

        return answer

    def get_percentile(self, percentiles):
        answer = {}
        for i in range(len(self.data_lists)):
            pl = []
            for p in percentiles:
                pl.append(np.percentile(self.data_lists[i], p))

            answer[self.data_names[i]] = pl

        return answer

    def get_interval_estimation(self):
        answer = {}
        for i in range(len(self.data_lists)):
            data = np.array(self.data_lists[i])
            mean = np.mean(data)
            std_dev = np.std(data)
            confidence_level = 0.95

            n = len(data)
            t_value = sps.t.ppf(1 - (1 - confidence_level) / 2, n - 1)
            margin_of_error = t_value * (std_dev / np.sqrt(n))
            confidence_interval = (mean - margin_of_error, mean + margin_of_error)

            answer[self.data_names[i]] = confidence_interval

        return answer

    def get_shapiro_normal(self):
        answer = {}
        for i in range(len(self.data_lists)):
            stat, p = shapiro(self.data_lists[i])
            answer[self.data_names[i]] = {
                'T': stat,
                'P': p
            }

        return answer

    def get_chisquare_normal(self):
        answer = {}
        for i in range(len(self.data_lists)):
            stat, p = chisquare(self.data_lists[i])
            answer[self.data_names[i]] = {
                'T': stat,
                'P': p
            }

        return answer

    def get_regression_coef(self, output_name):
        input_data = self.data_body.drop(columns=[output_name], axis=1)
        output_data = self.data_body.filter(items=[output_name])

        input_t = input_data.transpose()
        b = np.dot(np.dot(np.linalg.inv(np.dot(input_t, input_data)), input_t), output_data)
        return b

    def fit_model(self, output_name):
        assert isinstance(self.data_body, pd.DataFrame), "self.data_body должен быть DataFrame"

        # Ensure input_data is a DataFrame with proper feature names
        input_data = self.data_body.drop(columns=[output_name], axis=1)
        output_data = self.data_body[output_name]

        # Fit the model
        self.model = LinearRegression()
        self.results = self.model.fit(input_data, output_data)

        # Get coefficients and intercept
        coefficients = self.model.coef_
        intercept = self.model.intercept_

        # Construct the equation text
        equation_text = f"{output_name} = {intercept:.2f}"
        for variable, coefficient in zip(input_data.columns, coefficients):
            equation_text += f" + {coefficient:.2f} * {variable}"

        # Calculate R^2 and mean absolute error
        r_squared = self.model.score(input_data, output_data)
        mean_abs_error = mean_absolute_error(output_data, self.model.predict(input_data))

        n = len(output_data)
        p = input_data.shape[1]

        # Check to prevent divide by zero error
        if r_squared == 1:
            f_statistic = np.inf
            p_value = 0.0
        else:
            f_statistic = (r_squared / (1 - r_squared)) * ((n - p - 1) / p)
            p_value = 1 - sps.f.cdf(f_statistic, p, n - p - 1)

        return {
            'R^2': r_squared,
            'Средняя ошибка аппроксимации': mean_abs_error,
            'Критерий Фишера': p_value,
            'Уравнение': equation_text
        }

    def predict(self, input_data):
        return self.results.predict(input_data)

    def get_summary(self):
        try:
            power = self.get_power()
            average = list(self.get_average(power).values())
            std = self.get_standard_deviation(average, power)
            first_std = []
            for i in list(std.values()):
                first_std.append(i['Первая формула стандартного отклонения'])

            return {
                'Мощность выборки': power,
                'Выборочное среднее': self.get_sample_mean(power),
                'Медиана': self.get_median(),
                'Мода': self.get_mode(),
                'Размах варианции': self.get_scope(),
                'Дисперсия': self.get_dispersion(average, power),
                'Стандартное отклонения': self.get_standard_deviation(average, power),
                'Коэффициент вариации': self.get_variation(first_std, average),
                'Верхний и нижний квартиль': self.get_quartile(),
                'Коэффициент эксцесса': self.get_kurtosis(),
                'Коэффициент асимметрии': self.get_asymmetry(),
                'Перцентиль (40 & 80)': self.get_percentile([40, 80]),
                'Интервальное оценивание': self.get_interval_estimation(),
                'Нормальность Хи-Квадрат Пирсона': self.get_chisquare_normal(),
                'Нормальность Шапиро-Уилка': self.get_shapiro_normal(),
                'Коэффициент регрессии': self.get_regression_coef(self.target),
                'Данные регрессии': self.fit_model(self.target)
            }
        except ValueError:
            return {
                'Ошибка': {
                    'Название': 'Ошибка в анализе данных',
                    'Причина': 'Наличие не числовых столбцов',
                    'Код': 1
                }
            }
