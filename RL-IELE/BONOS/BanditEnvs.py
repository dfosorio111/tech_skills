# Se modificó la clase/modulo BanditEnvs. En el método constructor se agregaron los siguientes atributos: 
# atributos: self.__beta=Bi con distribución normal N(0,1), self.__omega_w0 = np.pi / 100000, self.__omega_w1 = np.pi / 1000
# media de las distribuciones de los escenarios 4 y 5 self.__mu_4 = self.__beta + np.cos(self.__omega_w0 * self.t), self.__mu_5 = self.__beta + np.cos(self.__omega_w1 * self.t)

#  métodos: run_env_4 genera una recompensa a partir de la distribución normal de N(self.__mu_4,self.__sigma_2)
# run_env_5 genera una recompensa a partir de la distribución normal de N(self.__mu_5,self.__sigma_2)

import numpy as np

class BanditEnvs:

  def __init__(self, k=8):

        # Handle possible errors on args (k)
        if k < 0 or k > 20:
          raise Exception("Please use a number for k between 0 and 20 (int)")

        self.k = int(k)
        self.t = 1
        # mu values
        self.__mu = np.array([-0.6,  1.8, -3.0,  3.4, -1.2,  0.6, -0.6, -1.2,
       -1.8, -1.2, -0.6, -2.4,  0.0 ,  3. ,  3.0,  2.4,  3.6 ,  0.6,  0.0,  1.2])

        # mu arrays
        self.__mu_1 = np.copy(self.__mu[0:self.k])
        self.__mu_2 = np.copy(np.flip(self.__mu)[0:self.k])
        self.__mu_3 = np.copy(self.__mu[0:self.k])
        
        # new mu arrays
        self.__beta = np.random.normal(0, 1, size=self.k)
        self.__omega_w0 = np.pi / 100000
        self.__omega_w1 = np.pi / 1000

        self.__mu_4 = self.__beta + np.cos(self.__omega_w0 * self.t)
        self.__mu_5 = self.__beta + np.cos(self.__omega_w1 * self.t)
        
        
        # sigma arrays
        self.__sigma_1 = np.ones(self.k)*3
        self.__sigma_2 = np.ones(self.k)
        self.__sigma_3 = np.ones(self.k)*1.5

  # Environment with large var
  def run_env_1(self, action=0):
    # Compute reward
    mu = self.__mu_1[action]
    sigma = self.__sigma_1[action]
    reward = np.random.normal(mu, sigma)

    # Return reward
    return reward

  # Environment with small var
  def run_env_2(self, action=0):
    # Compute reward
    mu = self.__mu_2[action]
    sigma = self.__sigma_2[action]
    reward = np.random.normal(mu, sigma)

    # Return reward
    return reward

  # Non-static Environment
  def run_env_3(self, action=0):
    # Compute reward
    mu = self.__mu_3[action]
    sigma = self.__sigma_3[action]
    reward = np.random.normal(mu, sigma)

    # Add small changes to mu (non-static env)
    self.__mu_3 += np.random.normal(0, 0.1, size=self.k)

    # Return reward
    return reward
  
   # Ambiente con  w0=pi/100000
  def run_env_4(self, action=0):
    # Compute reward
    mu =  self.__mu_4[action]
    sigma = self.__sigma_2[action]
    reward = np.random.normal(mu, sigma)

    # Increment t
    self.t += 1

    # Return reward
    return reward

     # Ambiente con  w1=pi/1000
  def run_env_5(self, action=0):
    # Compute reward
    mu = self.__mu_5[action]
    sigma = self.__sigma_2[action]
    reward = np.random.normal(mu, sigma)

    # Increment t
    self.t += 1

    # Return reward
    return reward
  
  
  # Reset Non-static Environment
  def reset(self):
    self.__mu_3 = np.copy(self.__mu[0:self.k])
    self.t=1
    
    #print('Los entornos se han reiniciado satisfactoriamente')
