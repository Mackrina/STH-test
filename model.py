import numpy as np
from pypfilt import OdeModel


class Model(OdeModel):

    def field_types(self, ctx):
        return [
            # Model state variables: host population
            ('S', float),
            ('E', float),
            ('I', float),
            # Model state variables: host parasites
            ('W_I', float),
            ('W_M', float),
            # Model state variables: environmental parasites
            ('L_R', float),
            ('L_I', float),
            # Model parameters
            ('b', float), # Human birth rate
            ('d', float), # Human mortality rate
            ('alpha_H', float), # Larvae maturity rate (in-host)
            ('delta_H', float), # Human larvae output
            ('alpha_L', float), # Larvae maturity rate (environment)
            ('kappa', float), # Carrying capacity (environment)
            ('mu_L', float), # Larvae mortality rate (environment)
            ('mu_LH', float), # Larvae mortality rate (host)
            ('n_H', float), # Probability of infection given contact
            ('beta_H', float), # Contact date (per day)
            ('r', float), # Natural parasite growth rate (environment)
        ]

    def d_dt(self, time, xt, ctx, is_forecast):
        # Host birth and death rates.
        host_births = xt['b'] * xt['S']
        host_deaths_S = xt['d'] * xt['S']
        host_deaths_E = xt['d'] * xt['E']
        host_deaths_I = xt['d'] * xt['I']

        # Host exposures to environmental larvae.
        env_larvae = xt['L_R'] + xt['L_I']
        lambda_H = xt['n_H'] * xt['beta_H'] * xt['L_I'] / env_larvae
        host_exposures = lambda_H * xt['S']

        # Host progression from E to I.
        host_infectious = xt['alpha_H'] * xt['E']
import numpy as np
from pypfilt import OdeModel


class Model(OdeModel):

    def field_types(self, ctx):
        r"""
        Define the state vector :math:`[\sigma, \rho, \beta, x, y, z]^T`.
        """
        return [
            # Model state variables: host population
            ('S_H', float),
            ('E_H', float),
            ('I_H', float),
            # Model state variables: environmental parasites
            ('L_I', float),
            # Model parameters
            ('b_H', float),  # Human birth rate
            ('d_H', float),  # Human mortality rate
            ('c_H', float),  # Contact rate of humans with reservoir
            ('p_1', float),  # Probability of getting infect 
            ('alpha_H', float),  # Larvae maturity rate (in- human host)
            ('r_H', float),  # Larvae output rate of humans
            ('f_H', float),  # Gram of feces of human
            ('p_2', float),  # probability of rhabditiform larvae develop into infective larvae
            ('kappa', float),  # number of larvae in the reservoir that 50% of getting infect from its maximum value
            ('mu_L', float),  # Larvae mortality rate (environment)
            
        ]

    def d_dt(self, time, xt, ctx, is_forecast):
        # Host birth and death rates.
        host_births = xt['b_H'] * (xt['S_H'] + xt['E_H'] + xt['I_H'])
        host_deaths_S_H = xt['d_H'] * xt['S_H']
        host_deaths_E_H = xt['d_H'] * xt['E_H']
        host_deaths_I_H = xt['d_H'] * xt['I_H']

        # Larvae death rates.
        larvae_deaths_I_env = xt['mu_L'] * xt['L_I']

        # Host exposures to environmental larvae.
        effective_contact_H = xt['c_H'] + xt['p_1']
        lambda_H = effective_contact_H * xt['L_I'] / (xt['kappa'] + xt['L_I'])
        human_exposures = lambda_H * xt['S_H']

        # Host progression from E to I.
        infectious_Humans = xt['alpha_H'] * xt['E_H']

        # Host contribution to environmental reservoir
        delta_H = xt['r_H'] * xt['f_H'] * xt['p_2']
        human_larvae_output = delta_H * xt['I_H']


        # Return the rates for each model compartment.
        d_dt = np.zeros(xt.shape, dtype=xt.dtype)
        d_dt['S_H'] = host_births - host_deaths_S_H - human_exposures
        d_dt['E_H'] = human_exposures - host_deaths_E_H - infectious_Humans
        d_dt['I_H'] = infectious_Humans - host_deaths_I_H
        d_dt['L_I'] = human_larvae_output - larvae_deaths_I_env 
        
        return d_dt
      
