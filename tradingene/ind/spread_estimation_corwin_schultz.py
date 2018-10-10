# -*- coding: utf-8 -*-
"""
Created on Tue May 15 14:55:25 2018

@author: user
"""
import numpy as np
from scipy.optimize import fsolve
import math


#import matplotlib.pyplot as plt
#mode = 1 indicates Jensen's Indequality
def corwin_schultz(L_obs_0, H_obs_0, L_obs_1, H_obs_1, mode=0):
    k_1 = 4 * math.log(2)
    k_2 = math.sqrt(8 / math.pi)

    L_obs_01 = min([L_obs_0, L_obs_1])
    H_obs_01 = max([H_obs_0, H_obs_1])

    beta = math.log(H_obs_0 / L_obs_0) * math.log(
        H_obs_0 / L_obs_0) + math.log(H_obs_1 / L_obs_1) * math.log(
            H_obs_1 / L_obs_1)
    gamma = math.log(H_obs_01 / L_obs_01) * math.log(H_obs_01 / L_obs_01)

    func_sigma = lambda sigma : sigma * sigma * (k_2 * k_2 * (2 - 2 * np.sqrt(2)) + k_1) + \
                                            sigma * k_2 * (2 * np.sqrt(2) - 2 ) * np.sqrt(sigma*sigma*(k_2 * k_2 - k_1) + beta / 2) + \
                                            beta / 2 - gamma
    sigma_guess = 0
    sigma_solve = fsolve(func_sigma, sigma_guess)
    func_alpha = lambda alpha : -1 * k_2 * sigma_solve + \
                                np.sqrt(sigma_solve * sigma_solve * (k_2 * k_2 - k_1) + beta / 2) - alpha

    alpha_guess = 0
    alpha_solve = fsolve(func_alpha, alpha_guess)

    if (mode == 0):
        func_alpha_ignor_ineq = lambda alpha : (np.sqrt(2 * beta)- np.sqrt(beta))/(3 - 2 * np.sqrt(2)) \
                                                - np.sqrt(gamma / (3 - 2 * np.sqrt(2))) - alpha
        alpha_solve = fsolve(func_alpha_ignor_ineq, alpha_guess)
        #alph = np.linspace(-1, 1, )
    perc_spread = 2 * (np.exp(alpha_solve) - 1) / (1 + np.exp(alpha_solve))
    return perc_spread
