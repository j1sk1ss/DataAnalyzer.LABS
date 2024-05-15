import flet as ft

from data_process import data_is_loaded, get_dataframe, get_target, get_data
from pages.page import Page


reg_variables_fields = []
reg_answer = ft.Text('')


def calculate_reg(event):
    reg_answer.value = f'{get_target()}:\n'
    if len(reg_variables_fields) != 0:
        values = [float(x.value) for x in reg_variables_fields]
        reg_answer.value = reg_answer.value + f'{get_dataframe().predict([values])[0]}'
    else:
        return 0


def get_reg_page(page: Page):
    page.clean_controls()

    try:
        if data_is_loaded():
            pdata = []
            edata = []

            dataframe = get_dataframe()
            input_data = dataframe.data_body.drop(columns=[get_target()], axis=1)
            predicted_output = dataframe.predict(input_data)

            expected_output = list(dataframe.data_body[get_target()])

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
                    content=ft.Text(value=f"Прогноз {get_target()} против реальности"),
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

            reg_answer.value = f'{get_target()}:\n...'

            def calculate_regression():
                calculate_reg(None)
                page.body.update()

            reg_variables_fields.clear()
            for i in get_data().columns:
                if i is not get_target():
                    reg_variables_fields.append(
                        ft.TextField(
                            label=i, data=i, on_change=lambda _: calculate_regression(),
                            height=40, width=80, value='0.0'
                        )
                    )

            page.add_control(
                ft.Row(
                    [
                        *reg_variables_fields, reg_answer
                    ]
                )
            )

        return page

    except AttributeError:
        print('[Error] Reg error')
