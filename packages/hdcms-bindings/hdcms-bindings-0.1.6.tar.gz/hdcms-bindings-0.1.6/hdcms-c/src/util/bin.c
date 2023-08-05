#include <stdbool.h>
#include <math.h>
#include "array.h"
#include "bin.h"

struct matrix 
bin_stat_1D(const struct matarray A, double start, double end, double num_bins)
{
    struct matrix M = mat_zeros(A.length, (size_t)num_bins);
    for (size_t i = 0; i < A.length; i++) {
        struct matrix spectra = matarr_get(A, i);
        struct vec bin_heights = spec_vec(spectra, start, end, num_bins);
        vec_to_row(M, bin_heights, i);
        vec_free(bin_heights);
    }

    struct matrix B = mat_zeros((size_t)num_bins, 2);
    for (size_t i = 0; i < num_bins; i++) {
        struct vec ith_bin = vec_from_col(M, i);
        mat_set(B, i, 0, vec_mean(ith_bin));
        mat_set(B, i, 1, vec_std(ith_bin));
    }
    mat_free(M);
    return B;
}

// binary search
//
// this condition is always true (other cases need to be handled in get_bin()): 
//
//      bins[start] <= val < bins[end]
static size_t
binary_search(const struct vec bins, size_t start, size_t stop, double val)
{
    // assert condition
    assert(vec_get(bins, start) <= val && val < vec_get(bins, stop));

    if (stop == start + 1)
        return start;

    size_t i = (start + stop) / 2;
    if (vec_get(bins, i) <= val) {
        return binary_search(bins, i, stop, val);
    } else {
        return binary_search(bins, start, i, val);
    }
}

static size_t
get_bin(const struct vec bins, double val)
{
    if (val < vec_get(bins, 0)) {
        return 0;
    } else if (vec_get(bins, bins.length - 1) <= val) {
        return bins.length - 1;
    }
    return binary_search(bins, 0, bins.length - 1, val);
}

struct vec 
spec_vec(const struct matrix m, double start, double end, double num_bins)
{
    // +1 since linspace allocates a size $n$ array, but that's 1 less than the
    // number of bins
    struct vec t = vec_linspace(start, end, num_bins+1);
    struct vec v = vec_zeros((size_t)num_bins);

    for (size_t i = 0; i < m.len1; i++) {
        size_t i_max = get_bin(t, mat_get(m, i, 0));
        vec_set(v, i_max, mat_get(m, i, 1));
    }
    vec_free(t);
    return v;
}

void
scaled_data(const struct matrix m, char type)
{
    if (type == 'm') {
        // max
        struct vec v = vec_from_col(m, 1);
        double max = vec_max(v);
        vec_invscale(v, max);
    } else if (type == 'u') {
        // unit
        struct vec v = vec_from_col(m, 1);
        double dot = vec_dot(v, v);
        vec_invscale(v, sqrt(dot));
    } else if (type == 'n') {
        // no scaling
        return;
    } else {
        WARNING("specified unimplemented scaling `%c`, must be: m, u, or n", type);
    }
}

double 
prob_dot_prod(const struct matrix u_orig, const struct matrix v_orig, double desingularization)
{
    // input are nx2 matrices of (mean, std) pairs
    // assert input correct
    if (u_orig.len2 != 2) {
        WARNING("%s vec size not equal to 2 (maybe pass --2d)\n", __func__);
        exit(1);
        // unreachable
    }
    if (v_orig.len2 != 2) {
        WARNING("%s vec size not equal to 2 (maybe pass --2d)\n", __func__);
        exit(1);
        // unreachable
    }

    struct matrix u = mat_copy(u_orig);
    struct matrix v = mat_copy(v_orig);

    struct vec u_mean = vec_from_col(u, 0);
    struct vec u_std = vec_from_col(u, 1);
    struct vec v_mean = vec_from_col(v, 0);
    struct vec v_std = vec_from_col(v, 1);

    // add small float so we don't have 0 std
    vec_add_const(u_std, desingularization);
    vec_add_const(v_std, desingularization);

    struct vec weights = vec_copy(u_std);
    vec_scale(weights, 2);
    vec_multiply(weights, v_std);

    // sq_sum = u_std^2 + v_std^2       <-- all pointwise
    vec_square(u_std);
    vec_square(v_std);
    struct vec sq_sum = u_std; // rename for clarity
    vec_add(sq_sum, v_std);

    vec_divide(weights, sq_sum);
    vec_sqrt(weights);

    struct vec tmp3 = vec_copy(u_mean);
    vec_sub(tmp3, v_mean);
    vec_square(tmp3);
    vec_scale(tmp3, -0.5);
    vec_divide(tmp3, sq_sum);

    vec_exp(tmp3);

    vec_multiply(weights, tmp3);
    vec_free(sq_sum);
    vec_free(tmp3);

    vec_multiply(weights, v_mean);
    double denom = sqrt(vec_dot(u_mean, u_mean)) * sqrt(vec_dot(v_mean, v_mean));
    double ans = vec_dot(weights, u_mean) / denom;

    vec_free(weights);
    mat_free(u);
    mat_free(v);
    return ans;
}

