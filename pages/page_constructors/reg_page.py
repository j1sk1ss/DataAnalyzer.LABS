import flet as ft

from data_process import data_is_loaded, get_dataframe
from pages.page import Page


def get_reg_page(page: Page):
    page.clean_controls()

    try:
        if data_is_loaded():
            pdata = []
            edata = []

            dataframe = get_dataframe()
            predicted = dataframe.data_body.drop(columns=['Luminosity(L/Lo)'], axis=1).to_numpy()
            predicted_output = dataframe.predict(predicted)

            expected_output = list(dataframe.data_body['Luminosity(L/Lo)'])

            bottom_axis = [
                ft.ChartAxisLabel(
                    value=x,
                    label=ft.Text(str(x), size=10, weight=ft.FontWeight.NORMAL),
                ) for x in range(len(predicted_output))
            ]

            left_axis = [
                ft.ChartAxisLabel(
                    value=x,
                    label=ft.Text(str(x), size=10, weight=ft.FontWeight.NORMAL),
                ) for x in range(int(max(predicted_output)), 0, max(int(max(predicted_output) / 100), 1))
            ]

            for i in range(len(predicted_output)):
                pdata.append(ft.LineChartDataPoint(i, predicted_output[i]))

            for i in range(len(expected_output)):
                edata.append(ft.LineChartDataPoint(i, expected_output[i]))

            chart_data = [
                ft.LineChartData(
                    data_points=pdata,
                    stroke_width=2,
                    color=ft.colors.LIGHT_GREEN,
                    curved=True,
                    stroke_cap_round=True,
                ),
                ft.LineChartData(
                    data_points=edata,
                    stroke_width=2,
                    color=ft.colors.LIGHT_BLUE,
                    curved=True,
                    stroke_cap_round=True,
                )
            ]

            page.add_control(ft.Row([
                ft.Container(
                    content=ft.Text(value="Прогноз против реальности"),
                    alignment=ft.alignment.center,
                    width=1200,
                    height=60,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=ft.border_radius.all(5),
                )
            ]))

            page.add_control(
                ft.LineChart(
                    data_series=chart_data,
                    left_axis=ft.ChartAxis(
                        labels=left_axis
                    ),
                    bottom_axis=ft.ChartAxis(
                        labels=bottom_axis
                    ),
                    border=ft.Border(
                        bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))
                    )
                )
            )

        return page

    except AttributeError:
        print('[Error] Reg error')
