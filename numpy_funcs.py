## Линейные трансформации numpy
X1, y1 = make_blobs(n_samples=1000, centers=[[0, 0]], random_state=42)
## первая строка - куда смотрит ось x (i) после трансформации
## вторая строка - куда смотрит ось y (j) после трансформации

no_transformation = np.array([[1, 0],[0,1]])
extension_x = np.array([[2, 0],[0,1]])
extension_y = np.array([[1, 0],[0,2]])
rotation_90 = np.array([[0, 1],[-1,0]])
ext_x_thin_y_rotation_90 = np.array([[0, 2],[-0.2,0]])
X_res = X1.dot(ext_x_thin_y_rotation_90)
