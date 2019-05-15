stp(Retea, Root, Edges) :- Root = 2, Edges = [[4,1], [2, 3], [3, 4], [4, 5]].
drum(Retea, From, To, Root, Edges, Path) :- Root = 2, Edges = [[4,1], [2, 3], [3, 4], [4, 5]], Path = [5, 4, 1].
