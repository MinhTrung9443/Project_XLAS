import cv2
import numpy as np

L = 256

def Erosion(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45))
    imgout = cv2.erode(imgin, w)
    return imgout

def Dilation(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgout = cv2.dilate(imgin, w)
    return imgout
    
    
def Boundary(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    temp = cv2.erode(imgin, w)
    imgout = imgin - temp
    return imgout

def ConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 200, L-1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    dem, label = cv2.connectedComponents(temp)
    text = 'Co %d thanh phan lien thong' % (dem-1) 
    print(text)

    a = np.zeros(dem, np.int32)
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] = a[r] + 1
            if r > 0:
                label[x,y] = label[x,y] + color

    for r in range(1, dem):
        print('%4d %10d' % (r, a[r]))
    label = label.astype(np.uint8)
    cv2.putText(label,text,(1,25),cv2.FONT_HERSHEY_SIMPLEX,1.0, (255,255,255),2)
    return label

def ConvexHull(imgin):
    imgout = cv2.cvtColor(imgin, cv2.COLOR_GRAY2BGR)
    Contours, _ = cv2.findContours(imgin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Contour = Contours[0]
    p = cv2.convexHull(Contour, returnPoints=False)
    n = len(p)
    for i in range(0, n-1):
        vi_tri_1 = p[i][0]
        vi_tri_2 = p[i+1, 0]
        x1 = Contour[vi_tri_1][0][0]
        y1 = Contour[vi_tri_1][0][1]
        
        x2 = Contour[vi_tri_2][0][0]
        y2 = Contour[vi_tri_2][0][1]
        cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 2)
    vi_tri_1 = p[n-1][0]
    vi_tri_2 = p[0, 0]
    x1 = Contour[vi_tri_1][0][0]
    y1 = Contour[vi_tri_1][0][1]
    
    x2 = Contour[vi_tri_2][0][0]
    y2 = Contour[vi_tri_2][0][1]
    cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return imgout

def DefectDetect(imgin):
    imgout = cv2.cvtColor(imgin, cv2.COLOR_GRAY2BGR)
    Contours, _ = cv2.findContours(imgin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Contour = Contours[0]
    p = cv2.convexHull(Contour, returnPoints=False)
    n = len(p)
    for i in range(0, n-1):
        vi_tri_1 = p[i][0]
        vi_tri_2 = p[i+1, 0]
        x1 = Contour[vi_tri_1][0][0]
        y1 = Contour[vi_tri_1][0][1]
        
        x2 = Contour[vi_tri_2][0][0]
        y2 = Contour[vi_tri_2][0][1]
        cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 2)
    vi_tri_1 = p[n-1][0]
    vi_tri_2 = p[0, 0]
    x1 = Contour[vi_tri_1][0][0]
    y1 = Contour[vi_tri_1][0][1]
    
    x2 = Contour[vi_tri_2][0][0]
    y2 = Contour[vi_tri_2][0][1]
    cv2.line(imgout, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    
    data = cv2.convexityDefects(Contour, p)
    n = len(data)
    for i in range(0, n):
        if data[i,0,3] > 5000:
            vi_tri = data[i,0,2]
            x = Contour[vi_tri][0][0]
            y = Contour[vi_tri][0][1]
            cv2.circle(imgout, (x, y), 5, (0, 255, 0), -1)
        
    return imgout


def removeSmallRice(imgin):
    w = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81))
    temp = cv2.morphologyEx(imgin, cv2.MORPH_TOPHAT,w)
    nguong = 100
    _, temp = cv2.threshold(temp, nguong, L-1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    n, label = cv2.connectedComponents(temp, None)
    a = np.zeros(n, np.int32)
    M, N = label.shape
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            if r > 0:
                a[r] += 1
                
    max_value = np.max(a)
    imgout = np.zeros((M, N), np.uint8)
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            if r > 0:
                if a[r] > 0.7*max_value:
                    imgout[x, y] = L - 1
    return imgout

def Contour(imgin):
    #Bắt buộc imgin là ảnh nhị phân (có 2 màu: đen 0 và trắng 255)
    M, N = imgin.shape
    imgout = cv2.cvtColor(imgin, cv2.COLOR_GRAY2BGR)
    contours, _ =cv2.findContours(imgin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]
    n = len(contour)
    for i in range(0, n-1):
        x1 = contour[i][0][0]
        y1 = contour[i][0][1]

        x2 = contour[i+1][0][0]
        y2 = contour[i+1][0][1]

        cv2.line(imgout, (x1, y1), (x2, y2), (0, 255, 0), 2)

    x1 = contour[n-1][0][0]
    y1 = contour[n-1][0][1]

    x2 = contour[0][0][0]
    y2 = contour[0][0][1]

    cv2.line(imgout, (x1, y1), (x2, y2), (0, 255, 0), 2)


    return imgout