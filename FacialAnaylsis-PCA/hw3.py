from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    # Your implementation goes here!
    x = np.load(filename)
    x = x - np.mean(x, axis=0)
    return x

def get_covariance(dataset):
    # Your implementation goes here!
    x = dataset
    x = np.dot(np.transpose(x), x) / (len(x) -1)
    return x


def get_eig(S, m):
    # Your implementation goes here!
    x, y = eigh(S)
    x = np.sort(x)[:: -1]
    x = x[0:m]
    x = np.diag(x)

    y = np.array(y[:len(y), ::-1])
    y = np.array(y[:len(y), 0:m])
    return x,y



def get_eig_prop(S, prop):
    # Your implementation goes here!
    x = eigh(S)[0]
    sum = np.sum(x)
    for i in range(len(x)):
        x[i] = x[i] / sum

    x = x[x[:] > 0.07]

    for i in range(len(x)):
        x[i] = x[i] * sum

    x = np.sort(x)[:: -1]
    x = np.diag(x)

    z = [sum * prop, np.inf]
    y = eigh(S, subset_by_value=z)[1]
    y = np.array(y[:len(y), ::-1])
    y = np.array(y[:len(y), 0:len(x)])
    return x,y


def project_image(image, U):
    # Your implementation goes here!
    x = np.dot(np.transpose(U), image)
    return np.dot(U, x)


def display_image(orig, proj):
    # Your implementation goes here!
    orig = (np.reshape(orig, (32,32))).transpose()
    proj = (np.reshape(proj, (32,32))).transpose()
    x, (title1, title2) = plt.subplots(1,2)
    title1.set_title("Original")
    title2.set_title("Projection")
    img1 = title1.imshow(orig)
    img2 = title2.imshow(proj)
    x.colorbar(img1, ax = title1)
    x.colorbar(img2, ax = title2)
    plt.show()
    pass

