#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True
#cython: nonecheck=False
#cython: profile=False
#cython: infer_types=False
import numpy as np
from libc.stdlib cimport malloc, free
from cython.parallel import prange


cdef extern from 'bardell_functions_uv.hpp':
    double vec_fuv(double *f, double xi, double xi1t, double xi2t) nogil
    double vec_fuv_x(double *f, double xi, double xi1t, double xi2t) nogil

cdef extern from 'bardell_functions_w.hpp':
    double vec_fw(double *f, double xi, double xi1t, double xi1r,
                  double xi2t, double xi2r) nogil
    double vec_fw_x(double *f, double xi, double xi1t, double xi1r,
                  double xi2t, double xi2r) nogil
    double vec_fw_xx(double *f, double xi, double xi1t, double xi1r,
                  double xi2t, double xi2r) nogil

DOUBLE = np.float64

cdef int NMAX = 30
cdef int DOF = 3


def fuvw(double [::1] c, object s, double [::1] xs, double [::1] ys,
        int num_cores=4):
    cdef double a, b
    cdef int m, n
    cdef double x1u, x2u
    cdef double x1v, x2v
    cdef double x1w, x1wr, x2w, x2wr
    cdef double y1u, y2u
    cdef double y1v, y2v
    cdef double y1w, y1wr, y2w, y2wr
    a = s.a
    b = s.b
    m = s.m
    n = s.n
    x1u = s.x1u; x2u = s.x2u
    x1v = s.x1v; x2v = s.x2v
    x1w = s.x1w; x1wr = s.x1wr; x2w = s.x2w ; x2wr = s.x2wr
    y1u = s.y1u; y2u = s.y2u
    y1v = s.y1v; y2v = s.y2v
    y1w = s.y1w; y1wr = s.y1wr; y2w = s.y2w ; y2wr = s.y2wr

    cdef int size_core, pti, i, j
    cdef double [:, ::1] us, vs, ws, phixs, phiys
    cdef double [:, ::1] xs_core, ys_core

    size = xs.shape[0]
    add_size = num_cores - (size % num_cores)
    if add_size == num_cores:
        add_size = 0
    new_size = size + add_size

    if (size % num_cores) != 0:
        xs_core = np.ascontiguousarray(np.hstack((xs, np.zeros(add_size))).reshape(num_cores, -1), dtype=DOUBLE)
        ys_core = np.ascontiguousarray(np.hstack((ys, np.zeros(add_size))).reshape(num_cores, -1), dtype=DOUBLE)
    else:
        xs_core = np.ascontiguousarray(np.reshape(xs, (num_cores, -1)), dtype=DOUBLE)
        ys_core = np.ascontiguousarray(np.reshape(ys, (num_cores, -1)), dtype=DOUBLE)

    size_core = xs_core.shape[1]

    us = np.zeros((num_cores, size_core), dtype=DOUBLE)
    vs = np.zeros((num_cores, size_core), dtype=DOUBLE)
    ws = np.zeros((num_cores, size_core), dtype=DOUBLE)
    phixs = np.zeros((num_cores, size_core), dtype=DOUBLE)
    phiys = np.zeros((num_cores, size_core), dtype=DOUBLE)

    for pti in prange(num_cores, nogil=True, chunksize=1, num_threads=num_cores,
                    schedule='static'):
        cfuvw(&c[0], m, n, a, b, &xs_core[pti,0],
              &ys_core[pti,0], size_core, &us[pti,0], &vs[pti,0], &ws[pti,0],
              x1u, x2u,
              x1v, x2v,
              x1w, x1wr, x2w, x2wr,
              y1u, y2u,
              y1v, y2v,
              y1w, y1wr, y2w, y2wr)

        cfwx(&c[0], m, n, a, b, &xs_core[pti,0], &ys_core[pti,0],
             size_core, &phixs[pti,0],
             x1w, x1wr, x2w, x2wr,
             y1w, y1wr, y2w, y2wr)

        cfwy(&c[0], m, n, a, b, &xs_core[pti,0], &ys_core[pti,0],
             size_core, &phiys[pti,0],
             x1w, x1wr, x2w, x2wr,
             y1w, y1wr, y2w, y2wr)

    for i in range(num_cores):
        for j in range(size_core):
            phixs[i, j] *= -1.
            phiys[i, j] *= -1.
    return (np.ravel(us)[:size], np.ravel(vs)[:size], np.ravel(ws)[:size],
            np.ravel(phixs)[:size], np.ravel(phiys)[:size])


def fstrain(double [::1] c, object s, double [::1] xs, double [::1] ys, int
            num_cores=4, int NLgeom=0):
    cdef double a, b, r, alpharad
    cdef int m, n
    cdef double x1u, x2u
    cdef double x1v, x2v
    cdef double x1w, x1wr, x2w, x2wr
    cdef double y1u, y2u
    cdef double y1v, y2v
    cdef double y1w, y1wr, y2w, y2wr
    a = s.a
    b = s.b
    r = s.r
    alpharad = s.alpharad
    m = s.m
    n = s.n
    x1u = s.x1u; x2u = s.x2u
    x1v = s.x1v; x2v = s.x2v
    x1w = s.x1w; x1wr = s.x1wr; x2w = s.x2w ; x2wr = s.x2wr
    y1u = s.y1u; y2u = s.y2u
    y1v = s.y1v; y2v = s.y2v
    y1w = s.y1w; y1wr = s.y1wr; y2w = s.y2w ; y2wr = s.y2wr

    cdef int size_core, pti
    cdef double [:, ::1] exxs, eyys, gxys, kxxs, kyys, kxys
    cdef double [:, ::1] xs_core, ys_core

    size = xs.shape[0]
    add_size = num_cores - (size % num_cores)
    if add_size == num_cores:
        add_size = 0
    new_size = size + add_size

    if (size % num_cores) != 0:
        xs_core = np.ascontiguousarray(np.hstack((xs, np.zeros(add_size))).reshape(num_cores, -1), dtype=DOUBLE)
        ys_core = np.ascontiguousarray(np.hstack((ys, np.zeros(add_size))).reshape(num_cores, -1), dtype=DOUBLE)
    else:
        xs_core = np.ascontiguousarray(np.reshape(xs, (num_cores, -1)), dtype=DOUBLE)
        ys_core = np.ascontiguousarray(np.reshape(ys, (num_cores, -1)), dtype=DOUBLE)

    size_core = xs_core.shape[1]

    exxs = np.zeros((num_cores, size_core), dtype=DOUBLE)
    eyys = np.zeros((num_cores, size_core), dtype=DOUBLE)
    gxys = np.zeros((num_cores, size_core), dtype=DOUBLE)
    kxxs = np.zeros((num_cores, size_core), dtype=DOUBLE)
    kyys = np.zeros((num_cores, size_core), dtype=DOUBLE)
    kxys = np.zeros((num_cores, size_core), dtype=DOUBLE)

    if alpharad != 0:
        raise NotImplementedError('Conical shells not suported')

    for pti in prange(num_cores, nogil=True, chunksize=1, num_threads=num_cores,
                    schedule='static'):
        cfstrain(&c[0], m, n, a, b, r, alpharad,
              &xs_core[pti,0], &ys_core[pti,0], size_core,
              &exxs[pti,0], &eyys[pti,0], &gxys[pti,0],
              &kxxs[pti,0], &kyys[pti,0], &kxys[pti,0],
              x1u, x2u,
              x1v, x2v,
              x1w, x1wr, x2w, x2wr,
              y1u, y2u,
              y1v, y2v,
              y1w, y1wr, y2w, y2wr, NLgeom)

    return (np.ravel(exxs)[:size], np.ravel(eyys)[:size], np.ravel(gxys)[:size],
            np.ravel(kxxs)[:size], np.ravel(kyys)[:size], np.ravel(kxys)[:size])


cdef void cfuvw(double *c, int m, int n, double a, double b, double *xs,
        double *ys, int size, double *us, double *vs, double *ws,
        double x1u, double x2u,
        double x1v, double x2v,
        double x1w, double x1wr, double x2w, double x2wr,
        double y1u, double y2u,
        double y1v, double y2v,
        double y1w, double y1wr, double y2w, double y2wr) nogil:
    cdef int i, j, col, pti
    cdef double x, y, u, v, w, xi, eta
    cdef double *fu
    cdef double *fv
    cdef double *fw
    cdef double *gu
    cdef double *gv
    cdef double *gw

    fu = <double *>malloc(NMAX * sizeof(double *))
    gu = <double *>malloc(NMAX * sizeof(double *))
    fv = <double *>malloc(NMAX * sizeof(double *))
    gv = <double *>malloc(NMAX * sizeof(double *))
    fw = <double *>malloc(NMAX * sizeof(double *))
    gw = <double *>malloc(NMAX * sizeof(double *))

    for pti in range(size):
        x = xs[pti]
        y = ys[pti]

        xi = 2*x/a - 1.
        eta = 2*y/b - 1.

        vec_fuv(fu, xi, x1u, x2u)
        vec_fuv(gu, eta, y1u, y2u)
        vec_fuv(fv, xi, x1v, x2v)
        vec_fuv(gv, eta, y1v, y2v)
        vec_fw(fw, xi, x1w, x1wr, x2w, x2wr)
        vec_fw(gw, eta, y1w, y1wr, y2w, y2wr)

        u = 0
        v = 0
        w = 0

        for j in range(n):
            for i in range(m):
                col = DOF*(j*m + i)
                u += c[col+0]*fu[i]*gu[j]
                v += c[col+1]*fv[i]*gv[j]
                w += c[col+2]*fw[i]*gw[j]

        us[pti] = u
        vs[pti] = v
        ws[pti] = w

    free(fu)
    free(gu)
    free(fv)
    free(gv)
    free(fw)
    free(gw)


cdef void cfwx(double *c, int m, int n, double a, double b, double *xs,
        double *ys, int size, double *wxs,
        double x1w, double x1wr, double x2w, double x2wr,
        double y1w, double y1wr, double y2w, double y2wr) nogil:
    cdef int i, j, col, pti
    cdef double x, y, wx, xi, eta
    cdef double *fwxi
    cdef double *gw

    fwxi = <double *>malloc(NMAX * sizeof(double *))
    gw = <double *>malloc(NMAX * sizeof(double *))

    for pti in range(size):
        x = xs[pti]
        y = ys[pti]

        xi = 2*x/a - 1.
        eta = 2*y/b - 1.

        vec_fw_x(fwxi, xi, x1w, x1wr, x2w, x2wr)
        vec_fw(gw, eta, y1w, y1wr, y2w, y2wr)

        wx = 0

        for j in range(n):
            for i in range(m):
                col = DOF*(j*m + i)
                wx += (2/a)*c[col+2]*fwxi[i]*gw[j]

        wxs[pti] = wx

    free(fwxi)
    free(gw)


cdef void cfwy(double *c, int m, int n, double a, double b, double *xs,
        double *ys, int size, double *wys,
        double x1w, double x1wr, double x2w, double x2wr,
        double y1w, double y1wr, double y2w, double y2wr) nogil:
    cdef int i, j, col, pti
    cdef double x, y, wy, xi, eta
    cdef double *fw
    cdef double *gweta

    fw = <double *>malloc(NMAX * sizeof(double *))
    gweta = <double *>malloc(NMAX * sizeof(double *))

    for pti in range(size):
        x = xs[pti]
        y = ys[pti]

        xi = 2*x/a - 1.
        eta = 2*y/b - 1.

        vec_fw(fw, xi, x1w, x1wr, x2w, x2wr)
        vec_fw_x(gweta, eta, y1w, y1wr, y2w, y2wr)

        wy = 0

        for j in range(n):
            for i in range(m):
                col = DOF*(j*m + i)
                wy += (2/b)*c[col+2]*fw[i]*gweta[j]

        wys[pti] = wy

    free(fw)
    free(gweta)


def fg(double[:, ::1] g, double x, double y, object s):
    cdef int i, j, col
    cdef double xi, eta
    cdef double *fu
    cdef double *fv
    cdef double *fw
    cdef double *fw_xi
    cdef double *gu
    cdef double *gv
    cdef double *gw
    cdef double *gw_eta

    if s.__class__.__name__ != 'Shell':
        raise ValueError('A Shell object must be passed')

    fu = <double *>malloc(NMAX * sizeof(double *))
    gu = <double *>malloc(NMAX * sizeof(double *))
    fv = <double *>malloc(NMAX * sizeof(double *))
    gv = <double *>malloc(NMAX * sizeof(double *))
    fw = <double *>malloc(NMAX * sizeof(double *))
    fw_xi = <double *>malloc(NMAX * sizeof(double *))
    gw = <double *>malloc(NMAX * sizeof(double *))
    gw_eta = <double *>malloc(NMAX * sizeof(double *))

    xi = 2*x/s.a - 1.
    eta = 2*y/s.b - 1.

    vec_fuv(fu, xi, s.x1u, s.x2u)
    vec_fuv(gu, eta, s.y1u, s.y2u)
    vec_fuv(fv, xi, s.x1v, s.x2v)
    vec_fuv(gv, eta, s.y1v, s.y2v)
    vec_fw(fw, xi, s.x1w, s.x1wr, s.x2w, s.x2wr)
    vec_fw_x(fw_xi, xi, s.x1w, s.x1wr, s.x2w, s.x2wr)
    vec_fw(gw, eta, s.y1w, s.y1wr, s.y2w, s.y2wr)
    vec_fw_x(gw_eta, eta, s.y1w, s.y1wr, s.y2w, s.y2wr)

    for j in range(s.n):
        for i in range(s.m):
            col = DOF*(j*s.m + i)
            g[0, col+0] = fu[i]*gu[j]
            g[1, col+1] = fv[i]*gv[j]
            g[2, col+2] = fw[i]*gw[j]
            g[3, col+2] = -(2/s.a)*fw_xi[i]*gw[j]
            g[4, col+2] = -(2/s.b)*fw[i]*gw_eta[j]

    free(fu)
    free(gu)
    free(fv)
    free(gv)
    free(fw)
    free(fw_xi)
    free(gw)
    free(gw_eta)


cdef void cfstrain(double *c, int m, int n, double a, double b,
        double r, double alpharad,
        double *xs, double *ys, int size,
        double *exxs, double *eyys, double *gxys,
        double *kxxs, double *kyys, double *kxys,
        double x1u, double x2u,
        double x1v, double x2v,
        double x1w, double x1wr, double x2w, double x2wr,
        double y1u, double y2u,
        double y1v, double y2v,
        double y1w, double y1wr, double y2w, double y2wr, int NLgeom) nogil:
    cdef int i, j, col, pti
    cdef double x, y, xi, eta
    cdef double exx, eyy, gxy, kxx, kyy, kxy
    cdef int flagcyl

    cdef double *fu
    cdef double *fuxi
    cdef double *fv
    cdef double *fvxi
    cdef double *fw
    cdef double *fwxi
    cdef double *fwxixi

    cdef double *gu
    cdef double *gueta
    cdef double *gv
    cdef double *gveta
    cdef double *gw
    cdef double *gweta
    cdef double *gwetaeta

    cdef double wxi, weta

    fu = <double *>malloc(NMAX * sizeof(double *))
    fuxi = <double *>malloc(NMAX * sizeof(double *))
    gu = <double *>malloc(NMAX * sizeof(double *))
    gueta = <double *>malloc(NMAX * sizeof(double *))
    fv = <double *>malloc(NMAX * sizeof(double *))
    fvxi = <double *>malloc(NMAX * sizeof(double *))
    gv = <double *>malloc(NMAX * sizeof(double *))
    gveta = <double *>malloc(NMAX * sizeof(double *))
    fw = <double *>malloc(NMAX * sizeof(double *))
    fwxi = <double *>malloc(NMAX * sizeof(double *))
    fwxixi = <double *>malloc(NMAX * sizeof(double *))
    gw = <double *>malloc(NMAX * sizeof(double *))
    gweta = <double *>malloc(NMAX * sizeof(double *))
    gwetaeta = <double *>malloc(NMAX * sizeof(double *))

    if r == 0:
        flagcyl = 0
    else:
        flagcyl = 1

    for pti in range(size):
        x = xs[pti]
        y = ys[pti]

        xi = 2*x/a - 1.
        eta = 2*y/b - 1.

        vec_fuv(fu, xi, x1u, x2u)
        vec_fuv_x(fuxi, xi, x1u, x2u)
        vec_fuv(gu, eta, y1u, y2u)
        vec_fuv_x(gueta, eta, y1u, y2u)
        vec_fuv(fv, xi, x1v, x2v)
        vec_fuv_x(fvxi, xi, x1v, x2v)
        vec_fuv(gv, eta, y1v, y2v)
        vec_fuv_x(gveta, eta, y1v, y2v)
        vec_fw(fw, xi, x1w, x1wr, x2w, x2wr)
        vec_fw_x(fwxi, xi, x1w, x1wr, x2w, x2wr)
        vec_fw_xx(fwxixi, xi, x1w, x1wr, x2w, x2wr)
        vec_fw(gw, eta, y1w, y1wr, y2w, y2wr)
        vec_fw_x(gweta, eta, y1w, y1wr, y2w, y2wr)
        vec_fw_xx(gwetaeta, eta, y1w, y1wr, y2w, y2wr)

        wxi = 0
        weta = 0

        for j in range(n):
            for i in range(m):
                col = DOF*(j*m + i)
                wxi += c[col+2]*fwxi[i]*gw[j]
                weta += c[col+2]*fw[i]*gweta[j]

        exx = 0
        eyy = 0
        gxy = 0
        kxx = 0
        kyy = 0
        kxy = 0

        for j in range(n):
            for i in range(m):
                col = DOF*(j*m + i)
                exx += c[col+0]*fuxi[i]*gu[j]*(2/a) + NLgeom*2/(a*a)*c[col+2]*fwxi[i]*gw[j]*wxi
                if flagcyl == 1:
                    eyy += c[col+1]*fv[i]*gveta[j]*(2/b) + 1/r*c[col+2]*fw[i]*gw[j] + NLgeom*2/(b*b)*c[col+2]*fw[i]*gweta[j]*weta
                else:
                    eyy += c[col+1]*fv[i]*gveta[j]*(2/b) + NLgeom*2/(b*b)*c[col+2]*fw[i]*gweta[j]*weta
                gxy += c[col+0]*fu[i]*gueta[j]*(2/b) + c[col+1]*fvxi[i]*gv[j]*(2/a) + NLgeom*4/(a*b)*(
                                        c[col+2]*fwxi[i]*gw[j]*weta +
                                        wxi*c[col+2]*fw[i]*gweta[j] )
                kxx += -c[col+2]*fwxixi[i]*gw[j]*4/(a*a)
                kyy += -c[col+2]*fw[i]*gwetaeta[j]*4/(b*b)
                kxy += -2*c[col+2]*fwxi[i]*gweta[j]*4/(a*b)

        exxs[pti] = exx
        eyys[pti] = eyy
        gxys[pti] = gxy
        kxxs[pti] = kxx
        kyys[pti] = kyy
        kxys[pti] = kxy

    free(fu)
    free(fuxi)
    free(gu)
    free(gueta)
    free(fv)
    free(fvxi)
    free(gv)
    free(gveta)
    free(fw)
    free(fwxi)
    free(fwxixi)
    free(gw)
    free(gweta)
    free(gwetaeta)

