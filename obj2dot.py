import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def loadOBJ(fliePath):
    numVertices = 0
    numUVs = 0
    numNormals = 0
    numFaces = 0
    vertices = []
    uvs = []
    normals = []
    vertexColors = []
    faceVertIDs = []
    uvIDs = []
    normalIDs = []
    for line in open(fliePath, "r"):
        vals = line.split()
        if len(vals) == 0:
            continue
        if vals[0] == "v":
            v = [float(i) for i in vals[1:4]]
            vertices.append(v)
            if len(vals) == 7:
                vc = [float(i) for i in vals[4:7]]
                vertexColors.append(vc)
            numVertices += 1
        if vals[0] == "vt":
            vt = [float(i) for i in vals[1:4]]
            uvs.append(vt)
            numUVs += 1
        if vals[0] == "vn":
            vn = [float(i) for i in vals[1:4]]
            normals.append(vn)
            numNormals += 1
        if vals[0] == "f":
            fvID = []
            uvID = []
            nvID = []
            for f in vals[1:]:
                w = f.split("/")
                if numVertices > 0:
                    fvID.append(int(w[0])-1)
                if numUVs > 0:
                    uvID.append(int(w[1])-1)
                if numNormals > 0:
                    nvID.append(int(w[2])-1)
            faceVertIDs.append(fvID)
            uvIDs.append(uvID)
            normalIDs.append(nvID)
            numFaces += 1
    print("numVertices: ", numVertices)
    print("numUVs: ", numUVs)
    print("numNormals: ", numNormals)
    print("numFaces: ", numFaces)
    return vertices, uvs, normals, faceVertIDs, uvIDs, normalIDs, vertexColors

def obj2dot(vertices, size):
    xmax = vertices[:,0].max()
    xmin = vertices[:, 0].min()
    ymax = vertices[:, 1].max()
    ymin = vertices[:, 1].min()
    zmax = vertices[:, 2].max()
    zmin = vertices[:, 2].min()

    #原点を(0,0,0)に移動
    vertices[:, 0] = vertices[:, 0] - xmin
    vertices[:, 1] = vertices[:, 1] - ymin
    vertices[:, 2] = vertices[:, 2] - zmin

    #正規化係数の計算
    xlangth = xmax - xmin
    ylangth = ymax - ymin
    zlangth = zmax - zmin
    maxlength = max(xlangth, ylangth, zlangth)
    resize_coef = size/maxlength
    #座標をx,y,zのサイズに正規化
    resize = np.empty(vertices.shape)
    resize[:, 0] = vertices[:, 0] * resize_coef
    resize[:, 1] = vertices[:, 1] * resize_coef
    resize[:, 2] = vertices[:, 2] * resize_coef

    #整数に直して重複する点を削除
    resize = resize.astype(np.int16)
    resize = np.unique(resize, axis=0)
    return resize

#結果の描画
def plot_result(vertices, size):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    sc = ax1.scatter(vertices[:, 0], vertices[:, 1], zs=vertices[:, 2], marker='s',zdir='z', s=30, vmin=0, vmax=1)
    ax1.set_xlabel("X-axis")
    ax1.set_ylabel("Y-axis")
    ax1.set_zlabel("Z-axis")
    ax1.set_xlim(0, size)
    ax1.set_ylim(0, size)
    ax1.set_zlim(0, size)

    plt.show()

if __name__ == "__main__":
    vertices, uvs, normals, faceVertIDs, uvIDs, normalIDs, vertexColors = loadOBJ('model/Model_D0903B79/lgu.OBJ')
    P = np.array(vertices)
    P = obj2dot(P, 128)

    np.savetxt('./output/lgu.csv', P, delimiter=',', fmt='%d')

    plot_result(P, 128)