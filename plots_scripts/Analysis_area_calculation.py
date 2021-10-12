from plots_scripts.Analysis_area_plotting import choose_bound_fkt, lin_bg_fkt


def lin_BG_int_fkt(df, df2, i_low, i_up):
    s = 1
    while s < len(df.columns):
        i = 0
        while i < len(df):
            m = (df.iloc[i_up, s] - df.iloc[i_low, s]) / (df.iloc[i_up, 0] - df.iloc[i_low, 0])
            y_lin_BG = m * (df["E"][i] - df.iloc[i_low, 0]) + df.iloc[i_low, s]
            df2.iloc[i, s] = y_lin_BG
            i += 1
        s += 1
    return df2


def integration_fkt(df3, i_low_int, i_up_int):
    df4 = df3.copy()
    df4.drop(df4.index[1:len(df4)], 0, inplace=True)
    s = 1
    while s < len(df3.columns):
        df4.iloc[0, s] = df3.iloc[i_low_int:i_up_int, s].sum()
        s += 1
    return df4


def calc_path_main_fkt(df, Inputs, bounds_container=None):
    if bounds_container is None:
        lower_fit_bound, fit_E_low, i_low_fit = choose_bound_fkt(df, Inputs, 0)
        upper_fit_bound, fit_E_up, i_up_fit = choose_bound_fkt(df, Inputs, 1)
        lower_int_bound, int_E_low, i_low_int = choose_bound_fkt(df, Inputs, 2)
        upper_int_bound, int_E_up, i_up_int = choose_bound_fkt(df, Inputs, 3)
    else:
        fit_E_low, i_low_fit, fit_E_up, i_up_fit, int_E_low, i_low_int, int_E_up, i_up_int = bounds_container

    # calculation of linear BG
    df2 = df.copy()
    df2 = lin_BG_int_fkt(df, df2, i_low_fit, i_up_fit)

    # cal diff of area
    df3 = df - df2
    df3["E"] = df["E"]

    # integration of the spectra
    df4 = integration_fkt(df3, i_low_int, i_up_int)

    # createa a df with only the spectra, to reshape it into a matrix
    df5 = df4.copy()
    df5 = df5.drop(['E'], axis=1)

    # correcting the area by the mean free path, cross section and the transmission fkt
    df6 = df5/(Inputs["sigma"]*Inputs["trans_fkt"]*Inputs["IMFP"])

    e_bound_container = fit_E_low, fit_E_up, int_E_low, int_E_up
    return df, df2, df3, df4, df5, df6, e_bound_container

