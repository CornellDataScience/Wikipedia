import sys
import json


data = [['Linear algebra', 'Endomorphism', 'Topological space', 'Endomorphism', 'Linear algebra', 'Euclidean vector', 'Norm (mathematics)', 'Norm (mathematics)', 'Euclidean space', 'Norm (mathematics)'], ['Linear algebra', 'Linear system', 'Dynamical system', 'Chaos theory', 'Physics', 'Optics', 'Physics', 'Chaos theory', 'Science', 'Political science'], ['Linear algebra', 'Linear algebra', 'Inner product space', 'Space (mathematics)', 'Norm (mathematics)', 'Norm (mathematics)', 'Vector space', 'Functional analysis', 'Space (mathematics)', 'Functional analysis'], ['Linear algebra', 'Linear map', 'Function space', 'Continuous function', 'Map (mathematics)', 'Linear map', 'Eigenvalues and eigenvectors', 'Determinant', 'Linear map', 'Linear map'], ['Linear algebra', 'Transformation matrix', 'Translation (geometry)', 'Transformation matrix', 'Active and passive transformation', 'Eigenvalues and eigenvectors', 'Sparse matrix', 'Matrix calculus', 'Matrix (mathematics)', 'Stochastic matrix'], ['Linear algebra', 'Linear map', 'Linear function', 'Function space', 'Function (mathematics)', 'Calculus of variations', 'Nonlinear system', 'Soliton', 'Partial differential equation', 'Finite element method'], ['Linear algebra', 'Linear map', 'Functional analysis', 'Euclidean space', 'Inner product space', 'Space (mathematics)', 'Measure (mathematics)', 'Measure (mathematics)', 'Space (mathematics)', 'Functional analysis'], ['Linear algebra', 'Linear map', 'Linear function', 'Polynomial', 'Algebraic equation', 'Abstract algebra', 'Algebraic equation', 'System of linear equations', 'Determinant', 'Linear map'], ['Linear algebra', 'Function space', 'Function space', 'Eigenvalues and eigenvectors', 'Diagonal matrix', 'Rotation matrix', 'Diagonal matrix', 'Determinant', 'Matrix (mathematics)', 'Determinant'], ['Linear algebra', 'Linear regression', 'Variable (mathematics)', 'Functional (mathematics)', 'Continuous function', 'Function (mathematics)', 'Map (mathematics)', 'Graph of a function', 'Higher-order function', 'Function composition'], ['Linear algebra', 'Position (vector)', 'Coordinate system', 'Three-dimensional space', 'Dimension', 'Dimension (vector space)', 'Vector space', 'Functional analysis', 'Dimension (vector space)', 'Hilbert space'], ['Linear algebra', 'Orthonormal basis', 'Orthonormal basis', 'Hilbert space', 'Linear algebra', 'Nonlinear system', 'Integral equation', 'Integral', 'Function (mathematics)', 'Metric (mathematics)'], ['Linear algebra', 'Row and column vectors', 'Linear algebra', 'Linearization', 'System', 'Chaos theory', 'Chaos theory', 'Science', 'Computer science', 'Artificial intelligence'], ['Linear algebra', 'Linear algebra', 'Matrix (mathematics)', 'Row and column vectors', 'Linear algebra', 'Matrix calculus', 'Sparse matrix', 'Matrix calculus', 'Matrix (mathematics)', 'Rotation matrix'], ['Linear algebra', 'Endomorphism', 'Morphism', 'Banach space', 'Space (mathematics)', 'Manifold', 'Topology', 'Euclidean space', 'Hilbert space', 'Inner product space'], ['Linear algebra', 'Transformation matrix', 'Invertible matrix', 'Matrix addition', 'Determinant', 'Sparse matrix', 'Invertible matrix', 'Determinant', 'Linear map', 'Function space'], ['Linear algebra', 'Dimension (vector space)', 'Three-dimensional space', 'Space (mathematics)', 'Topological space', 'Functional analysis', 'Hilbert space', 'Function space', 'Functional analysis', 'Scalar (mathematics)'], ['Linear algebra', 'Inner product space', 'Space (mathematics)', 'Euclidean space', 'Topology', 'Topological space', 'Continuous function', 'Functional (mathematics)', 'Map (mathematics)', 'Linear function'], ['Linear algebra', 'Linear function', 'Linearization', 'Linear system', 'System of linear equations', 'Variable (mathematics)', 'System of linear equations', 'Variable (mathematics)', 'Continuous function', 'Point (geometry)'], ['Linear algebra', 'Linear function', 'Polynomial', 'Equation', 'Variable (mathematics)', 'Higher-order function', 'Functional analysis', 'Continuous function', 'Higher-order function', 'Calculus of variations'], ['Linear algebra', 'Inner product space', 'Hilbert space', 'Norm (mathematics)', 'Inner product space', 'Inner product space', 'Norm (mathematics)', 'Functional analysis', 'Functional (mathematics)', 'Linear function'], ['Linear algebra', 'Equation', 'Nonlinear system', 'Partial differential equation', 'Nonlinear system', 'Linear system', 'Linearization', 'Chaos theory', 'Dynamical system', 'Partial differential equation'], ['Linear algebra', 'Equation', 'Differential equation', 'Algebraic equation', 'Differential equation', 'Soliton', 'Optics', 'Optics', 'Soliton', 'Optics'], ['Linear algebra', 'Determinant', 'Sparse matrix', 'Row and column vectors', 'Matrix (mathematics)', 'Stochastic matrix', 'Quantum electrodynamics', 'Quantum electrodynamics', 'Quantum mechanics', 'Quantum electrodynamics'], ['Linear algebra', 'Linear function', 'Linear algebra', 'Linearization', 'Equation', 'Nonlinear system', 'Calculus of variations', 'Continuous function', 'Functional (mathematics)', 'Variable (mathematics)'], ['Linear algebra', 'Linear equation', 'Flat (geometry)', 'Flat (geometry)', 'Euclidean space', 'Euclidean space', 'Translation (geometry)', 'Translation (geometry)', 'Euclidean space', 'Position (vector)'], ['Linear algebra', 'Space (mathematics)', 'Continuous function', 'Morphism', 'Morphism', 'Endomorphism', 'Module (mathematics)', 'Endomorphism', 'Linear map', 'Function space'], ['Linear algebra', 'Eigenvalues and eigenvectors', 'Diagonal matrix', 'Diagonal matrix', 'Rotation matrix', 'Clockwise', 'Rotation (mathematics)', 'Rigid body', 'Rotation (mathematics)', 'Rotation (mathematics)'], ['Linear algebra', 'Nonlinear system', 'Linear equation', 'Algebraic equation', 'Nonlinear system', 'Calculus of variations', 'Function (mathematics)', 'Integral', 'Integral', 'Function (mathematics)'], ['Linear algebra', 'Vector space', 'Topological space', 'Banach space', 'Topological space', 'Topology', 'Manifold', 'Surface (topology)', 'Plane (geometry)', 'Plane (geometry)'], ['Linear algebra', 'Linearization', 'Linearization', 'Linear system', 'Linear regression', 'Linearization', 'Equation', 'Calculus of variations', 'Integral equation', 'Mathematical analysis'], ['Linear algebra', 'Linear algebra', 'Three-dimensional space', 'Position (vector)', 'Active and passive transformation', 'Eigenvalues and eigenvectors', 'Linear map', 'Linear map', 'Matrix (mathematics)', 'Eigenvalues and eigenvectors'], ['Linear algebra', 'Banach space', 'Norm (mathematics)', 'Dimension (vector space)', 'Norm (mathematics)', 'Scalar (mathematics)', 'Dimension (vector space)', 'Three-dimensional space', 'Dimension (vector space)', 'Space (mathematics)'], ['Linear algebra', 'Eigenvalues and eigenvectors', 'Sparse matrix', 'Matrix calculus', 'Matrix addition', 'Eigenvalues and eigenvectors', 'Transformation matrix', 'Linear algebra', 'Nonlinear system', 'Soliton'], ['Linear algebra', 'Space (mathematics)', 'Vector space', 'Endomorphism', 'Linear map', 'Scalar (mathematics)', 'Norm (mathematics)', 'Functional analysis', 'Norm (mathematics)', 'Space (mathematics)'], ['Linear algebra', 'Determinant', 'System of linear equations', 'Soliton', 'Quantum mechanics', 'Chaos theory', 'Artificial intelligence', 'Chaos theory', 'Mathematical model', 'Chaos theory'], ['Linear algebra', 'Endomorphism', 'Function composition', 'Exponential function', 'Function (mathematics)', 'Taylor series', 'Mathematical analysis', 'Space (mathematics)', 'Linear algebra', 'Nonlinear system'], ['Linear algebra', 'Three-dimensional space', 'Incidence geometry', 'Incidence geometry', 'Three-dimensional space', 'Line (geometry)', 'Analytic geometry', 'Coordinate system', 'Origin (mathematics)', 'Position (vector)'], ['Linear algebra', 'Linear function', 'Eigenvalues and eigenvectors', 'Eigenvalues and eigenvectors', 'Active and passive transformation', 'Rotation (mathematics)', 'Rigid body', 'Classical mechanics', 'Physics', 'Chaos theory'], ['Linear algebra', 'Linear map', 'Endomorphism', 'Module homomorphism', 'Morphism', 'Module homomorphism', 'Ring (mathematics)', 'Endomorphism', 'Topological space', 'Metric (mathematics)'], ['Linear algebra', 'Banach space', 'Endomorphism', 'Linear algebra', 'Space (mathematics)', 'Measure (mathematics)', 'Measure (mathematics)', 'Measure (mathematics)', 'Space (mathematics)', 'Vector space'], ['Linear algebra', 'Hilbert space', 'Unitary operator', 'Functional analysis', 'Inner product space', 'Vector space', 'Position (vector)', 'Eigenvalues and eigenvectors', 'Euclidean vector', 'Euclidean vector'], ['Linear algebra', 'Linearization', 'Linear regression', 'Linear system', 'Chaos theory', 'System of linear equations', 'Differential equation', 'Mathematical analysis', 'Hilbert space', 'Function space'], ['Linear algebra', 'Endomorphism', 'Vector space', 'Three-dimensional space', 'Euclidean vector', 'Scalar multiplication', 'Euclidean vector', 'Euclidean vector', 'Euclidean vector', 'Plane (geometry)'], ['Linear algebra', 'Eigenvalues and eigenvectors', 'Active and passive transformation', 'Transformation matrix', 'Translation (geometry)', 'Euclidean vector', 'Row and column vectors', 'Matrix (mathematics)', 'Transformation matrix', 'Affine geometry'], ['Linear algebra', 'Norm (mathematics)', 'Euclidean vector', 'Linear algebra', 'Euclidean vector', 'Eigenvalues and eigenvectors', 'Scalar multiplication', 'Function space', 'Vector space', 'Row and column vectors'], ['Linear algebra', 'Linearization', 'Linear regression', 'Linear equation', 'Partial differential equation', 'Algebraic equation', 'Eigenvalues and eigenvectors', 'Transformation matrix', 'Translation (geometry)', 'Translation (geometry)'], ['Linear algebra', 'Equation', 'Eigenvalues and eigenvectors', 'Dimension (vector space)', 'Orthonormal basis', 'Vector space', 'Position (vector)', 'Position (vector)', 'Origin (mathematics)', 'Two-dimensional space'], ['Linear algebra', 'Linearization', 'System of linear equations', 'Nonlinear system', 'Mathematical analysis', 'Integral', 'Three-dimensional space', 'Two-dimensional space', 'Euclidean space', 'Rotation (mathematics)'], ['Linear algebra', 'Banach space', 'Function (mathematics)', 'Integral', 'Function composition', 'Functional (mathematics)', 'Function composition', 'Functional (mathematics)', 'Higher-order function', 'Functional analysis'], ['Linear algebra', 'Endomorphism', 'Function space', 'Function space', 'Linear map', 'Map (mathematics)', 'Map (mathematics)', 'Continuous function', 'Fourier transform', 'Transformation (function)'], ['Linear algebra', 'Position (vector)', 'Translation (geometry)', 'Transformation matrix', 'Matrix (mathematics)', 'Invertible matrix', 'Determinant', 'Transformation matrix', 'Transformation matrix', 'Matrix (mathematics)'], ['Linear algebra', 'Plane (geometry)', 'Projective geometry', 'Transformation matrix', 'Active and passive transformation', 'Eigenvalues and eigenvectors', 'Vector space', 'Topological space', 'Banach space', 'Morphism'], ['Linear algebra', 'Three-dimensional space', 'Plane (geometry)', 'Differential geometry', 'Analytic geometry', 'Origin (mathematics)', 'Line (geometry)', 'Three-dimensional space', 'Euclidean vector', 'Row and column vectors'], ['Linear algebra', 'Space (mathematics)', 'Linear algebra', 'Dimension (vector space)', 'Scalar (mathematics)', 'Functional analysis', 'Higher-order function', 'Term (logic)', 'Constant term', 'Coefficient'], ['Linear algebra', 'Nonlinear system', 'Differential equation', 'Differential equation', 'Finite element method', 'Nonlinear system', 'Calculus of variations', 'Calculus of variations', 'Function (mathematics)', 'Graph of a function'], ['Linear algebra', 'Active and passive transformation', 'Vector space', 'Euclidean space', 'Analytic geometry', 'Analytic geometry', 'Plane (geometry)', 'Geometry', 'Point (geometry)', 'Incidence geometry'], ['Linear algebra', 'Inner product space', 'Norm (mathematics)', 'Dimension (vector space)', 'Endomorphism', 'Group (mathematics)', 'Abstract algebra', 'Group (mathematics)', 'Endomorphism', 'Ring (mathematics)'], ['Linear algebra', 'Linear equation', 'Linear algebra', 'Linear map', 'Functional analysis', 'Stefan Banach', 'Functional analysis', 'Linear algebra', 'Equation', 'System of linear equations'], ['Linear algebra', 'Linear map', 'Linear map', 'Matrix (mathematics)', 'System of linear equations', 'Analytic geometry', 'Differential geometry', 'Manifold', 'Topology', 'Topological space'], ['Linear algebra', 'Three-dimensional space', 'Coordinate system', 'Coordinate system', 'Two-dimensional space', 'Geodesic', 'Metric (mathematics)', 'Continuous function', 'Higher-order function', 'Graph of a function'], ['Linear algebra', 'Row and column vectors', 'Vector space', 'Eigenvalues and eigenvectors', 'Nonlinear system', 'Differential equation', 'Nonlinear system', 'Differential equation', 'Numerical analysis', 'Linearization'], ['Linear algebra', 'Banach space', 'Transformation (function)', 'Function (mathematics)', 'Continuous function', 'Metric (mathematics)', 'Euclidean space', 'Banach space', 'Banach space', 'Function space'], ['Linear algebra', 'Linear regression', 'Variable (mathematics)', 'Higher-order function', 'Functional analysis', 'Scalar (mathematics)', 'Scalar multiplication', 'Function space', 'Vector space', 'Continuous function'], ['Linear algebra', 'Hilbert space', 'Vector space', 'Hilbert space', 'Calculus of variations', 'Mathematical analysis', 'Hilbert space', 'Euclidean space', 'Line (geometry)', 'Three-dimensional space'], ['Linear algebra', 'Norm (mathematics)', 'Inner product space', 'Vector space', 'Euclidean vector', 'Linear algebra', 'Three-dimensional space', 'Linear algebra', 'Transformation matrix', 'Determinant'], ['Linear algebra', 'Inner product space', 'Orthonormal basis', 'Banach space', 'Linear algebra', 'Function space', 'Linear function', 'Scalar (mathematics)', 'Linear map', 'Scalar (mathematics)'], ['Linear algebra', 'Linear system', 'Chaos theory', 'System', 'System of linear equations', 'Chaos theory', '3D modeling', 'Mathematical model', 'Linear regression', 'Linear function'], ['Linear algebra', 'Euclidean vector', 'Position (vector)', 'Scalar (mathematics)', 'Inner product space', 'Space (mathematics)', 'Dimension (vector space)', 'Endomorphism', 'Banach space', 'Endomorphism'], ['Linear algebra', 'Dimension (vector space)', 'Dimension', 'Dimension', 'Euclidean space', 'Flat (geometry)', 'Euclidean space', 'Vector space', 'Norm (mathematics)', 'Norm (mathematics)'], ['Linear algebra', 'Euclidean vector', 'Eigenvalues and eigenvectors', 'Linear function', 'Linear map', 'Determinant', 'System of linear equations', 'Linear algebra', 'Scalar (mathematics)', 'Linear function'], ['Linear algebra', 'Position (vector)', 'Coordinate system', 'Position (vector)', 'Translation (geometry)', 'Euclidean vector', 'Euclidean space', 'Projective geometry', 'Three-dimensional space', 'Linear equation'], ['Linear algebra', 'Linear map', 'Norm (mathematics)', 'Linear map', 'Endomorphism', 'Abstract algebra', 'Algebraic equation', 'Algebraic equation', 'Abstract algebra', 'Category theory'], ['Linear algebra', 'Norm (mathematics)', 'Function space', 'Space (mathematics)', 'Euclidean space', 'Functional analysis', 'Topology', 'Topological space', 'Euclidean space', 'Affine geometry'], ['Linear algebra', 'Hilbert space', 'Norm (mathematics)', 'Inner product space', 'Scalar (mathematics)', 'Linear map', 'Linear map', 'Linear algebra', 'Dynamical system', 'Vector space'], ['Linear algebra', 'Euclidean vector', 'Vector space', 'Space (mathematics)', 'Dimension (vector space)', 'Function space', 'Calculus of variations', 'Higher-order function', 'Calculus of variations', 'Differential equation'], ['Linear algebra', 'Space (mathematics)', 'Banach space', 'Morphism', 'Continuous function', 'Topological space', 'Space (mathematics)', 'Inner product space', 'Vector space', 'Topological space'], ['Linear algebra', 'Linear system', 'Linearization', 'System', 'Mathematical model', 'Linear regression', 'Variable (mathematics)', 'Exponential function', 'Function composition', 'Fourier transform'], ['Linear algebra', 'Scalar multiplication', 'Euclidean vector', 'Euclidean space', 'Flat (geometry)', 'Linear equation', 'Partial differential equation', 'Nonlinear system', 'Linear algebra', 'Active and passive transformation'], ['Linear algebra', 'Scalar (mathematics)', 'Scalar (mathematics)', 'Functional analysis', 'Topological space', 'Banach space', 'Morphism', 'Function (mathematics)', 'Morphism', 'Function (mathematics)'], ['Linear algebra', 'Inner product space', 'Hilbert space', 'Euclidean space', 'Differential geometry', 'Topology', 'Differential geometry', 'Geometry', 'Line (geometry)', 'Incidence geometry'], ['Linear algebra', 'Linear system', 'Linearization', 'System', 'Linear system', 'Linear algebra', 'Dynamical system', 'Linearization', 'Linearization', 'Nonlinear system'], ['Linear algebra', 'Linearization', 'Equation', 'Nonlinear system', 'Dynamical system', 'Linear system', 'System', 'Axiomatic system', 'System', 'Axiomatic system'], ['Linear algebra', 'Row and column vectors', 'Vector space', 'Endomorphism', 'Banach space', 'Norm (mathematics)', 'Banach space', 'Space (mathematics)', 'Projective geometry', 'Three-dimensional space'], ['Linear algebra', 'Matrix calculus', 'Matrix (mathematics)', 'Stochastic matrix', 'Diagonal matrix', 'Matrix (mathematics)', 'Diagonal matrix', 'Matrix (mathematics)', 'Transformation matrix', 'Matrix (mathematics)'], ['Linear algebra', 'Plane (geometry)', 'Line (geometry)', 'Line (geometry)', 'Linear equation', 'Flat (geometry)', 'Flat (geometry)', 'Linear equation', 'Differential equation', 'Differential equation'], ['Linear algebra', 'Dynamical system', 'Equation', 'Eigenvalues and eigenvectors', 'Active and passive transformation', 'Transformation matrix', 'Matrix (mathematics)', 'Matrix calculus', 'Linear algebra', 'Linear equation'], ['Linear algebra', 'Space (mathematics)', 'Three-dimensional space', 'Integral', 'Integral', 'Calculus of variations', 'Geodesic', 'Differential geometry', 'Geodesic', 'Calculus of variations'], ['Linear algebra', 'Determinant', 'Linear algebra', 'System of linear equations', 'System', 'Linear system', 'Linear system', 'Linear regression', 'Linear algebra', 'Norm (mathematics)'], ['Linear algebra', 'Nonlinear system', 'Eigenvalues and eigenvectors', 'Dimension (vector space)', 'Dimension', 'Space (mathematics)', 'Point (geometry)', 'Non-Euclidean geometry', 'Affine geometry', 'Projective geometry'], ['Linear algebra', 'Matrix calculus', 'Linear algebra', 'Linearization', 'Dynamical system', 'Nonlinear system', 'System of linear equations', 'Algebraic equation', 'Linear equation', 'Eigenvalues and eigenvectors'], ['Linear algebra', 'Scalar multiplication', 'Vector space', 'Endomorphism', 'Category of modules', 'Ring (mathematics)', 'Module homomorphism', 'Category of modules', 'Endomorphism', 'Endomorphism'], ['Linear algebra', 'Equation', 'Partial differential equation', 'Dynamical system', 'System of linear equations', 'Linearization', 'Finite element method', 'Mathematical analysis', 'Space (mathematics)', 'Banach space'], ['Linear algebra', 'Row and column vectors', 'Linear algebra', 'Three-dimensional space', 'Surface (topology)', 'Manifold', 'Geodesic', 'Metric (mathematics)', 'Topological space', 'Topological space'], ['Linear algebra', 'Eigenvalues and eigenvectors', 'Linear map', 'Functional analysis', 'Function (mathematics)', 'Mathematical analysis', 'Geometry', 'Mathematical analysis', 'Functional (mathematics)', 'Map (mathematics)'], ['Linear algebra', 'Linear map', 'Dimension (vector space)', 'Functional analysis', 'Linear map', 'Map (mathematics)', 'Continuous function', 'Taylor series', 'Fourier series', 'Taylor series'], ['Linear algebra', 'Active and passive transformation', 'Vector space', 'Metric (mathematics)', 'Geodesic', 'Geometry', 'Plane (geometry)', 'Three-dimensional space', 'Incidence geometry', 'Euclidean geometry'], ['Linear algebra', 'System of linear equations', 'Linear equation', 'Linear equation', 'Eigenvalues and eigenvectors', 'Sparse matrix', 'Row and column vectors', 'Linear algebra', 'Linear equation', 'Incidence geometry'], ['Linear algebra', 'Transformation matrix', 'Determinant', 'System of linear equations', 'Eigenvalues and eigenvectors', 'Row and column vectors', 'Vector space', 'Dynamical system', 'Linearization', 'System'], ['Linear algebra', 'Determinant', 'Eigenvalues and eigenvectors', 'Scalar multiplication', 'Eigenvalues and eigenvectors', 'Matrix (mathematics)', 'Invertible matrix', 'Matrix (mathematics)', 'Row and column vectors', 'Sparse matrix']]

def calculate_times(word, list):
    i = 0
    for rows in list:
        for item in rows:
            if (item == word):
                i += 1
    return i

def process_list(data, n):
    list = []
    for i in range(len(data[0])):
        if i <= n:
            innerlist = []
            k = 0
            for j in range(len(data)):
                innerlist.append(data[j][i])
                k += 1
                if k > i:
                    break
            list.append(innerlist)
        else:
            return list
    # print(list)
    return list


def generate_json(lst,acc):
    # for i in rang(len(list)):
    if lst==[]:
        return []
    else:
        dic = {}
        dic["name"]= str(acc)
        dic["children"]=[{"name":i, "size":10} for i in lst[0]]
        dic["children"] = dic["children"] + [generate_json(lst[1:],acc+1)]
        return dic

if __name__ == '__main__':
    n = int(sys.argv[1])
    #b = int(sys.argv[2])
    lst = process_list(data, n)
    # print("before reverse", lst)
    lst[0] = lst[0] + ['Placeholder']
    list.reverse(lst)
    # print("after reverse", lst)
    result_json = generate_json(lst,0)
    print(result_json)
    with open('result.json', 'w') as fp:
        json.dump(result_json, fp)
