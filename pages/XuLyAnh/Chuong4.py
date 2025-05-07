import numpy as np
import cv2
L = 256

def Spectrum(imgin):
    f  = imgin.astype(np.float32)/(L-1)
    #Buoc1: DFT
    F = np.fft.fft2(f)
    #Buoc2: Shift vao the center of the inmage
    F = np.fft.fftshift(F)

    #Buoc5: Tinh Spectrum
    S = np.sqrt(F.real**2, + F.imag**2)
    S = np.clip(S, 0, L-1)
    imgout = S.astype(np.uint8)

    return imgout

def FrequencyFilter(imgin, H):
    f = imgin.astype(np.float32)
    F = np.fft.fft2(f)
    F = np.fft.fftshift(F)
    G = F * H
    G = np.fft.ifftshift(G)
    g = np.fft.ifft2(G)
    gR = g.real.copy()
    gR = np.clip(gR, 0, L-1)
    return gR.astype(np.uint8)

def CreateNotchRejectFilter():
    P = 250
    Q = 180
    u1, v1 = 44, 58
    u2, v2 = 40, 119
    u3, v3 = 86, 59
    u4, v4 = 82, 119

    D0 = 10
    n = 2
    H = np.ones((P,Q), np.float32)
    for u in range(0, P):
        for v in range(0, Q):
            h = 1.0
            # Bộ lọc u1, v1
            Duv = np.sqrt((u-u1)**2 + (v-v1)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u1))**2 + (v-(Q-v1))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u2, v2
            Duv = np.sqrt((u-u2)**2 + (v-v2)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u2))**2 + (v-(Q-v2))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u3, v3
            Duv = np.sqrt((u-u3)**2 + (v-v3)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u3))**2 + (v-(Q-v3))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0

            # Bộ lọc u4, v4
            Duv = np.sqrt((u-u4)**2 + (v-v4)**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            Duv = np.sqrt((u-(P-u4))**2 + (v-(Q-v4))**2)
            if Duv > 0:
                h = h*1.0/(1.0 + np.power(D0/Duv,2*n))
            else:
                h = h*0.0
            H[u,v] = h
    return H

def DrawNotchRejectFilter():
    H = CreateNotchRejectFilter()
    H = H*(L-1)
    H = H.astype(np.uint8)
    return H
    
def CreateMoireFilter(M, N):
    H = np.ones((M, N), np.complex64)
    H.imag = 0.0

    u1, v1 = 44, 55
    u2, v2 = 85, 55 
    u3, v3 = 41, 111
    u4, v4 = 81, 111


    u5, v5 = M - 44, M - 55
    u6, v6 = M - 85, M - 55 
    u7, v7 = M - 41, M - 111
    u8, v8 = M - 81, M - 111



    D0 = 7
    for u in range(0, M):
        for v in range(0, N):
            #u1, v1
            Duv = np.sqrt((u-u1)**2 + (v - v1)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u2, v2
            Duv = np.sqrt((u-u2)**2 + (v - v2)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u3, v3
            Duv = np.sqrt((u-u3)**2 + (v - v3)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u4, v4
            Duv = np.sqrt((u-u4)**2 + (v - v4)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u5, v5
            Duv = np.sqrt((u-u5)**2 + (v - v5)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u6, v6
            Duv = np.sqrt((u-u6)**2 + (v - v6)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u7, v7
            Duv = np.sqrt((u-u7)**2 + (v - v7)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
            #u8, v8
            Duv = np.sqrt((u-u8)**2 + (v - v8)**2)
            if Duv <= D0:
                H.real[u, v] = 0.0
    
    return H

def FrequencyFiltering(imgin, H):
    f  = imgin.astype(np.float32)
    #Buoc1: DFT
    F = np.fft.fft2(f)
    #Buoc2: Shift vao the center of the inmage
    F = np.fft.fftshift(F)
    #Buoc3: Nhan F voi H
    G = F*H

    #Buoc4: Shift return
    G = np.fft.ifftshift(G)

    #Buoc5: IDFT
    g = np.fft.ifft2(G)
    gR = np.clip(g.real, 0, L-1)
    imgout = gR.astype(np.uint8)

    return imgout

def CreateInferenceFilter(M, N):
    H = np.ones((M,N), np.complex64)
    D0 = 7
    for u in range(M):
        for v in range(N):
            if u not in range(M//2-D0, M//2+D0+1):
                if v in range(N//2-D0, N//2+D0+1):
                    H[u,v] = 0.0
    return H

def CreateMotionFilter(M, N):
    H = np.zeros((M, N), np.complex64)
    T = 1.0
    a = 0.1
    b = 0.1
    phi_prev = 0.0
    for u in range(0, M):
        for v in range(0, N):
            phi = np.pi*((u-M//2)*a + (v-N//2)*b)
            if abs(phi) < 1.0e-6:
                phi = phi_prev
                
            else:
                RE = T*np.sin(phi)*np.cos(phi)/phi
                IM = -T*np.sin(phi)*np.sin(phi)/phi
            H.real[u, v] = RE
            H.imag[u, v] = IM
            phi_prev = phi
    
    return H

def CreateDemotionFilter(M, N):
    H = np.zeros((M, N), np.complex64)
    T = 1.0
    a = 0.1
    b = 0.1
    phi_prev = 0.0
    for u in range(0, M):
        for v in range(0, N):
            phi = np.pi*((u-M//2)*a + (v-N//2)*b)
            mau_so = np.sin(phi)

            if abs(mau_so) < 1.0e-6:
                phi = phi_prev
                
            
            RE = phi/(T*np.sin(phi))*np.cos(phi)
            IM = phi/T
            H.real[u, v] = RE
            H.imag[u, v] = IM
            phi_prev = phi
    
    return H

def CreateNotchFilter(P,Q):
    H = np.ones((P,Q), np.complex64)
    coords = [(44, 55), (85, 55), (40, 112), (81, 112)]
    D0 = 10
    for u in range(P):
        for v in range(Q):
            for (ui, vi) in coords + [(P-ui, Q-vi) for (ui, vi) in coords]:
                d = np.sqrt((u - ui)**2 + (v - vi)**2)
                if d < D0:
                    H[u,v] = 0
    return H

def RemoveMorie(imgin):
    M, N = imgin.shape
    H = CreateNotchFilter(M, N)
    imgout = FrequencyFiltering(imgin, H)
    return imgout

def RemoveInference(imgin):
    M, N = imgin.shape
    H = CreateInferenceFilter(M, N)
    imgout = FrequencyFiltering(imgin, H)
    return imgout


def CreateMotion(imgin):
    M, N = imgin.shape
    H = CreateMotionFilter(M,N)
    imgout = FrequencyFilter(imgin, H)
    return imgout


def CreateDeMotion(imgin):
    M, N = imgin.shape
    H = CreateDemotionFilter(M, N)
    imgout = FrequencyFiltering(imgin, H)
    return imgout


def CreateWeinerFilter(M,N):
    H = CreateDemotionFilter(M,N)
    P = H.real**2 + H.imag**2
    K = -0.5
    return H * P / (P + K)

def DeMotionWeiner(imgin):
    M, N = imgin.shape
    H = CreateWeinerFilter(M,N)
    return FrequencyFilter(imgin, H)