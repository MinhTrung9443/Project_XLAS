import numpy as np
import cv2

L = 256

def Negative(imgin):
    #M: độ cao của ảnh
    #N: độ rộng của ảnh
    M, N = imgin.shape

    #Tạo imgout có kích thước bằng imgin có màu đen
    imgout = np.zeros((M,N),np.uint8) + np.uint8(255)
    
    #Quét ảnh: xét từng phần tử của ma trận
    for x in range(0,M):
        for y in range(0,N):
            r = imgin[x,y]
            s = L - 1 - r
            imgout[x,y] = np.uint8(s)
    return imgout

def Logarit(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N),np.uint8) + np.uint8(255)
    c = (L - 1)/np.log(1.0*L)
    for x in range (0,M):
        for y in range(0,N):
            r = imgin[x,y]
            if r == 0:
                r = 1
            s = c*np.log(1.0 + r)
            imgout[x,y] = np.uint8(s)
    return imgout

def Power(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N),np.uint8) + np.uint8(255)
    gamma = 5.0
    c = np.power(L-1.0, 1-gamma)
    for x in range (0,M):
        for y in range(0,N):
            r = imgin[x,y]
            if r == 0:
                r = 1
            s = c*np.power(1.0*r, gamma)
            imgout[x,y] = np.uint8(s)
    return imgout

def PiecewiseLinear(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N),np.uint8) + np.uint8(255)
    rmin, rmax, _, _ = cv2.minMaxLoc(imgin)
    r1 = rmin
    s1 = 0
    r2 = rmax
    s2 = L - 1
    for x in range (0, M):
        for y in range(0, N):
            r = imgin[x,y]
            #Đoạn 1:
            if r < r1:
                s = 1.0 * s1 / r1 * r
            #Đoạn 2:
            elif r < r2:
                s = 1.0 * (s2 - s1) / (r2 - r1) * (r - r1) + s1
            #Đoạn 3:
            else:
                s = 1.0 * (L - 1 - s2) / (L - 1 - r2) * (r - r2) + s2
            imgout[x,y] = np.uint8(s)
    return imgout

def Histogram(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, L), np.uint8) + np.uint8(255)
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1
    p = 1.0*h/(M*N)
    scale = 3000
    for r in range(0, L):
        cv2.line(imgout, (r, M - 1), (r, M - 1 - np.int32(scale*p[r])), (0, 0, 0))
    return imgout

def HistEqual(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r] + 1
    p = 1.0*h/(M*N)
    s = np.zeros(L, np.float32)
    for k in range(0, L):
        for j in range(0, k + 1):
            s[k] = s[k] + p[j]
    
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            imgout[x, y] = np.uint8((L-1)*s[r])
    return imgout

def HistEqualColor(imgin):
    #Anh mau cua opencv la BGR
    #Anh mau cua pillow la RGB
    #Pillow la module Xu ly anh cua python
    b = imgin[:,:,0]
    g = imgin[:,:,1]
    r = imgin[:,:,2]

    b = cv2.equalizeHist(b)
    g = cv2.equalizeHist(g)
    r = cv2.equalizeHist(r)

    imgout = imgin.copy()
    imgout[:,:,0]=b
    imgout[:,:,1]=g
    imgout[:,:,2]=r
    return imgout

def LocalHist(imgin):
    #Ảnh là ma trận M hàng N cột 
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    a = m // 2
    b = m // 2
    for x in range(a, M-a):
        for y in range(b, N-b):
            w = imgin[x-a:x+a+1, y-b:y+b+1]
            w = cv2.equalizeHist(w)
            imgout[x,y]=w[a,b]
    return imgout

def HistStat(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N), np.uint8)
    
    # sum = 0.0
    # for x in range(0, M):
    #     for y in range(0,N):
    #         sum = sum + imgin[x,y]           
    # my_mean = sum/(M*N)
    
    # sum = 0.0
    # for x in range(0, M):
    #     for y in range(0,N):
    #         sum = sum + (imgin[x,y] - my_mean)**2
            
    # variance = sum/(M*N)
    # my_stddev = np.sqrt(variance)
    # print(my_mean, my_stddev)  c
    
    mean, stddev = cv2.meanStdDev(imgin)
    mG = mean[0,0]
    sigmaG = stddev[0,0]
    C = 22.8
    k0 = 0.0
    k1 = 0.1
    k2 = 0.0 
    k3 = 0.1
    
    m = 3
    n = 3
    a = m // 2
    b = m // 2
    for x in range(a, M-a):
        for y in range(b, N-b):
            w = imgin[x-a:x+a+1, y-b:y+b+1]
            mean, stddev = cv2.meanStdDev(w)
            msxy = mean[0,0]
            sigmasxy = stddev[0,0]
            if (k0*mG <= msxy <= k1*mG) and (k2*sigmaG <= sigmasxy <= k3*sigmaG):
                imgout[x,y] = np.uint8(C * imgin[x,y])
            else:
                imgout[x,y] = imgin[x,y]
    
    return imgout

def MyBoxFilter(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N), np.uint8)
    m = 11
    n = 11
    w = np.ones((m,n))
    w = w/(m*n)

    a = m // 2
    b = n // 2
    for x in range(a, M-a):
        for y in range(b, M-b):
            r = 0.0
            for s in range(-a, a+1):
                for t in range(-b, b+1):
                    r = r + w[s+a,t+b]*imgin[x+s,y+t]
            imgout[x,y] = np.uint8(r)
    return imgout

def BoxFilter(imgin):
    m = 21
    n = 21
    w = np.ones((m,n))
    w = w/(m*n)
    imgout = cv2.filter2D(imgin,cv2.CV_8UC1,w)
    return imgout

def Threshold(imgin):
    temp = cv2.blur(imgin, (15,15))
    retval, imgout = cv2.threshold(temp,64,255,cv2.THRESH_BINARY)
    return imgout

def MedianFilter(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M,N), np.uint8)
    m = 5
    n = 5
    w = np.zeros((m,n), np.uint8)
    a = m // 2
    b = n // 2
    for x in range(0, M):
        for y in range(0, N):
            for s in range(-a, a+1):
                for t in range(-b, b+1):
                    w[s+a,t+b] = imgin[(x+s)%M,(y+t)%N]
            w_1D = np.reshape(w, (m*n,))
            w_1D = np.sort(w_1D)
            imgout[x,y] = w_1D[m*n//2]
    return imgout

def Sharpen(imgin):
    # Đạo hàm cấp 2 của ảnh
    w = np.array([[1,1,1],[1,-8,1],[1,1,1]])
    temp = cv2.filter2D(imgin,cv2.CV_32FC1,w)

    # Hàm cv2.Laplacian chỉ tính đạo hàm cấp 2
    # cho bộ lọc có số -4 chính giữa
    imgout = imgin - temp
    imgout = np.clip(imgout, 0, L-1)
    imgout = imgout.astype(np.uint8)
    return imgout
 
def Gradient(imgin):
    sobel_x = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    sobel_y = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    # Đạo hàm cấp 1 theo hướng x
    mygx = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_x)
    # Đạo hàm cấp 1 theo hướng y
    mygy = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_y)

    # Lưu ý: cv2.Sobel có hướng x nằm ngang
    # ngược lại với sách Digital Image Processing
    gx = cv2.Sobel(imgin,cv2.CV_32FC1, dx = 1, dy = 0)
    gy = cv2.Sobel(imgin,cv2.CV_32FC1, dx = 0, dy = 1)

    imgout = abs(gx) + abs(gy)
    imgout = np.clip(imgout, 0, L-1)
    imgout = imgout.astype(np.uint8)
    return imgout


def Sharpening(imgin):
    w = np.array([[1 , 1, 1],[1, -8, 1], [1, 1, 1]], np.float32)
    Laplacian = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    imgout = imgin - Laplacian
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout


# def SharpeningMask(imgin):
#     M, N = imgin.shape
#     imgout = np.zeros((M, N), np.uint8)
#     temp = cv2.GaussianBlur(imgin, (5, 5), 3.0)
#     mask = imgin - temp
#     k = 1.0
#     imgout = imgin + k*mask
#     rmin, rmax, _, _ = cv2.minMaxLoc(imgout)
#     print(rmin, rmax)
#     imgout = (L-1)*(imgout - rmin)/(rmax - rmin)
#     imgout = np.clip(imgout, 0, L-1)
#     imgout = imgout.astype(np.uint8)
#     return imgout

def create_gauss_filter(m, n, sigma):
    w = np.zeros((m, n), np.float32)

    a = m // 2
    b = n // 2

    for s in range(-a, a + 1):
        for t in range (-b, b+1):
            w[s+a, t+b] = np.exp(-(s*s + t*t)/(2*sigma*sigma)) 

    K = 0
    for x in range(0, m):
        for y in range (0, n):
            K = K + w[x, y]

    return K

def MySharpeningMask(imgin):
    m = 3
    n = 3
    sigma = 1.0
    temp = cv2.GaussianBlur(imgin, (m, n), sigma).astype(np.float64)
    mask = imgin - temp
    k = 20.2
    imgout = imgin + k*mask
    imgout = np.clip(imgout, 0, L-1).astype(np.uint8)
    return imgout


def SharpeningMask(imgin):
    m = 3
    n = 3
    sigma = 1.0
    w = create_gauss_filter(m, n, sigma)
    temp = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    mask = imgin - temp
    rmin, rmax, _, _ = cv2.minMaxLoc(mask)
    mask = mask - rmin
    k = 5.0
    imgout = imgin + k*mask
    imgout = np.clip(imgout, 0, L-1).astype(np.uint8)
    return imgout


def Grandient(imgin):
    gx = cv2.Sobel(imgin, cv2.CV_32FC1, 1, 0)
    gy = cv2.Sobel(imgin, cv2.CV_32FC1, 0, 1)
    imgout  = abs(gx) + abs(gy)
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout
















