import pandas as pd
import numpy as np
from ioutils import read_input, save_data
import datetime
from typing import Iterator

def main():
    path = "data/sample_data.txt"
    raw_data = read_input(path)
    energy_per_weight = 7700 # standard kcal/kg
    tdee_calc_window = datetime.timedelta(days=13) # 2 week
    tdee_smoothing_factor = 0.1 
    data_with_tdee = calculate_all_tdee(raw_data, energy_per_weight, tdee_calc_window, tdee_smoothing_factor)
    print(data_with_tdee)

def calculate_all_tdee(data: pd.DataFrame, energy_per_weight: float, tdee_calc_window: datetime.timedelta,
                       tdee_smoothing_factor: float = 0.1):
    dates = data.index
    window_int = tdee_calc_window.days
    if len(data.index) < tdee_calc_window.days:
        raise IndexError(f"only {len(data.index)} days of data but window length is f{tdee_calc_window}")
    tdee_guess = calc_tdee_for_date(data, dates[window_int], energy_per_weight, tdee_calc_window)
    data.loc[dates[window_int], "TDEE_Guess"] = tdee_guess
    for date in dates[window_int+1:]:
        tdee_curr_date_guess = calc_tdee_for_date(data, date, energy_per_weight, tdee_calc_window)
        tdee_guess = (tdee_smoothing_factor * tdee_curr_date_guess
        + (1-tdee_smoothing_factor) * tdee_guess)
        data.loc[date, "TDEE_Guess"] = tdee_guess
    return data

def calc_tdee_for_date(data: pd.DataFrame, date: datetime.date, energy_per_weight: float,
                       time_period: datetime.timedelta = datetime.timedelta(days=13)):
    if energy_per_weight == -1:
        raise NotImplementedError("Does not yet support calculating energy per weight")
    start_date = date - time_period
    dates: Iterator = daterange(start_date, date, step_size=datetime.timedelta(days=1))
    dates: list = list(dates) # might use it as an iterator later
    days: np.array = np.array(range(1, len(dates)+1))
    weights: np.array = data.loc[dates, "Weight"].to_numpy()
    energies: np.array = data.loc[dates, "Energy"].to_numpy()

    weight_trend, _ = np.polyfit(days, weights, 1) # gives kg/day
    mean_intake: float = np.mean(energies)
    tdee_guess = mean_intake - weight_trend * energy_per_weight
    return tdee_guess
    

def daterange(start_date: datetime.date, end_date: datetime.date,
              step_size: datetime.timedelta):
    curr_date: datetime.date = start_date
    while curr_date <= end_date:
        yield curr_date
        curr_date += step_size

if __name__ == "__main__":
    main()
