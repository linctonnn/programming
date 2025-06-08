# Depth First Search (DFS)
#
# INPUT
# A - matriks ketetanggaan. Matriks ini harus berbentuk persegi, simetris, dan biner dengan sumber nomor vertex.
#
# OUTPUT
# vertexList - daftar vertex berurutan yang ditemukan dalam pencarian

import numpy

def DFS(A, source):
  source -= 1
  n = A.shape[0]
  unvisited = [1] * n
  stack = [source]
  vertexList = []
  while stack:
    v = stack.pop()
    if unvisited[v]:
      vertexList.append(v)
      unvisited[v] = 0
    for u in range(n - 1, 0, -1):
      if A[v,u] == 1 and unvisited[u] == 1:
        stack.append(u)
  return vertexList

nomor_1 = numpy.array([
#  A  B  C  D  E  F  G  H  I  J  K  L  M  N
  [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A
  [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], # B
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # C
  [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], # D
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # E
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], # F
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # G
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # H
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # I
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], # J
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], # K
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], # L
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # M
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # N
])

nomor_2 = numpy.array([
#    A  B  C  D  E  F  G  H  I  J  K  L
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # B
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # C
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # D
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # E
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],  # G
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # H
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # I
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # J
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # K
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]   # L
]) 

A = numpy.array([
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])



vertex_list = DFS(A, 1)
# Representasi huruf untuk setiap vertex
print([x + 1 for x in vertex_list])
# mapping_abc_2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
# print("DFS: ", [mapping_abc_2[x] for x in nol_dfs])