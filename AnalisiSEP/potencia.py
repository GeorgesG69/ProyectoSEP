import numpy as np
import math

#--------------------------------------------------- POTENCIA DEL GENERADOR -----------------------------------------
def generador(imp_gen, voltaje, phi, vth, index_gen):

    #Pasamos el voltaje del generador a su forma rectangular
    voltaje_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        voltaje_generado[i,0] = voltaje[i]*(math.cos(phi[i]) + math.sin(phi[i])*1j)

    #Calculo de la corriente del generador
    corriente_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        indice_vth = index_gen[i] - 1
        voltaje_carga = voltaje_generado[i,0] - vth[indice_vth,0]
        corriente_generado[i,0] = voltaje_carga/imp_gen[i]
    
    #Potencia de los generadores
    p_generado=np.zeros((len(voltaje),1),dtype="complex_")
    q_generado=np.zeros((len(voltaje),1),dtype="complex_")
    
    p_generado = (voltaje_generado * np.conjugate(corriente_generado)).real
    q_generado = (voltaje_generado * np.conjugate(corriente_generado)).imag
        
    return p_generado, q_generado
#---------------------------------------------------- POTENCIA DE LA CARGA ------------------------------------------

def Cargas(imp_carga, Vth, bus_i_carga, i_carga, p_carga, q_carga, s_carga, fp_carga):
    
    for k in range(len(bus_i_carga)):
        if bus_i_carga[k] != 0:

            admitancia = 1/imp_carga
            #print(imp_carga)
            #print(admitancia)
            admitanciaConjugada = np.conjugate(admitancia)
                        
            S_carga = np.zeros((len(admitanciaConjugada), 1), dtype="complex_")
            
            #Potencia aparente carga
            for m in range(len(admitanciaConjugada)):
                S_carga[m] = ((Vth[m]) ** 2) * (admitanciaConjugada[m])

            #Potencia activa carga
            P_carga = np.zeros((len(S_carga), 1), dtype="float_")
            for s in range(len(S_carga)):
                P_carga[s, 0] = S_carga[s, 0].real

            #Potencia reactiva carga
            Q_carga = np.zeros((len(S_carga), 1), dtype="float_")
            for t in range(len(S_carga)):
                Q_carga[t, 0] = S_carga[t, 0].imag

    #print(f"Sc {k}: {S_carga}\n\nPc: {P_carga}\n\nQc: {Q_carga}")
    return S_carga, P_carga, Q_carga

#--------------------------------------------------- POTENCIAS DE LAS LINEAS -----------------------------------------

def Lineas(imp_linea, Vth_rect, bus_i_l, bus_j_l):

    #print(f"imp l: {imp_linea}\n\nvth: {Vth_rect}\n\nbus i: {bus_i_l}\n\nbus j: {bus_j_l}\n\n")

    for i in range(len(bus_j_l)):

        # Flujos de potencia
        #print(imp_linea[i])
        S_per_i_j = Vth_rect[bus_i_l-1] * np.conjugate((Vth_rect[bus_i_l-1] - Vth_rect[bus_j_l-1]) * (imp_linea[i]))
        

   # print(f"\n vth: {Vth_rect[bus_i_l-1]}\n\nvth2: {Vth_rect[bus_j_l-1]}\n\nPer ij: \n\n{S_per_i_j}\n")

    return S_per_i_j
