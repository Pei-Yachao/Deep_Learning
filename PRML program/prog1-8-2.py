# -*- coding: utf-8 -*-
import sys
from numpy import *
from scipy import linalg
from matplotlib.pyplot import *

data = loadtxt(sys.argv[1], delimiter="\t")

xs = data[0:2,:].T   # �w�K�f�[�^ [[x0,y0], [x1,y1], ...]
cs = int_(data[2,:]) # �����N���X [c0, c1, ...]

# �w�K�f�[�^�̐�
N = len(xs)

# �N���X�̐�
K = max(cs)+1

#### �����x�N�g���̕ϊ��֐� ####
def phi(x):
    return [x[0], x[1], 1]
    #return [x[0]**2, x[1]**2, x[0]*x[1], x[0], x[1], 1]

#### �p�����[�^�̍œK�� ####
# phi(�����x�N�g��)���s�ɕ��ׂ��s��
X = array([ phi(xs[i]) for i in range(N) ])

# �����N���X�ԍ��̐�������1�ɂ����x�N�g��p��
# �s�ɕ��ׂ��s��
P = zeros([N, K])
for i in range(N):
    P[i, cs[i]] = 1

# X^TXA = X^TP �𖞂��� A �����߂�p�����[�^
A = linalg.solve(X.T.dot(X), X.T.dot(P))

# �[���t�s����g���ꍇ
# A = linalg.pinv(X).dot(P)

# �ŏ����@�����s���Ă����֐�������܂�
# A,residues,rank,s=linalg.lstsq(X, P)

#### ���ʊ�̍\�z ####
def distance(x, i):
    t = zeros(K)
    t[i] = 1
    return linalg.norm(x-t)

# (x, y) �� (0,...,0,1,0,...,0) �̋������ŏ��̃N���X�ɕ���
def classify(x, y):
    p = A.T.dot(phi([x, y]))
    return argmin([distance(p, i) for i in range(K)])

#### �ǂ�Ȋ����ŋ�Ԃ��������ꂽ�����Ă݂܂��傤 ####
# �\���̈�̐ݒ�
xmin = min(xs[:,0]); xmax = max(xs[:,0])
ymin = min(xs[:,1]); ymax = max(xs[:,1])
xmin -= (xmax-xmin)/20
xmax += (xmax-xmin)/20
ymin -= (ymax-ymin)/20
ymax += (ymax-ymin)/20
xlim(xmin, xmax)
ylim(ymin, ymax)

X, Y = meshgrid(linspace(xmin, xmax, 100), linspace(ymin, ymax, 100))
Z = vectorize(classify)(X, Y)
pcolor(X, Y, Z, alpha=0.1)
scatter(xs[:,0], xs[:,1], c=cs, s = 50, linewidth=0)
show()